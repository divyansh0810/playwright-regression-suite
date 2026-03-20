#Booking an order with promitional scheme of rate change with quantity slab
#and verifying the correct rate changes with correct quantity slab lower value.

import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import pytest

load_dotenv()

@pytest.mark.book_order
@pytest.mark.regression
def test_book_order_promotional_scheme_quantity_slab_lower_boundary_value():
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
        
        page.get_by_role("textbox", name="Qty").click()
        page.get_by_role("textbox", name="Qty").fill("200")
        page.get_by_role("textbox", name="Qty").press("Enter")
        
        page.wait_for_timeout(5000)
        slab1_item_rate_text = page.get_by_role("textbox", name="Rate", exact=True).input_value()

        slab1_item_rate = round(float(slab1_item_rate_text.replace(",", "").strip()), 3)
    
        print("Verifying price for 200-499 quantity is 28")
        assert slab1_item_rate== 28, f"Expected slab 1 price 28 got {slab1_item_rate}"
        
        print("Verification of slab 1 price completed successfully.")
        
        print("Verification of rate for slab 2")
        
        page.get_by_role("textbox", name="Qty").click()
        page.get_by_role("textbox", name="Qty").fill("500")
        page.get_by_role("textbox", name="Qty").press("Enter")
        
        page.wait_for_timeout(5000)
        
        slab2_item_rate_text = page.get_by_role("textbox", name="Rate", exact=True).input_value()

        slab2_item_rate = round(float(slab2_item_rate_text.replace(",", "").strip()), 3)
            
        print("Verifying price for 500-999 quantity is 27")
        assert slab2_item_rate== 27, f"Expected slab 2 price 27 got {slab2_item_rate}"
        
        print("Verification of slab 2 price completed successfully.")
        
        print("Verification of rate for slab 3")
        
        page.get_by_role("textbox", name="Qty").click()
        page.get_by_role("textbox", name="Qty").fill("1000")
        page.get_by_role("textbox", name="Qty").press("Enter")
        
        page.wait_for_timeout(5000)
        
        slab3_item_rate_text = page.get_by_role("textbox", name="Rate", exact=True).input_value()

        slab3_item_rate = round(float(slab3_item_rate_text.replace(",", "").strip()), 3)
          
        print("Verifying price for 1000 and above quantity is 26")
        assert slab3_item_rate== 26, f"Expected slab 3 price 26 got {slab3_item_rate}"
        
        print("Verification of slab 3 price completed successfully.")
        
        print("Promotional scheme slab price for lower boundary verified successfully.")
        
        browser.close()
        
        
        
    