#Adding same items in two rows and verify popup message appeaars.

import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import pytest

load_dotenv()

@pytest.mark.book_order
@pytest.mark.regression
def test_book_order_with_duplicate_items():
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
        
        page.get_by_role("button", name="Add Row").click()
        
        page.get_by_role("combobox", name="Product Code").fill("M41510102")
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Product Code").press("Enter")
        
        page.wait_for_timeout(2000)
        
        close_btn = page.locator(".btn.btn-modal-close")
        if close_btn.is_visible():
            close_btn.click()
            page.get_by_role("combobox", name="Product Code").fill("M41510102")
            page.wait_for_timeout(3000)
            page.get_by_role("combobox", name="Product Code").press("Enter")
            
        heading = page.get_by_role("heading", name= "Message").inner_text()
        message = page.locator(".msgprint").inner_text()
        
        print("Verifying message from popup")
        assert "Message" in heading

        assert f"Duplicate Item Code found in Row 1." in message
        
        print("Verification of duplicate item completed successfully.")
        browser.close()