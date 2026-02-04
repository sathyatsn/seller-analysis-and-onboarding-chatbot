import time
from playwright.sync_api import sync_playwright

def discover_sellers(target_count=150):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        sellers = set()
        categories = [
            "https://www.whatnot.com/tag/trading_card_games",
            "https://www.whatnot.com/tag/funko",
            "https://www.whatnot.com/tag/comics",
            "https://www.whatnot.com/tag/sports_cards"
        ]
        
        for cat in categories:
            if len(sellers) >= target_count:
                break
                
            print(f"Navigating to {cat}")
            try:
                page.goto(cat, wait_until="domcontentloaded")
                
                # Scroll down a few times
                for _ in range(5):
                    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    time.sleep(2)
                    
                    # Scrape visible user links
                    links = page.locator("a[href^='/user/']").all()
                    for link in links:
                        href = link.get_attribute("href")
                        if href:
                            full_url = f"https://www.whatnot.com{href}"
                            sellers.add(full_url)
                    
                    print(f"Found {len(sellers)} unique sellers so far...")
                    if len(sellers) >= target_count:
                        break
            except Exception as e:
                print(f"Error on {cat}: {e}")
                    
        browser.close()
        return list(sellers)

if __name__ == "__main__":
    urls = discover_sellers()
    with open("seller_urls.txt", "w") as f:
        for url in urls:
            f.write(url + "\n")
    print(f"Saved {len(urls)} URLs to seller_urls.txt")
