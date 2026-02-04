
import json
import os

# --- Onboarding Thresholds ---
# User Rules: Rating >= 4.9 AND Reviews > 500
MIN_RATING = 4.9
MIN_SOLD = 100 # Kept as baseline
MIN_REVIEWS = 500

def load_data(filename):
    if not os.path.exists(filename):
        print(f"Error: {filename} not found.")
        return []
    with open(filename, 'r') as f:
        return json.load(f)

def parse_number(s):
    if not s or s == "N/A":
        return 0
    s = str(s).strip().upper()
    multiplier = 1
    if s.endswith('K'):
        multiplier = 1000
        s = s[:-1]
    elif s.endswith('M'):
        multiplier = 1000000
        s = s[:-1]
    
    try:
        val = float(s.replace('<', '').replace('>', ''))
        return val * multiplier
    except ValueError:
        return 0

def evaluate_seller(seller):
    rating = seller.get('Seller Rating')
    sold_raw = seller.get('Sold', '0')
    reviews_raw = seller.get('Reviews', '0')
    
    sold_count = parse_number(sold_raw)
    review_count = parse_number(reviews_raw)
    
    reasons = []
    
    # Rating Check
    if rating < MIN_RATING:
        reasons.append(f"Rating {rating} is below {MIN_RATING}")
        
    # Sales Check
    if sold_count < MIN_SOLD:
        reasons.append(f"Sales volume ({sold_raw}) is too low (< {MIN_SOLD})")
        
    # Reviews Check
    if review_count < MIN_REVIEWS:
        reasons.append(f"Review count ({reviews_raw}) is too low (< {MIN_REVIEWS})")

    is_approved = len(reasons) == 0
    return is_approved, reasons, rating, sold_raw, reviews_raw

