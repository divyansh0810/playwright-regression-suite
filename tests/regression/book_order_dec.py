#Creating a book order with increased quantity save the price and amount of increase quantity
#then decrease quantity to one and verify the amount for one item reflecting correct by dividing the 
#increased quantity amount by increased quantity.

import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import pytest

load_dotenv()

@pytest.mark.book_order
@pytest.mark.regressions
def test_book_order_decrease_quantity():
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
        page.locator(".col.grid-static-col.col-xs-2.error").click()
        page.get_by_role("combobox", name="Product Code").fill("JL113840")
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Product Code").press("Enter")
        
        page.get_by_role("textbox", name="Qty").click()
        page.get_by_role("textbox", name="Qty").fill("50")
        page.get_by_role("textbox", name="Qty").press("Enter")
        
        inc_item_amount = page.get_by_role("textbox",name="Amount").input_value()
        print(f"Inc item amount: {inc_item_amount}")
        
        float_inc_item_amount= float(inc_item_amount.replace(",", ""))
        print(f"Amount of inc item in float {float_inc_item_amount}") 
        
        inc_qty = page.locator('input[data-fieldname="qty"]').input_value()
        print(f"Increased quantity: {inc_qty}")
        
        float_inc_qty= float(inc_qty.replace(",", ""))
        print(f"Increased quantity in float: {float_inc_qty}")
        
        page.get_by_role("textbox", name="Qty").click()
        page.get_by_role("textbox", name="Qty").fill("1")
        page.get_by_role("textbox", name="Qty").press("Enter")
        
        one_item_amount = page.get_by_role("textbox", name="Amount").input_value()
        print(f"amount of one item {one_item_amount}")
        float_one_item_amount= float(one_item_amount.replace(",", ""))
        print(f"amount of one item in float {float_one_item_amount}")
        
        expected_amount = float_inc_item_amount / float_inc_qty
        print(f"expected amount {expected_amount}")
        
        print("Verifying price after decreasing")

        assert round(float_one_item_amount, 3) == round(expected_amount, 3), \
    f"Mismatch: Amount after inc items({round(float_one_item_amount,3)}) != amount({round(expected_amount,3)})"
    
        print("Verifying price after decreasing passed successfully.")
        
        browser.close()
        
        
        
        
        
        
