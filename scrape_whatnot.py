import re
import time
import pandas as pd
from playwright.sync_api import sync_playwright

def clean_number(text):
    """Converts 3.2K to 3200, 1.5M to 1500000, etc."""
    if not text:
        return 0
    text = text.upper().replace(',', '').strip()
    if 'K' in text:
        return int(float(text.replace('K', '')) * 1000)
    if 'M' in text:
        return int(float(text.replace('M', '')) * 1000000)
    try:
        return float(text)
    except ValueError:
        return 0

def get_profile_data(page, url):
    """Extracts data from a single seller profile."""
    try:
        print(f"Scraping {url}...")
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(2)  # Wait for dynamic content

        # Extract UserID from URL
        user_id = url.split('/')[-1]

        # Selectors based on research
        # Note: These are heuristic based on the previous analysis
        # We look for specific text patterns if classes are unstable, but try structure first.

        # UserName
        try:
            username = page.locator("div.flex.flex-col.justify-center > div.text-body1").first.inner_text()
        except:
            username = "N/A"

        # Stats Container
        # We can find stats by searching for the text labels
        
        # Rating
        rating = 0.0
        try:
           # Look for the star icon's sibling or text like "4.9"
           # Often it's at the top. Let's look for text that matches a rating pattern
           rating_text = page.locator("text=/^\\d\\.\\d$/").first.inner_text()
           rating = float(rating_text)
        except:
            pass
            
        # If regex locator fails, try broader
        if rating == 0.0:
             # Fallback: finding the reviews and looking near it
             pass

        # Reviews
        reviews_count = 0
        try:
            reviews_text = page.locator("span", has_text=re.compile(r"Reviews")).first.inner_text()
            # extract number "3.2K Reviews" -> "3.2K"
            reviews_clean = reviews_text.split()[0]
            reviews_count = clean_number(reviews_clean) # Keep raw if needed? Request said "3.2K" format in output, but we need to filter?
            # Actually user wants output format: "3.2K". Filtering is on rating.
            # But the table example shows specific formats. I should store raw for display and clean for logic if needed?
            # The request asks for output format similar to "3.2K".
            # I will store the display string but might need value for sorting if "Top Performing" implies sorting.
            # User asks: "identify the top performing seller" -> implies sorting by Sales or Followers?
            # "Get any 100 sellers data... user with rating less than 4.9 please eliminate"
            
            # Let's clean later, just get text for now
            reviews_str = reviews_clean
        except:
            reviews_str = "0"
        
        # Avg Ship
        try:
            ship_text = page.locator("span", has_text=re.compile(r"Avg Ship")).first.inner_text()
            ship_str = ship_text.split()[0] + "d" if 'Avg' in ship_text else ship_text
            # Usually "1d Avg Ship"
            ship_str = ship_text.replace(" Avg Ship", "")
        except:
            ship_str = "N/A"

        # Sold
        try:
            sold_text = page.locator("span", has_text=re.compile(r"Sold")).first.inner_text()
            sold_str = sold_text.replace(" Sold", "")
        except:
            sold_str = "0"

        # Following
        try:
            # Locate button with Strong text "Following"
            following_btn = page.locator("button", has_text="Following").first
            following_str = following_btn.locator("strong").first.inner_text()
        except:
            following_str = "0"

        # Followers
        try:
            followers_btn = page.locator("button", has_text="Followers").first
            followers_str = followers_btn.locator("strong").first.inner_text()
        except:
            followers_str = "0"
            
        
        # Refine Rating extraction if missed
        if rating == 0.0:
             # Try to find the element before 'Reviews' if they are siblings?
             pass

        return {
            "UserID": user_id,
            "UserName": username,
            "Seller Rating": rating,
            "Reviews": reviews_str,
            "Average Ship": ship_str,
            "Sold": sold_str,
            "Following": following_str,
            "Followers": followers_str,
            "RawRating": rating # For filtering
        }

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def discover_sellers(page, target_count=150):
    """Discovers seller URLs from category pages."""
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
                
    return list(sellers)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) # Headless=False to avoid detection sometimes
        context = browser.new_context()
        page = context.new_page()

        print("Discovering sellers...")
        seller_urls = discover_sellers(page, target_count=150)
        
        data = []
        for i, url in enumerate(seller_urls):
            print(f"Processing {i+1}/{len(seller_urls)}: {url}")
            profile = get_profile_data(page, url)
            
            if profile:
                # Filter by rating
                # Note: some ratings might be "New" or missing
                try:
                    r = float(profile["Seller Rating"])
                    if r >= 4.9:
                        print(f"  -> Keeping (Rating: {r})")
                        data.append(profile)
                    else:
                        print(f"  -> Skipping (Rating: {r} < 4.9)")
                except:
                     print("  -> Skipping (Invalid Rating)")

            if len(data) >= 100:
                print("Reached 100 qualified sellers!")
                break
        
        browser.close()

    # Save to files
    if data:
        df = pd.DataFrame(data)
        # Drop raw rating column used for filtering
        df_final = df.drop(columns=["RawRating"])
        
        # Reorder columns
        cols = ["UserID", "UserName", "Seller Rating", "Reviews", "Average Ship", "Sold", "Following", "Followers"]
        df_final = df_final[cols]
        
        df_final.to_csv("whatnot_top_sellers.csv", index=False)
        df_final.to_json("whatnot_top_sellers.json", orient="records", indent=2)
        print("Data saved to whatnot_top_sellers.csv and whatnot_top_sellers.json")
    else:
        print("No data collected.")

if __name__ == "__main__":
    main()
