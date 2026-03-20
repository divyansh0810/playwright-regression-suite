#Booking an item with free item scheme and verifying free item is added 
#when free item eligible quantity is reached and verifying the rate is 0 
# for free item and code is same.

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
        page.set_default_timeout(60000)

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
        page.wait_for_timeout(3000)
        page.screenshot(path="reports/before_qnty.png", full_page=True)
    
        page.get_by_role("textbox", name="Qty").click()
        page.get_by_role("textbox", name="Qty").fill("20")
        page.get_by_role("textbox", name="Qty").press("Enter")
        first_row_qnty = page.locator('input[data-fieldname="qty"]').input_value()
        page.wait_for_timeout(3000)
        
        ordered_qty= float(first_row_qnty.replace(",", ""))
        print(f" quantity ordered: {ordered_qty}")
        rows = page.locator(".grid-body .grid-row")
        
        print("Verifying rows count increase to 2")

        row_count = rows.count()

        print(f"Row count: {row_count}")

        assert row_count == 2, f"Expected 2 rows but found {row_count}"
        
        
        row1 = page.locator('.grid-row[data-idx="1"]')
        row2 = page.locator('.grid-row[data-idx="2"]')
        
        main_item_product_code = row1.locator('[data-fieldname="product_code"] .static-area').inner_text()
        free_item_product_code = row2.locator('[data-fieldname="product_code"] .static-area').inner_text()
       
        print("Verifying code should be the same for both")

        print("Main item code:", main_item_product_code)
        print("free item code:", free_item_product_code)

        assert main_item_product_code == free_item_product_code, "Product codes do not match"
        
        print("Verifying free item rate is zero")
        
        free_item_rate = row2.locator('[data-fieldname="rate"] .static-area').inner_text()

        rate = float(free_item_rate.replace("₹", "").replace(",", "").strip())

        print(rate)

        assert rate == 0.0, "Free item rate should be zero"
        
        print("Verifying free item amount is zero")
        
        free_item_amount = row2.locator('[data-fieldname="amount"] .static-area').inner_text()

        amount = float(free_item_amount.replace("₹", "").replace(",", "").strip())

        assert amount == 0.0, "Free item rate should be zero"
        
        print("Free item verification is done successfully.")
        
        browser.close()
        
        
        
