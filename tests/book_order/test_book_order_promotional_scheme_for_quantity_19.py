#Adding a item in book order which has free item promotional scheme applied
#and making the quantity to 19 and verify a informational message appears.

import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from playwright.sync_api import expect
import pytest

load_dotenv()

@pytest.mark.book_order
@pytest.mark.regression
def test_book_order_promotional_scheme_free_item_19_quantity():
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
        page.locator('input[data-fieldname="set_warehouse"]').fill("WH-MAIN - VIPL")
        page.keyboard.press("Enter")
        
        if page.locator(".modal-content").is_visible():
            page.locator(".btn-modal-close").click()
            page.wait_for_selector(".modal-backdrop", state="detached")
        
        page.locator('.grid-row[data-idx="1"] [data-fieldname="product_code"].error.bold').click()
        page.get_by_role("combobox", name="Product Code").fill("M41510102")
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Product Code").press("Enter")
        page.wait_for_timeout(2000)
        
        product_code = page.get_by_role("combobox",name="Product Code").input_value()
        
        page.get_by_role("textbox", name="Qty").click()
        page.get_by_role("textbox", name="Qty").fill("19")
        page.get_by_role("textbox", name="Qty").press("Enter")
        
        popup = page.locator(".msgprint")
        
        print("Verifying popup visible")

        expect(popup).to_be_visible()
        
        print("Verifying the message of popup")

        expected_message = f"If you sale 20.0 quantities of the item {product_code}, the scheme F.REST will be applied on the item."

        expect(popup).to_contain_text(expected_message, timeout=10000)
        
        print("Test for promotional scheme free item with 19 quantities verified successfully.")
        
        browser.close()
        