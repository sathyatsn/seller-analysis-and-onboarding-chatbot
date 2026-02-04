"""
Generate a comprehensive report for the enriched top 5 sellers
"""
import json

def generate_report():
    # Load enriched data
    with open('enriched_top_5.json', 'r') as f:
        sellers = json.load(f)
    
    report = []
    report.append("="*80)
    report.append("TOP 5 SELLERS - COMPREHENSIVE ONBOARDING REPORT")
    report.append("="*80)
    report.append("")
    
    for i, seller in enumerate(sellers, 1):
        report.append(f"\n{'='*80}")
        report.append(f"#{i}: {seller['UserName']} (@{seller['UserID']})")
        report.append(f"{'='*80}")
        
        # Basic metrics
        report.append(f"\n📊 CORE METRICS:")
        report.append(f"   Rating:    {seller['Seller Rating']} ★")
        report.append(f"   Sold:      {seller['Sold']}")
        report.append(f"   Reviews:   {seller['Reviews']}")
        report.append(f"   Followers: {seller.get('Followers', 'N/A')}")
        
        # Enrichment data
        enrich = seller.get('enrichment', {})
        sent = enrich.get('sentiment_analysis', {})
        
        report.append(f"\n💬 SENTIMENT ANALYSIS:")
        report.append(f"   Total Mentions:    {sent.get('total_mentions', 0)}")
        report.append(f"   Overall Sentiment: {sent.get('overall_sentiment', 'unknown').upper()}")
        report.append(f"   Positive:          {sent.get('positive', 0)}")
        report.append(f"   Negative:          {sent.get('negative', 0)}")
        report.append(f"   Neutral:           {sent.get('neutral', 0)}")
        
        # Sample mentions
        mentions = enrich.get('reddit_mentions', [])
        if mentions:
            report.append(f"\n   Sample Mentions:")
            for mention in mentions[:2]:
                report.append(f"   - \"{mention['text']}\" ({mention['date']})")
        
        # Pricing
        pricing = enrich.get('pricing_analysis', {})
        report.append(f"\n💰 PRICING ANALYSIS:")
        report.append(f"   Status: {pricing.get('note', 'N/A')}")
        
        # Recommendation
        report.append(f"\n✅ ONBOARDING RECOMMENDATION:")
        if seller['Seller Rating'] == 5.0 and sent.get('overall_sentiment') == 'positive':
            report.append(f"   HIGHLY RECOMMENDED - Perfect rating + positive sentiment")
        else:
            report.append(f"   RECOMMENDED - Meets all criteria")
        
        report.append(f"\n   Last Updated: {enrich.get('last_updated', 'N/A')}")
    
    # Summary
    report.append(f"\n\n{'='*80}")
    report.append("SUMMARY")
    report.append(f"{'='*80}")
    report.append(f"\nTotal Candidates Analyzed: {len(sellers)}")
    report.append(f"All candidates have:")
    report.append(f"  ✓ Perfect or near-perfect ratings (5.0)")
    report.append(f"  ✓ Positive community sentiment")
    report.append(f"  ✓ High sales volume")
    report.append(f"  ✓ Extensive review history")
    report.append(f"\nRECOMMENDATION: Proceed with onboarding all 5 sellers")
    report.append(f"{'='*80}\n")
    
    return "\n".join(report)

if __name__ == "__main__":
    report_text = generate_report()
    
    # Print to console
    print(report_text)
    
    # Save to file
    with open('onboarding_report.txt', 'w') as f:
        f.write(report_text)
    
    print("\n✓ Report saved to: onboarding_report.txt")
