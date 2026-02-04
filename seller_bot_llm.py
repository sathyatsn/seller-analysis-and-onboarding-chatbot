import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# --- Onboarding Thresholds ---
MIN_RATING = 4.9
MIN_REVIEWS = 500

def load_seller_data():
    """Load and return the clean seller data, merged with enrichment data where available"""
    # Load base data
    with open('clean_seller_data.json', 'r') as f:
        sellers = json.load(f)
    
    # Load enriched data if available
    try:
        with open('enriched_top_5.json', 'r') as f:
            enriched_list = json.load(f)
            # Create a map for easy lookup
            enriched_map = {s['UserID']: s.get('enrichment') for s in enriched_list}
            
            # Merge enrichment into main list
            for s in sellers:
                if s['UserID'] in enriched_map:
                    s['enrichment'] = enriched_map[s['UserID']]
    except FileNotFoundError:
        print("Warning: enriched_top_5.json not found. enrichment data will be missing.")

    return sellers

def create_system_prompt(sellers):
    """Create a system prompt that explains the data and rules to the LLM"""
    return f"""You are an intelligent seller onboarding assistant. You have access to a dataset of {len(sellers)} Whatnot sellers.

ONBOARDING CRITERIA:
- Rating must be >= {MIN_RATING}
- Reviews must be >= {MIN_REVIEWS}

DATASET STRUCTURE:
Each seller has: UserID, UserName, Seller Rating, Reviews, Sold.
SOME sellers (the top candidates) have an 'enrichment' field containing:
- 'reddit_mentions': List of Reddit comments
- 'sentiment_analysis': Positive/Negative scores
- 'pricing_analysis': Competitive status and estimated range
- 'listing_quality': Score (e.g. 9.5/10) and details

YOUR CAPABILITIES:
1. Answer ANY question about the sellers
2. Recommend sellers based on flexible criteria
3. Explain your reasoning clearly
4. **Answer questions about Sentiment, Social Media, Listing Quality, and Pricing** using the 'enrichment' data if available.

IMPORTANT RULES:
- If a user asks about social media/sentiment for a seller WITHOUT enrichment data, say "I don't have deeper analytics for that specific seller yet, only the top candidates."
- If asked for N sellers, return EXACTLY N sellers
- Always explain WHY you chose specific sellers

SELLER DATA (JSON):
{json.dumps(sellers, indent=2)}

Remember: Be helpful, accurate, and conversational."""

def chat_with_llm(messages):
    """Send messages to OpenAI and get a response"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using gpt-4o-mini for cost efficiency
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error communicating with OpenAI: {str(e)}\nPlease check your API key in the .env file."

def main():
    print("Loading seller data...")
    sellers = load_seller_data()
    
    # Initialize conversation history
    conversation_history = [
        {"role": "system", "content": create_system_prompt(sellers)}
    ]
    
    print("\n--- 🤖 AI-Powered Seller Onboarding Assistant ---")
    print(f"Criteria: Rating >= {MIN_RATING} | Reviews >= {MIN_REVIEWS}")
    print("Ask me anything about the sellers! (Type 'quit' to exit)\n")
    
    while True:
        user_input = input("> ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Add user message to history
        conversation_history.append({"role": "user", "content": user_input})
        
        # Get AI response
        response = chat_with_llm(conversation_history)
        
        # Add assistant response to history
        conversation_history.append({"role": "assistant", "content": response})
        
        # Print response
        print(f"\n{response}\n")

if __name__ == "__main__":
    main()
