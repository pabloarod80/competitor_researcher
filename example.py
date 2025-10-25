#!/usr/bin/env python3
"""
Example script demonstrating programmatic usage of the competitor tracker.

This shows how to use the modules directly in your own Python scripts.
"""

from competitor_tracker.database import CompetitorDB
from competitor_tracker.fetcher import NewsFetcher, DataEnricher
from competitor_tracker.analyzer import AIAnalyzer
from competitor_tracker.reporter import Reporter


def main():
    """Example usage of the competitor tracker."""

    # Initialize components
    print("Initializing competitor tracker...")
    db = CompetitorDB("example_competitors.db")

    # Configuration (you can load from config.yaml)
    config = {
        'enable_ai': False,  # Set to True if you have API keys
        'newsapi_key': None,  # Add your NewsAPI key here if available
    }

    fetcher = NewsFetcher(config)
    enricher = DataEnricher()
    analyzer = AIAnalyzer(config) if config.get('enable_ai') else None
    reporter = Reporter(db, analyzer)

    # Add some example competitors
    print("\nAdding competitors...")

    competitors = [
        {
            'name': 'OpenAI',
            'website': 'https://openai.com',
            'industry': 'Artificial Intelligence',
            'description': 'AI research and deployment company',
            'tracking_keywords': ['GPT', 'ChatGPT', 'AI model', 'machine learning']
        },
        {
            'name': 'Anthropic',
            'website': 'https://anthropic.com',
            'industry': 'Artificial Intelligence',
            'description': 'AI safety and research company',
            'tracking_keywords': ['Claude', 'AI safety', 'constitutional AI']
        },
        {
            'name': 'Google DeepMind',
            'website': 'https://deepmind.google',
            'industry': 'Artificial Intelligence',
            'description': 'AI research laboratory',
            'tracking_keywords': ['Gemini', 'AlphaGo', 'deep learning']
        }
    ]

    for comp_data in competitors:
        try:
            comp_id = db.add_competitor(
                name=comp_data['name'],
                website=comp_data['website'],
                industry=comp_data['industry'],
                description=comp_data['description'],
                tracking_keywords=comp_data['tracking_keywords']
            )
            print(f"  Added: {comp_data['name']} (ID: {comp_id})")
        except Exception as e:
            print(f"  Skipped {comp_data['name']} (already exists or error: {e})")

    # List all competitors
    print("\nTracked Competitors:")
    all_competitors = db.get_competitors()
    for comp in all_competitors:
        print(f"  - {comp['name']} (ID: {comp['id']})")

    # Fetch news for one competitor
    print("\nFetching recent news for OpenAI...")
    openai_comp = next((c for c in all_competitors if c['name'] == 'OpenAI'), None)

    if openai_comp:
        news_items = fetcher.fetch_competitor_news(
            competitor_name=openai_comp['name'],
            keywords=openai_comp.get('tracking_keywords'),
            days_back=7,
            max_results=5
        )

        print(f"Found {len(news_items)} news items")

        # Store news items
        for item in news_items:
            category = fetcher.categorize_news(
                item.get('title', ''),
                item.get('content', '')
            )

            sentiment = fetcher.analyze_sentiment(
                f"{item.get('title', '')} {item.get('content', '')}"
            )

            # AI summary if available
            ai_summary = None
            if analyzer:
                ai_summary = analyzer.summarize_article(
                    item.get('title', ''),
                    item.get('content', '')
                )

            db.add_news(
                competitor_id=openai_comp['id'],
                title=item.get('title', ''),
                url=item.get('url'),
                source=item.get('source'),
                content=item.get('content'),
                category=category,
                sentiment=sentiment,
                ai_summary=ai_summary,
                published_at=item.get('published_at')
            )

        print("\nLatest news items:")
        for i, item in enumerate(news_items[:3], 1):
            print(f"\n{i}. {item['title']}")
            print(f"   Source: {item.get('source', 'Unknown')}")
            if item.get('url'):
                print(f"   URL: {item['url']}")

    # Generate a daily report
    print("\n" + "=" * 60)
    print("DAILY REPORT")
    print("=" * 60)
    daily_report = reporter.generate_daily_report(output_format='text')
    print(daily_report)

    # Show statistics
    print("\n" + "=" * 60)
    print("STATISTICS")
    print("=" * 60)
    stats = db.get_stats()
    print(f"Total Competitors: {stats['total_competitors']}")
    print(f"Total News Items: {stats['total_news']}")
    print(f"News (Last 24h): {stats['news_last_24h']}")

    # Export data
    print("\nExporting data...")
    reporter.export_to_json("example_export.json", days_back=7)
    reporter.export_to_csv("example_export.csv", days_back=7)

    print("\nExample complete!")
    print("Check example_competitors.db, example_export.json, and example_export.csv")

    # Clean up
    db.close()


if __name__ == '__main__':
    main()
