import os
import time
from playwright.sync_api import sync_playwright

EMAIL = os.environ.get("KATABUMP_EMAIL")
PASSWORD = os.environ.get("KATABUMP_PASSWORD")
SERVER_ID = os.environ.get("SERVER_ID", "d1712508")

def main():
    if not EMAIL or not PASSWORD:
        print("ERROR: KATABUMP_EMAIL or KATABUMP_PASSWORD secrets are not set.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()

        try:
            print("Opening Katabump login page...")
            page.goto("https://control.katabump.com/auth/login", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)

            print("Filling in credentials...")
            user_input = page.locator('input[name="username"], input[name="email"], input[type="text"], input[type="email"]').first
            pass_input = page.locator('input[name="password"], input[type="password"]').first

            user_input.fill(EMAIL)
            pass_input.fill(PASSWORD)

            submit_btn = page.locator('button[type="submit"], input[type="submit"]').first
            submit_btn.click()

            page.wait_for_timeout(8000)

            print(f"Going to server {SERVER_ID}...")
            page.goto(f"https://control.katabump.com/server/{SERVER_ID}", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(6000)

            renew_btn = page.locator('button:has-text("Renew"), a:has-text("Renew")')
            if renew_btn.count() > 0 and renew_btn.first.is_visible():
                renew_btn.first.click()
                print("Renew button clicked successfully!")
                page.wait_for_timeout(3000)
            else:
                print("Renew button not active or server does not need renewal.")

        except Exception as e:
            print(f"An error occurred: {e}")
            page.screenshot(path="error_screenshot.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    main()
