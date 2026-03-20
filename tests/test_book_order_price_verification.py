#Verifying the  MRP and Price list rate are same on book order and item 
#price list. And Book order price list rate is equal to sum of rate and discount.

import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import pytest

load_dotenv()

@pytest.mark.book_order
@pytest.mark.regression
def test_book_order_price_verification():
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
        qty = page.locator('input[data-fieldname="qty"]').input_value()

        assert qty == "1", f"Expected qty to be 1 but got {qty}"
        print(qty)
        book_order_mrp = float(page.locator('input[data-fieldname="mrp"]').input_value())
        print("MRP on book order page:",book_order_mrp)
        
        book_order_rate = float(page.locator('input[data-fieldname="rate"]').input_value())
        print(" Rate on book order page:",book_order_rate)
        
        book_order_plr = float(page.locator('input[data-fieldname="price_list_rate"]').input_value())
        print("Price List Rate on book order page:",book_order_plr)
        
        page.locator(".btn-open-row > a").click()
        discount = float(page.get_by_role("textbox").nth(5).input_value())
        assert round(book_order_plr, 3) == round(book_order_rate + discount, 3), \
        f"Mismatch: price_list_rate({book_order_plr}) != rate({book_order_rate}) + discount({discount})"

        print("Price calculation of discount and total verified successfully")
        
        page.locator(".btn.btn-secondary.btn-sm.pull-right").first.click()
        page.get_by_role("combobox", name="Search or type a command").click()
        page.get_by_role("combobox", name="Search or type a command").fill("Item Price List")
        page.get_by_role("link", name="Item Price List", exact=True).click()
        page.get_by_role("combobox", name="Item Code").click()
        page.get_by_role("combobox", name="Item Code").fill("M41510102")
        page.get_by_role("combobox", name="Item Code").press("Enter")
        page.get_by_role("link", name="RR.F.REST LH RAY-MEBESTO").first.click()
        item_list_plr= float(page.get_by_role("textbox").nth(1).input_value())
        print("Price List Rate on item list page:", item_list_plr)
        item_list_mrp = float(page.get_by_role("textbox").nth(2).input_value())
        print("MRP on item list page:", item_list_mrp)
        assert round(book_order_plr,3) == round(item_list_plr,3), f"Rate mismatch: Book order price list rate {book_order_plr} not equal to item list price list rate {item_list_plr}"
        assert round(book_order_mrp,3) == round(item_list_mrp,3), f"MRP mismatch: Book order MRP {book_order_mrp} not equal to item list price list rate {item_list_mrp}"
        print("Price calculation of book order and price list page verified successfully.")
        
        browser.close()