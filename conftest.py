import pytest
import pandas as pd
import os
from datetime import datetime

results = []

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    start_time = datetime.now()

    outcome = yield
    report = outcome.get_result()

    end_time = datetime.now()

    if report.when == "call":

        error_message = ""
        screenshot_path = ""

        if report.failed:

            error_message = report.longrepr.reprcrash.message

            page = item.funcargs.get("page", None)

            if page:
                os.makedirs("reports/screenshots", exist_ok=True)

                screenshot_name = f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                screenshot_path = f"reports/screenshots/{screenshot_name}"

                page.screenshot(path=screenshot_path)

        results.append({
            "Test Name": item.name,
            "Status": report.outcome,
            "Start Time": start_time.strftime("%H:%M:%S"),
            "End Time": end_time.strftime("%H:%M:%S"),
            "Duration (sec)": round(report.duration, 2),
            "Error": error_message,
            "Screenshot": screenshot_path
        })


def pytest_sessionfinish(session, exitstatus):

    os.makedirs("reports", exist_ok=True)

    df = pd.DataFrame(results)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    file_path = f"reports/regression_report_{timestamp}.xlsx"

    df.to_excel(file_path, index=False)

    print(f"\nExcel Report Generated: {file_path}")
