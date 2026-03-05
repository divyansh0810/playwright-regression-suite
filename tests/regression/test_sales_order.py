import pytest
import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

load_dotenv()

@pytest.mark.regression
def test_open_sales_order():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True, slow_mo=800)
        page = browser.new_page()

        page.goto("https://test-vidirav15.frappe.cloud/login")

        # Fetch credentials
        user = os.getenv("ERP_USER")
        password = os.getenv("ERP_PASS")

        # Validate environment variables
        assert user is not None, "ERP_USER not set"
        assert password is not None, "ERP_PASS not set"

        # Fill login form
        page.fill("#login_email", user)
        page.fill("#login_password", password)

        page.click("button:has-text('Login')")

        page.wait_for_load_state("networkidle")

        page.goto("https://test-vidirav15.frappe.cloud/app/sales-order")

        page.wait_for_selector("text=Sales Order")

        browser.close()
