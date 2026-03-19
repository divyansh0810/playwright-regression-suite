#Creation of a book order with disabled customer 
# and verify the popup message appears while submit the order.

import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from playwright.sync_api import expect
import pytest

load_dotenv()

@pytest.mark.book_order
@pytest.mark.regression
def test_book_order_disabled_customer():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=800)
        page = browser.new_page()
        page.set_default_timeout(30000)

        page.goto("https://test-vidirav15.frappe.cloud/login")


        page.fill("#login_email", os.getenv("ERP_USER"))
        page.fill("#login_password", os.getenv("ERP_PASS"))
        page.click("button:has-text('Login')")


        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)
        page.locator("a").filter(has_text="ERPNext").click()
        
        page.get_by_label("Customer").click()
        page.get_by_role("button", name="Clear all filters").click()
        page.get_by_role("button", name="Filter", exact=True).click()
        
        page.get_by_role("combobox").nth(3).click()
        page.get_by_role("combobox").nth(3).fill("Disabled")
        
        page.get_by_role("paragraph",).filter(has_text="Disabled").click()
        
        page.get_by_role("combobox").nth(5).select_option("Yes")
        page.get_by_role("button", name="Apply Filters").click()
        
        target_row = page.locator('.list-row').nth(0)

        customer_id = target_row.locator('a[data-filter^="name"]').inner_text().strip()
        
        page.get_by_role("combobox", name="Search or type a command").click()
        page.get_by_role("combobox", name="Search or type a command").fill("Book Order")
        page.get_by_role("combobox", name="Search or type a command").press("Enter")
        
        page.get_by_role("button", name="Add Book Order").click()
        
        page.locator('input[data-fieldname="customer"]').fill(customer_id)
         
        page.locator('input[data-fieldname="set_warehouse"]').fill("WH-MAIN - VIPL")
        page.keyboard.press("Enter")
        
        page.locator(".col.grid-static-col.col-xs-2.error").click()
        page.get_by_role("combobox", name="Product Code").fill("M41510102")
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Product Code").press("Enter")
        
        page.get_by_role("button", name="Save").click()
        page.wait_for_timeout(5000)
        page.screenshot(path="reports/before_submit.png", full_page=True)

        submit_btn = page.locator('button:has-text("Submit")')

        print("Count:", submit_btn.count())
        print("Visible:", submit_btn.is_visible())

        if submit_btn.count() == 0:
            print("❌ Submit not in DOM")
        elif not submit_btn.is_visible():
            print("⚠️ Submit present but not visible")
        else:
            print("✅ Submit ready")

# print page content (optional but powerful)
        submit_btn = page.locator('button:has-text("Submit")')

# wait for UI to settle
        page.wait_for_load_state("networkidle")

# remove any overlay
        page.wait_for_selector(".modal-backdrop", state="detached", timeout=60000)

# wait for button
        # submit_btn.wait_for(state="visible", timeout=60000)
        submit_btn.click()
        page.get_by_role("button", name="Yes").click()
        page.wait_for_timeout(3000)
        heading = page.get_by_role("heading", name= "Message").inner_text()
        message = page.locator(".msgprint").inner_text()
        
        assert "Message" in heading

        assert f"Customer {customer_id} is disabled" in message
        
        print("Disabled customer not able to make order verified successfully.")
        browser.close()
