#Booking an order with promitional scheme of rate change with quantity slab
#and verifying the correct rate appears when quantity goes out of slab.

import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import pytest

load_dotenv()

@pytest.mark.book_order
@pytest.mark.regression
def test_book_order_promotional_scheme__slab_quantity_decrease():
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
        page.get_by_role("combobox", name="Product Code").fill("N40626620")
        page.wait_for_timeout(3000)
        page.get_by_role("combobox", name="Product Code").press("Enter")
        
        
        one_item_rate_text = page.get_by_role("textbox", name="Rate", exact=True).input_value()
        one_item_rate = round(float(one_item_rate_text.replace(",", "").strip()), 3)
        print(f"one item Rate: {one_item_rate}")     
        
        page.get_by_role("textbox", name="Qty").click()
        page.get_by_role("textbox", name="Qty").fill("200")
        page.get_by_role("textbox", name="Qty").press("Enter")
              
        page.get_by_role("textbox", name="Qty").click()
        page.get_by_role("textbox", name="Qty").fill("199")
        page.get_by_role("textbox", name="Qty").press("Enter")
        
        page.wait_for_timeout(5000)
        
        dec_item_rate_text = page.get_by_role("textbox", name="Rate", exact=True).input_value()

        dec_item_rate = round(float(dec_item_rate_text.replace(",", "").strip()), 3)
          
        print("Verifying the rate of one item and rate of quantity less than the first slab is same") 
        
        assert one_item_rate == dec_item_rate, f"Rate is not same for one item {one_item_rate} and quantity less than the first slab  {dec_item_rate}"
        
        print("Verifying the rate for one item and decreased quantity lower than slab is completed successfully.")   
    
        browser.close()