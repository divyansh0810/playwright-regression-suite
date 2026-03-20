#Adding a item with free item scheme after free item is added, decreasing
#the quantity and verify free item is removed.

import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import pytest

load_dotenv()

@pytest.mark.book_order
@pytest.mark.regression
def test_book_order_promotional_scheme_free_item():
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
        
        page.get_by_role("textbox", name="Qty").click()
        page.get_by_role("textbox", name="Qty").fill("20")
        page.get_by_role("textbox", name="Qty").press("Enter")
        
        page.wait_for_timeout(3000)
        
        rows = page.locator(".grid-body .grid-row")
        
        print("Verifying rows count increase to 2")

        row_count = rows.count()

        assert row_count == 2, f"Expected 2 rows but found {row_count}"
        
        print("Decreasing quantity to remove the free item")
        page.get_by_role("textbox", name="Qty").click()
        page.get_by_role("textbox", name="Qty").fill("1")
        page.get_by_role("textbox", name="Qty").press("Enter")
        
        page.wait_for_timeout(3000)
        
        
        rows = page.locator(".grid-body .grid-row")
        
        print("Verifying free item removed")

        row_count = rows.count()

        print(f"Row count after decreasing quantity and removal of free quantity: {row_count}")

        assert row_count == 1, f"Expected 2 rows but found {row_count}"
        
        print("Free item removal after quantity decreasing is successfully verified.")

        browser.close()