def main():
    print("Loading seller data...")
    sellers = load_data('clean_seller_data.json')
    seller_map = {s['UserID'].lower(): s for s in sellers}
    seller_map.update({s['UserName'].lower(): s for s in sellers}) # Allow searching by Display Name

    print(f"\n--- 🤖 Seller Onboarding Chatbot ---")
    print(f"Criteria: Rating >= {MIN_RATING} | Reviews >= {MIN_REVIEWS}")
    print("Type a username, or try 'Who is the best seller?'")

    # --- MEMORY STATE ---
    last_explanation = None
    # --------------------

    while True:
        query = input("\n> ").strip()
        if query.lower() in ['q', 'quit', 'exit']:
            print("Goodbye!")
            break
        
        if not query:
            continue
        
        # --- Smart Query Parser ---
        q_lower = query.lower()

        # 0. Context Handler (Why?)
        if any(w in q_lower for w in ['why', 'reason', 'explain', 'how come']):
            if last_explanation:
                print("\n🤖 CONTEXTUAL ANSWER:")
                print(last_explanation)
            else:
                print("❌ I haven't made a recommendation yet, so I can't explain 'why'.")
                print("   Try asking for a recommendation first!")
            continue

        # Detect "Best" or "One" recommender (Prioritize this!)
        if any(w in q_lower for w in ['best seller', 'recommend one', 'give me one', 'best one', 'recommend only one', 'answer']):
            # Filter first
            candidates = []
            for s in sellers:
                is_ok, _, rating_val, sold_str, reviews_str = evaluate_seller(s)
                if is_ok:
                    # Enrich with numeric values for sorting
                    s['_rating_num'] = rating_val
                    s['_sold_num'] = parse_number(sold_str)
                    s['_reviews_num'] = parse_number(reviews_str)
                    candidates.append(s)
            
            if not candidates:
                 print(f"❌ No sellers meet the strict criteria (Rating >= {MIN_RATING}, Reviews >= {MIN_REVIEWS})")
                 continue

            # Sort by Rating (Desc) then Sold (Desc)
            best_seller = sorted(candidates, key=lambda x: (x['_rating_num'], x['_sold_num']), reverse=True)[0]
            
            # SAVE CONTEXT
            last_explanation = (
                f"I recommended {best_seller['UserName']} because:\n"
                f"1. They satisfy the strict filtering (Rating >= {MIN_RATING}, Reviews >= {MIN_REVIEWS}).\n"
                f"2. I sorted all qualified candidates by Rating (they have {best_seller['Seller Rating']}).\n"
                f"3. I used Sales Volume as the tie-breaker for top ratings.\n"
                f"   {best_seller['UserName']} has {best_seller['Sold']} sales, which was the highest among the elite group."
            )

            print(f"\n🥇 THE #1 RECOMMENDED SELLER")
            print("=" * 50)
            print(f"User:     {best_seller['UserName']} (@{best_seller['UserID']})")
            print(f"Rating:   {best_seller['Seller Rating']} ★")
            print(f"Sold:     {best_seller['Sold']}")
            print(f"Reviews:  {best_seller['Reviews']}")
            print("=" * 50)
            print("🧐 WHY THIS USER?")
            print(f"1. They have a Perfect (or near-perfect) Rating of {best_seller['Seller Rating']}.")
            print(f"2. Among those with top ratings, they have the HIGHEST sales volume ({best_seller['Sold']}).")
            print("   This indicates they manage huge volume without compromising quality.")
            print("=" * 50)
            continue
        
        # Detect "Top X" or "Best X" intent (Leaderboard)
        if any(w in q_lower for w in ['top', 'best', 'most', 'worst', 'sort']):
            
            # 1. Determine Metric
            metric_key = 'Seller Rating' # Default
            metric_name = "Rating"
            reverse_sort = True
            
            if 'sold' in q_lower or 'sales' in q_lower:
                metric_key = 'Sold'
                metric_name = "Items Sold"
            elif 'review' in q_lower:
                metric_key = 'Reviews'
                metric_name = "Review Count"
            elif 'rating' in q_lower:
                metric_key = 'Seller Rating'
                metric_name = "Rating"
            
            # 2. Determine Count (N)
            count = 10 # Default
            import re
            numbers = re.findall(r'\d+', q_lower)
            if numbers:
                count = int(numbers[0])
            
            # SAVE CONTEXT
            last_explanation = (
                f"I showed you the Top {count} users sorted by {metric_name}.\n"
                f"I looked at the '{metric_key}' field for all users and ordered them descending."
            )

            # 3. Sort and Slice
            # Helper to get sort value safely
            def get_sort_val(s):
                val = s.get(metric_key)
                if metric_key in ['Sold', 'Reviews']:
                    return parse_number(val)
                # For Rating, ensure numeric
                try:
                    return float(val) if val else 0
                except:
                    return 0

            sorted_sellers = sorted(sellers, key=get_sort_val, reverse=reverse_sort)
            top_n = sorted_sellers[:count]
            
            # 4. Display Leaderboard
            print(f"\n🏆 TOP {count} BY {metric_name.upper()}")
            print(f"{'#':<4} {'User':<25} {'Metric':<15}")
            print("-" * 45)
            for i, s in enumerate(top_n, 1):
                val = s.get(metric_key, 'N/A')
                print(f"{i:<4} {s['UserName'][:24]:<25} {val:<15}")
            print("-" * 45)
            continue



        # Detect "Onboarding" or "Recommend" intent (Show ALL approved)
        if any(w in q_lower for w in ['recommend', 'onboard', 'approved', 'good sellers', 'qualify']):
            print(f"\n✨ RECOMMENDED SELLERS (Rating >= {MIN_RATING}, Reviews >= {MIN_REVIEWS})")
            print(f"{'User':<25} {'Rating':<8} {'Reviews':<10} {'Sold'}")
            print("-" * 60)
            
            approved_count = 0
            for s in sellers:
                is_ok, _, r, so, rev = evaluate_seller(s)
                if is_ok:
                    approved_count += 1
                    print(f"{s['UserName'][:24]:<25} {r:<8} {rev:<10} {so}")
            
            # SAVE CONTEXT
            last_explanation = (
                f"I listed all sellers that matched your strict Onboarding Criteria:\n"
                f"- Rating must be {MIN_RATING} or higher.\n"
                f"- Review count must be {MIN_REVIEWS} or higher.\n"
                f"Found {approved_count} sellers fitting this description."
            )

            if approved_count == 0:
                print("No sellers found meeting strict criteria.")
            else:
                print(f"\nTotal Approved: {approved_count}")
            print("-" * 60)
            continue

        seller = seller_map.get(query.lower())
        
        if not seller:
            # Try partial match if exact match fails
            matches = [s for name, s in seller_map.items() if query.lower() in name]
            if matches:
                print(f"❓ User '{query}' not found exactly. Did you mean one of these?")
                seen = set()
                count = 0
                for m in matches:
                     uname = m['UserName']
                     uid = m['UserID']
                     if uid in seen: continue
                     seen.add(uid)
                     print(f"   - {uname} ({uid})")
                     count += 1
                     if count >= 3: break
            else:
                print(f"❌ User '{query}' not found in database.")
            continue

        # Evaluation
        approved, reasons, rating, sold, reviews = evaluate_seller(seller)
        
        print("\n-------------------------------------")
        print(f"👤 Seller: {seller['UserName']} (@{seller['UserID']})")
        print(f"📊 Stats:  Rating: {rating} ★ | Sold: {sold} | Reviews: {reviews}")
        
        if approved:
             print(f"✅ RESULT: APPROVED FOR ONBOARDING")
             print("   Performance meets all high-quality standards.")
        else:
             print(f"❌ RESULT: NOT APPROVED")
             print("   Reasons:")
             for r in reasons:
                 print(f"   - {r}")
        print("-------------------------------------")

if __name__ == "__main__":
    main()
