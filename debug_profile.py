import re
import time
from playwright.sync_api import sync_playwright

def test_profile(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        print(f"Navigating to {url}")
        page.goto(url)
        
        # Wait for meaningful content or timeout
        try:
            page.wait_for_load_state("domcontentloaded")
            time.sleep(5)
            page.screenshot(path="debug_screenshot.png")
            print("Screenshot saved to debug_screenshot.png")
            print(f"Title: {page.title()}")
            
            # Check for specific elements
            content = page.content()
            if "Just a moment" in content or "Challenge" in content:
                print("DETECTED: Cloudflare/Anti-bot challenge")
            else:
                print("No obvious challenge text found.")
                
        except Exception as e:
            print(f"Error: {e}")
            
        browser.close()

if __name__ == "__main__":
    test_profile("https://www.whatnot.com/user/jalen4l")
