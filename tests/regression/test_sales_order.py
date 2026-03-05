import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import pytest

load_dotenv()

@pytest.mark.regression

def test_open_sales_order():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=800)
        page = browser.new_page()

        page.goto("https://test-vidirav15.frappe.cloud/login")


        page.fill("#login_email", os.getenv("ERP_USER"))
        page.fill("#login_password", os.getenv("ERP_PASS"))
        page.click("button:has-text('Login')")


        page.wait_for_load_state("networkidle")
        
        page.wait_for_selector("text=Home")

        page.goto("https://test-vidirav15.frappe.cloud/app/sales-order")


        page.wait_for_selector("text=Sales Order")

        print("Sales Order page opened successfully")

        browser.close()
