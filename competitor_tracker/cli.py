"""
Command-line interface for competitor tracking tool.

Provides commands for adding competitors, fetching updates,
generating reports, and managing the tracking system.
"""

import argparse
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime

from .database import CompetitorDB
from .fetcher import NewsFetcher, DataEnricher
from .analyzer import AIAnalyzer
from .reporter import Reporter


class CompetitorTrackerCLI:
    """Command-line interface for the competitor tracker."""

    def __init__(self, config_file: str = "config.yaml"):
        """Initialize CLI with configuration."""
        self.config = self._load_config(config_file)
        self.db = CompetitorDB(self.config.get('database', 'competitors.db'))
        self.fetcher = NewsFetcher(self.config)
        self.enricher = DataEnricher()
        self.analyzer = AIAnalyzer(self.config) if self.config.get('enable_ai') else None
        self.reporter = Reporter(self.db, self.analyzer)

    def _load_config(self, config_file: str) -> dict:
        """Load configuration from YAML file."""
        config_path = Path(config_file)

        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        else:
            # Return default config
            return {
                'database': 'competitors.db',
                'enable_ai': False,
                'ai_provider': 'openai',
                'ai_model': 'gpt-3.5-turbo'
            }

    def add_competitor(self, args):
        """Add a new competitor to track."""
        keywords = args.keywords.split(',') if args.keywords else None

        try:
            comp_id = self.db.add_competitor(
                name=args.name,
                website=args.website,
                description=args.description,
                industry=args.industry,
                tracking_keywords=keywords
            )
            print(f"Competitor added successfully! ID: {comp_id}")
            print(f"Name: {args.name}")
            if args.website:
                print(f"Website: {args.website}")

        except Exception as e:
            print(f"Error adding competitor: {e}")
            sys.exit(1)

    def list_competitors(self, args):
        """List all tracked competitors."""
        competitors = self.db.get_competitors()

        if not competitors:
            print("No competitors found. Add one with 'add' command.")
            return

        print(f"\nTracking {len(competitors)} competitor(s):\n")
        print(f"{'ID':<5} {'Name':<30} {'Website':<40}")
        print("-" * 75)

        for comp in competitors:
            website = comp.get('website', '')[:40] or 'N/A'
            print(f"{comp['id']:<5} {comp['name']:<30} {website:<40}")

        print()

    def fetch_updates(self, args):
        """Fetch updates for competitors."""
        if args.competitor_id:
            competitors = [self.db.get_competitor_by_id(args.competitor_id)]
            if not competitors[0]:
                print(f"Competitor ID {args.competitor_id} not found.")
                return
        else:
            competitors = self.db.get_competitors()

        if not competitors:
            print("No competitors to fetch updates for.")
            return

        total_fetched = 0

        for comp in competitors:
            print(f"\nFetching updates for {comp['name']}...")

            keywords = comp.get('tracking_keywords', [])

            # Fetch news
            news_items = self.fetcher.fetch_competitor_news(
                comp['name'],
                keywords=keywords,
                days_back=args.days,
                max_results=args.max_results
            )

            # Process and store news items
            for item in news_items:
                # Categorize
                category = self.fetcher.categorize_news(
                    item.get('title', ''),
                    item.get('content', '')
                )

                # Analyze sentiment
                sentiment = self.fetcher.analyze_sentiment(
                    f"{item.get('title', '')} {item.get('content', '')}"
                )

                # AI summary if available
                ai_summary = None
                if self.analyzer:
                    ai_summary = self.analyzer.summarize_article(
                        item.get('title', ''),
                        item.get('content', '')
                    )

                # Add to database
                self.db.add_news(
                    competitor_id=comp['id'],
                    title=item.get('title', ''),
                    url=item.get('url'),
                    source=item.get('source'),
                    content=item.get('content'),
                    category=category,
                    sentiment=sentiment,
                    ai_summary=ai_summary,
                    published_at=item.get('published_at')
                )

                total_fetched += 1

            print(f"  Found {len(news_items)} updates")

        print(f"\nTotal updates fetched: {total_fetched}")

    def generate_report(self, args):
        """Generate a report."""
        if args.type == 'daily':
            report = self.reporter.generate_daily_report(
                date=args.date,
                output_format=args.format
            )
        elif args.type == 'weekly':
            report = self.reporter.generate_weekly_report(
                week_start=args.date,
                output_format=args.format
            )
        elif args.type == 'profile':
            if not args.competitor_id:
                print("Error: --competitor-id required for profile report")
                return
            report = self.reporter.generate_competitor_profile(
                args.competitor_id,
                days_back=args.days or 30
            )
        else:
            print(f"Unknown report type: {args.type}")
            return

        # Output report
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)

    def export_data(self, args):
        """Export data to file."""
        if args.format == 'csv':
            self.reporter.export_to_csv(args.output, days_back=args.days)
        elif args.format == 'json':
            self.reporter.export_to_json(args.output, days_back=args.days)
        else:
            print(f"Unknown export format: {args.format}")

    def show_stats(self, args):
        """Show statistics."""
        stats = self.db.get_stats()

        print("\nCompetitor Tracking Statistics")
        print("=" * 60)
        print(f"Total Competitors: {stats['total_competitors']}")
        print(f"Total News Items: {stats['total_news']}")
        print(f"Total Product Changes: {stats['total_product_changes']}")
        print(f"Total Company Updates: {stats['total_company_updates']}")
        print(f"News (Last 24h): {stats['news_last_24h']}")
        print()

    def delete_competitor(self, args):
        """Delete a competitor."""
        comp = self.db.get_competitor_by_id(args.competitor_id)
        if not comp:
            print(f"Competitor ID {args.competitor_id} not found.")
            return

        if not args.force:
            response = input(f"Delete competitor '{comp['name']}' and all data? (yes/no): ")
            if response.lower() != 'yes':
                print("Cancelled.")
                return

        self.db.delete_competitor(args.competitor_id)
        print(f"Competitor '{comp['name']}' deleted.")

    def run(self):
        """Run the CLI."""
        parser = argparse.ArgumentParser(
            description='AI-Powered Competitor Analysis Tool',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Add a competitor
  python -m competitor_tracker add "Acme Corp" --website https://acme.com --industry "Software"

  # List competitors
  python -m competitor_tracker list

  # Fetch updates for all competitors
  python -m competitor_tracker fetch --days 7

  # Generate daily report
  python -m competitor_tracker report daily

  # Generate weekly report in HTML
  python -m competitor_tracker report weekly --format html --output report.html

  # Export data to CSV
  python -m competitor_tracker export data.csv --format csv --days 30
            """
        )

        parser.add_argument('--config', default='config.yaml',
                          help='Configuration file (default: config.yaml)')

        subparsers = parser.add_subparsers(dest='command', help='Commands')

        # Add competitor
        add_parser = subparsers.add_parser('add', help='Add a new competitor')
        add_parser.add_argument('name', help='Competitor name')
        add_parser.add_argument('--website', help='Company website')
        add_parser.add_argument('--description', help='Company description')
        add_parser.add_argument('--industry', help='Industry')
        add_parser.add_argument('--keywords', help='Tracking keywords (comma-separated)')

        # List competitors
        list_parser = subparsers.add_parser('list', help='List all competitors')

        # Fetch updates
        fetch_parser = subparsers.add_parser('fetch', help='Fetch competitor updates')
        fetch_parser.add_argument('--competitor-id', type=int,
                                 help='Fetch for specific competitor (default: all)')
        fetch_parser.add_argument('--days', type=int, default=7,
                                 help='Days to look back (default: 7)')
        fetch_parser.add_argument('--max-results', type=int, default=10,
                                 help='Max results per competitor (default: 10)')

        # Generate report
        report_parser = subparsers.add_parser('report', help='Generate report')
        report_parser.add_argument('type', choices=['daily', 'weekly', 'profile'],
                                  help='Report type')
        report_parser.add_argument('--date', help='Date for report (YYYY-MM-DD)')
        report_parser.add_argument('--format', choices=['text', 'json', 'html'],
                                  default='text', help='Output format')
        report_parser.add_argument('--output', help='Output file (default: stdout)')
        report_parser.add_argument('--competitor-id', type=int,
                                  help='Competitor ID (for profile report)')
        report_parser.add_argument('--days', type=int,
                                  help='Days to include (for profile report)')

        # Export data
        export_parser = subparsers.add_parser('export', help='Export data')
        export_parser.add_argument('output', help='Output file')
        export_parser.add_argument('--format', choices=['csv', 'json'],
                                  default='csv', help='Export format')
        export_parser.add_argument('--days', type=int, default=30,
                                  help='Days to export (default: 30)')

        # Stats
        stats_parser = subparsers.add_parser('stats', help='Show statistics')

        # Delete competitor
        delete_parser = subparsers.add_parser('delete', help='Delete competitor')
        delete_parser.add_argument('competitor_id', type=int, help='Competitor ID')
        delete_parser.add_argument('--force', action='store_true',
                                  help='Skip confirmation')

        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return

        # Execute command
        if args.command == 'add':
            self.add_competitor(args)
        elif args.command == 'list':
            self.list_competitors(args)
        elif args.command == 'fetch':
            self.fetch_updates(args)
        elif args.command == 'report':
            self.generate_report(args)
        elif args.command == 'export':
            self.export_data(args)
        elif args.command == 'stats':
            self.show_stats(args)
        elif args.command == 'delete':
            self.delete_competitor(args)


def main():
    """Main entry point."""
    cli = CompetitorTrackerCLI()
    cli.run()


if __name__ == '__main__':
    main()
