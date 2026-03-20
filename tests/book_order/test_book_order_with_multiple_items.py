#Adding multiple items in book order and verify the quantity 
# match and amount


import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import pytest

load_dotenv()

@pytest.mark.book_order
@pytest.mark.regression
def test_book_order_with_multiple_items():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, slow_mo=800)
        page = browser.new_page()
        page.set_default_timeout(30000)

        page.goto("https://test-vidirav15.frappe.cloud/login")


        page.fill("#login_email", os.getenv("ERP_USER"))
        page.fill("#login_password", os.getenv("ERP_PASS"))
        page.click("button:has-text('Login')")


        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)
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
        page.get_by_role("combobox", name="Product Code").fill("N40626620")
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Product Code").press("Enter")
        
        page.get_by_role("textbox", name="Qty").click()
        page.get_by_role("textbox", name="Qty").fill("150")
        page.get_by_role("textbox", name="Qty").press("Enter")
        
        page.get_by_role("button", name="Add Row").click()
        
        rows = page.locator(".grid-body .grid-row")
        
        page.get_by_role("combobox", name="Product Code").fill("M41510102")
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Product Code").press("Enter")
        
        row1 = page.locator('.grid-row[data-idx="1"]')
        row2 = page.locator('.grid-row[data-idx="2"]')
        first_item_quantity = float(row1.locator('[data-fieldname="qty"] .static-area').inner_text())
        second_item_quantity= float(row2.locator('[data-fieldname="qty"] .static-area').inner_text())
        
        first_item_amount_text = (row1.locator('[data-fieldname="amount"] .static-area').inner_text())
        first_item_amount = float(first_item_amount_text.replace("₹", "").replace(",", "").strip())
        
        second_item_amount_text =(row2.locator('[data-fieldname="amount"] .static-area').inner_text())
        second_item_amount = float(second_item_amount_text.replace("₹", "").replace(",", "").strip())

        total_quantity = float(page.locator('input[data-fieldname="total_qty"]').input_value())
        total_amount_text = (page.locator('input[data-fieldname="total_amount"]').input_value())
        total_amount = float(total_amount_text.replace(",", "").strip())
        
        assert total_quantity == first_item_quantity + second_item_quantity, f"Total quantity{total_quantity} is not equal to {first_item_quantity} + {second_item_quantity}"
        assert round(total_amount,3) == round(first_item_amount,3) + round(second_item_amount,3) , f"Total quantity{total_amount} is not equal to {first_item_amount} + {second_item_amount}"
        
        print("Total quantity and amount verified auccessfully.")
          
        browser.close()
