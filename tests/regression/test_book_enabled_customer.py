#Creation of a book order with enabled customer 
# and verify the customer is enabled in customer list.

import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import pytest

load_dotenv()

@pytest.mark.book_order
@pytest.mark.regression
def test_book_order_enabled_customer():
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
        
        

        page.get_by_role("link", name="Selling").click()

        page.get_by_role("link", name="Book Order").click()

        page.wait_for_selector("text=Book Order")

        print("Book Order page opened")
        
        page.get_by_role("button", name="Add Book Order").click()
        
        
        
        page.locator('input[data-fieldname="customer"]').fill("C")
        page.locator('div[role="option"]').first.click()
        page.locator(".btn.btn-modal-close").click()
        customer_id =  page.get_by_role("combobox").nth(2).input_value()
        print(customer_id)
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Search or type a command").click()
        page.get_by_role("combobox", name="Search or type a command").fill("Customer List")
        page.get_by_role("combobox", name="Search or type a command").press("Enter")
        page.get_by_role("button", name="Clear all filters").click()
        page.get_by_role("textbox", name="ID").click()
        page.get_by_role("textbox", name="ID").fill(customer_id)
        
        target_row = page.locator('.list-row').filter(
    has=page.locator(f'[data-filter="name,=,{customer_id}"]')
)

        
        customer_id_on_customer_page = target_row.locator('[data-filter^="name"]').inner_text().strip()
        print(customer_id_on_customer_page)
        status = target_row.locator(".indicator-pill .ellipsis").first.inner_text().strip()
        print(status)
        
        print("Verifying the customer-ID and the status is enabled for the customer")
        
        assert customer_id == customer_id_on_customer_page, f"Customer id mismatch."
        assert status == "Enabled", f"Customer is not enabled."
        
        print("Enabled customer verification is successfully done.")
        
        browser.close()
        
    
