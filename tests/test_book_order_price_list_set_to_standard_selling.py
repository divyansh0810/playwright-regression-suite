#Checking the price list on book order page set to Standard Selling.

import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import pytest

load_dotenv()

@pytest.mark.book_order
@pytest.mark.regression
def test_book_order_price_list_set_to_standard_selling():
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
        
        page.locator(".section-head.collapsible.collapsed > .ml-2 > .es-icon").click()

        selling_price_list= page.locator('[data-fieldname="selling_price_list"] input').input_value()
        
        assert selling_price_list== "Standard Selling", f"Selling price list is not set to Standard Selling ,it is {selling_price_list}"
        
        print("Price list set to standard selling verified successfully.")
        
        browser.close()