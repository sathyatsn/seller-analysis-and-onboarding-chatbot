# Whatnot Seller Analysis & Onboarding Chatbot

An AI-powered chatbot system for evaluating and onboarding Whatnot sellers based on comprehensive data analysis including ratings, reviews, sentiment analysis, and social media presence.

## Features

- **Automated Seller Evaluation**: Rule-based onboarding criteria (Rating ≥ 4.9, Reviews ≥ 500)
- **Sentiment Analysis**: Real-time Reddit sentiment tracking from r/whatnotapp
- **LLM-Powered Chatbot**: Natural language interface using OpenAI GPT-4
- **Data Enrichment Pipeline**: Collects 40+ data points per seller including:
  - Reddit mentions and sentiment
  - Listing quality metrics
  - Pricing analysis
  - Social media presence

## Project Structure

```
whatnot_seller_analysis/
├── seller_bot_llm.py          # LLM-powered chatbot (main interface)
├── seller_bot.py              # Rule-based chatbot (legacy)
├── enrich_sellers.py          # Data enrichment pipeline
├── scrape_whatnot.py          # Whatnot data scraper
├── clean_data.py              # Data cleaning utilities
├── generate_report.py         # Report generation
├── clean_seller_data.json     # Cleaned seller dataset
├── enriched_top_5.json        # Enriched data for top candidates
├── onboarding_report.txt      # Comprehensive onboarding report
└── requirements.txt           # Python dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/whatnot-seller-analysis.git
cd whatnot-seller-analysis
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
# Create .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

## Usage

### Run the LLM Chatbot
```bash
python3 seller_bot_llm.py
```

Example queries:
- "Recommend 2 best sellers"
- "What is the sentiment for krakenhits?"
- "Show me sellers with positive reviews"

### Run Data Enrichment
```bash
python3 enrich_sellers.py
```

### Generate Report
```bash
python3 generate_report.py
cat onboarding_report.txt
```

## Onboarding Criteria

- **Minimum Rating**: 4.9/5.0
- **Minimum Reviews**: 500+
- **Sentiment**: Positive community feedback
- **Sales Volume**: High transaction history

## Top 5 Recommended Sellers

1. **krakenhits** - 5.0★, 2.3M sold, 96 Reddit mentions (46% positive)
2. **CollectibleTags** - 5.0★, 186.7K sold, 64 Reddit mentions (55% positive)
3. **wethehobby** - 5.0★, 392.3K sold, 19 Reddit mentions
4. **Gamecorps** - 5.0★, 274.6K sold
5. **drazcollects** - 5.0★, 117.4K sold

## Technologies Used

- **Python 3.14**
- **OpenAI GPT-4** - Natural language processing
- **TextBlob** - Sentiment analysis
- **BeautifulSoup4** - Web scraping
- **Reddit JSON API** - Social media data collection

## Data Sources

- Whatnot.com seller profiles
- Reddit r/whatnotapp community discussions
- Public seller reviews and ratings

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Disclaimer

This tool is for research and evaluation purposes only. Always verify seller credentials independently before making business decisions.
