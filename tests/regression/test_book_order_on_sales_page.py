#Adding multiple items and submit book order with it and verify the 
#quantity and amount in sales order are same.


import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import pytest

load_dotenv()

@pytest.mark.book_order
@pytest.mark.regression
def test_book_order_amount_and_quantity_verification_in_sales_order():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)
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
        page.get_by_role("textbox", name="Qty").fill("150")
        page.get_by_role("textbox", name="Qty").press("Enter")
        
        page.wait_for_timeout(3000)
        
        total_quantity = float(page.locator('input[data-fieldname="total_qty"]').input_value())
        total_amount_text = (page.locator('input[data-fieldname="total_amount"]').input_value())
        total_amount = float(total_amount_text.replace(",", "").strip())
        
        page.get_by_role("button", name="Save").click()
        page.get_by_role("button", name="Submit").click()
        page.get_by_role("button", name="Yes").click()
        page.locator(".btn.btn-modal-close").first.click()
        
        total_quantity_in_sales = float(page.locator('input[data-fieldname="total_qty"]').input_value())
        total_amount_in_sales_text = (page.locator('input[data-fieldname="total_amount"]').input_value())
        total_amount_in_sales = float(total_amount_in_sales_text.replace(",", "").strip())
        
        assert round(total_quantity,3)== round(total_quantity_in_sales,3), f" Quantity mismatch {total_quantity_in_sales} is not equal to {total_quantity}"
        assert round(total_amount,3)== round(total_amount_in_sales,3), f" Quantity mismatch {total_amount_in_sales} is not equal to {total_amount}"
        
        print("Verification of amount and quantity in sales order successfully completed.")

        browser.close()
