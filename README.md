# Seller Analysis and Onboarding Chatbot

A smart chatbot that helps you find and evaluate the best sellers on Whatnot. This project uses AI to analyze seller data, read community feedback from Reddit, and give you recommendations on which sellers to work with.

**Built for Whatnot** - This entire project was created specifically for analyzing Whatnot sellers and making better onboarding decisions.

## The Business Problem

When onboarding new sellers to a marketplace, you face several challenges:

- **Time-consuming manual research** - Checking each seller's profile, reviews, and reputation takes hours
- **Inconsistent evaluation** - Different people might judge sellers differently
- **Missing community insights** - Hard to know what real users are saying on social media
- **Scale issues** - Can't efficiently evaluate hundreds of potential sellers

**This project solves these problems** by automating the entire seller evaluation process. Instead of spending hours per seller, you get comprehensive reports with data-driven recommendations in minutes.

## What Does This Do?

Think of this as your personal assistant for seller research. Instead of manually checking hundreds of seller profiles, this tool:

1. **Collects seller data** from Whatnot (ratings, sales, reviews)
2. **Reads Reddit discussions** to see what people are saying about sellers
3. **Analyzes sentiment** - Are people happy or unhappy with this seller?
4. **Gives you recommendations** - Which sellers meet your quality standards?
5. **Lets you ask questions** - Just chat with the bot like "Who are the top 3 sellers?"

## Why I Built This

I needed a faster way to evaluate Whatnot sellers for onboarding. Instead of spending hours researching each seller manually, this tool does it automatically and gives me detailed reports with real community feedback.

## What You Need

- Python 3 installed on your computer
- An OpenAI API key (for the chatbot brain)
- Internet connection (to scrape data)

## How to Set It Up

**Step 1: Download the code**
```bash
git clone https://github.com/YOUR_USERNAME/whatnot-seller-analysis.git
cd whatnot-seller-analysis
```

**Step 2: Install required libraries**
```bash
pip3 install -r requirements.txt
```

**Step 3: Add your OpenAI API key**
Create a file called `.env` and add:
```
OPENAI_API_KEY=your_key_here
```

## How to Use It

### Talk to the Chatbot
```bash
python3 seller_bot_llm.py
```

Then ask questions like:
- "Show me the best 5 sellers"
- "What do people say about krakenhits on Reddit?"
- "Which sellers have the most sales?"

### Get a Full Report
```bash
python3 enrich_sellers.py
python3 generate_report.py
cat onboarding_report.txt
```

This creates a detailed report with sentiment analysis for the top sellers.

## What Makes a Good Seller?

The tool looks for sellers with:
- ⭐ **Rating**: 4.9 or higher (out of 5)
- 💬 **Reviews**: At least 500 reviews
- 😊 **Positive sentiment**: Good feedback on Reddit
- 📈 **High sales**: Proven track record

## Top Sellers Found

Based on my analysis, here are the top 5 Whatnot sellers:

1. **krakenhits** - Perfect 5.0 rating, 2.3M items sold, 96 Reddit mentions
2. **CollectibleTags** - Perfect 5.0 rating, 186K items sold, 64 Reddit mentions  
3. **wethehobby** - Perfect 5.0 rating, 392K items sold
4. **Gamecorps** - Perfect 5.0 rating, 274K items sold
5. **drazcollects** - Perfect 5.0 rating, 117K items sold

## How It Works Behind the Scenes

1. **Data Collection**: Scrapes Whatnot seller profiles
2. **Reddit Analysis**: Searches r/whatnotapp for mentions of each seller
3. **Sentiment Analysis**: Uses AI to determine if comments are positive, negative, or neutral
4. **Smart Chatbot**: Uses GPT-4 to answer your questions in plain English
5. **Report Generation**: Creates easy-to-read reports with all the data

## Tech Stack (For the Curious)

- Python 3.14
- OpenAI GPT-4 (the chatbot brain)
- TextBlob (sentiment analysis)
- BeautifulSoup (web scraping)
- Reddit's public API (no login needed)

## Important Notes

- ⚠️ This is for research only - always do your own verification
- 🔒 Your API key stays private (it's in `.gitignore`)
- 📊 Data files are excluded from GitHub for privacy
- 🤖 The chatbot needs internet to work

## Questions?

Feel free to open an issue or reach out if you have questions about using this tool!

## License

MIT License - feel free to use and modify for your own projects.
