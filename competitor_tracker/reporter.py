"""
Reporting module for competitor tracking.

Generates various types of reports: daily briefings, weekly summaries,
competitor profiles, and export capabilities.
"""

import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path


class Reporter:
    """Generates reports and exports for competitor tracking data."""

    def __init__(self, db, analyzer=None):
        """
        Initialize reporter with database and optional AI analyzer.

        Args:
            db: Database instance
            analyzer: Optional AI analyzer for enhanced reports
        """
        self.db = db
        self.analyzer = analyzer

    def generate_daily_report(self, date: str = None,
                             output_format: str = 'text') -> str:
        """
        Generate daily report of competitor updates.

        Args:
            date: Date for report (YYYY-MM-DD), defaults to today
            output_format: 'text', 'json', or 'html'

        Returns:
            Formatted report string
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        # Get updates for the day
        start_time = f"{date} 00:00:00"
        end_time = f"{date} 23:59:59"

        updates = self.db.get_recent_updates(days=1)

        if output_format == 'json':
            return json.dumps({
                'date': date,
                'updates': updates
            }, indent=2)

        elif output_format == 'html':
            return self._generate_html_report(updates, date, 'daily')

        else:  # text format
            if self.analyzer:
                return self.analyzer.generate_daily_briefing(updates, date)
            else:
                return self._generate_text_report(updates, date, 'daily')

    def generate_weekly_report(self, week_start: str = None,
                              output_format: str = 'text') -> str:
        """
        Generate weekly report with trends and insights.

        Args:
            week_start: Start date of week (YYYY-MM-DD)
            output_format: 'text', 'json', or 'html'

        Returns:
            Formatted report string
        """
        if not week_start:
            # Get Monday of current week
            today = datetime.now()
            week_start = (today - timedelta(days=today.weekday())).strftime('%Y-%m-%d')

        # Get updates for the week
        updates = self.db.get_recent_updates(days=7)

        if output_format == 'json':
            return json.dumps({
                'week_start': week_start,
                'updates': updates
            }, indent=2)

        elif output_format == 'html':
            return self._generate_html_report(updates, week_start, 'weekly')

        else:  # text format
            if self.analyzer:
                return self.analyzer.generate_weekly_report(updates, week_start)
            else:
                return self._generate_text_report(updates, week_start, 'weekly')

    def generate_competitor_profile(self, competitor_id: int,
                                   days_back: int = 30) -> str:
        """
        Generate a detailed profile for a specific competitor.

        Args:
            competitor_id: ID of the competitor
            days_back: Number of days of history to include

        Returns:
            Formatted competitor profile
        """
        competitor = self.db.get_competitor_by_id(competitor_id)
        if not competitor:
            return f"Competitor ID {competitor_id} not found."

        updates = self.db.get_recent_updates(days=days_back, competitor_id=competitor_id)

        profile = f"COMPETITOR PROFILE: {competitor['name']}\n"
        profile += "=" * 60 + "\n\n"

        # Basic info
        profile += "COMPANY INFORMATION\n"
        profile += "-" * 60 + "\n"
        profile += f"Name: {competitor['name']}\n"
        if competitor.get('website'):
            profile += f"Website: {competitor['website']}\n"
        if competitor.get('industry'):
            profile += f"Industry: {competitor['industry']}\n"
        if competitor.get('headquarters'):
            profile += f"Headquarters: {competitor['headquarters']}\n"
        if competitor.get('employee_count'):
            profile += f"Employees: {competitor['employee_count']}\n"
        if competitor.get('description'):
            profile += f"\nDescription:\n{competitor['description']}\n"
        profile += "\n"

        # Activity summary
        news_count = len(updates.get('news', []))
        product_count = len(updates.get('product_changes', []))
        company_count = len(updates.get('company_updates', []))

        profile += f"ACTIVITY SUMMARY (Last {days_back} days)\n"
        profile += "-" * 60 + "\n"
        profile += f"News Articles: {news_count}\n"
        profile += f"Product Changes: {product_count}\n"
        profile += f"Company Updates: {company_count}\n"
        profile += f"Total Updates: {news_count + product_count + company_count}\n\n"

        # Recent activity
        if updates.get('news'):
            profile += "RECENT NEWS\n"
            profile += "-" * 60 + "\n"
            for item in updates['news'][:5]:
                profile += f"\n• {item['title']}\n"
                if item.get('ai_summary'):
                    profile += f"  {item['ai_summary']}\n"
                profile += f"  Source: {item.get('source', 'Unknown')}\n"
                if item.get('url'):
                    profile += f"  URL: {item['url']}\n"
            profile += "\n"

        # Competitive analysis
        if self.analyzer and updates:
            profile += "COMPETITIVE ANALYSIS\n"
            profile += "-" * 60 + "\n"
            analysis = self.analyzer.analyze_competitive_impact(
                updates.get('news', []),
                competitor['name']
            )
            profile += f"Threat Level: {analysis.get('threat_level', 'unknown').upper()}\n\n"

            if analysis.get('key_insights'):
                profile += "Key Insights:\n"
                for insight in analysis['key_insights']:
                    profile += f"  • {insight}\n"
                profile += "\n"

            if analysis.get('recommendations'):
                profile += "Recommendations:\n"
                for rec in analysis['recommendations']:
                    profile += f"  • {rec}\n"
                profile += "\n"

        return profile

    def export_to_csv(self, output_file: str, days_back: int = 30):
        """
        Export competitor data to CSV file.

        Args:
            output_file: Path to output CSV file
            days_back: Number of days of data to export
        """
        updates = self.db.get_recent_updates(days=days_back)

        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Write header
            writer.writerow([
                'Date', 'Competitor', 'Type', 'Title', 'Category',
                'Sentiment', 'Source', 'URL', 'Summary'
            ])

            # Write news items
            for item in updates.get('news', []):
                writer.writerow([
                    item.get('fetched_at', ''),
                    item.get('competitor_name', ''),
                    'News',
                    item.get('title', ''),
                    item.get('category', ''),
                    item.get('sentiment', ''),
                    item.get('source', ''),
                    item.get('url', ''),
                    item.get('ai_summary', '')
                ])

            # Write product changes
            for item in updates.get('product_changes', []):
                writer.writerow([
                    item.get('detected_at', ''),
                    item.get('competitor_name', ''),
                    'Product Change',
                    item.get('product_name', ''),
                    item.get('change_type', ''),
                    '',
                    '',
                    item.get('source_url', ''),
                    item.get('description', '')
                ])

            # Write company updates
            for item in updates.get('company_updates', []):
                writer.writerow([
                    item.get('created_at', ''),
                    item.get('competitor_name', ''),
                    'Company Update',
                    item.get('title', ''),
                    item.get('update_type', ''),
                    '',
                    '',
                    item.get('source_url', ''),
                    item.get('ai_analysis', '')
                ])

        print(f"Data exported to {output_file}")

    def export_to_json(self, output_file: str, days_back: int = 30):
        """
        Export competitor data to JSON file.

        Args:
            output_file: Path to output JSON file
            days_back: Number of days of data to export
        """
        competitors = self.db.get_competitors()
        updates = self.db.get_recent_updates(days=days_back)
        stats = self.db.get_stats()

        data = {
            'generated_at': datetime.now().isoformat(),
            'period_days': days_back,
            'statistics': stats,
            'competitors': competitors,
            'updates': updates
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Data exported to {output_file}")

    def _generate_text_report(self, updates: Dict, date: str,
                             report_type: str) -> str:
        """Generate simple text report without AI."""
        if report_type == 'daily':
            title = f"Daily Competitor Report - {date}"
        else:
            title = f"Weekly Competitor Report - Week of {date}"

        report = f"{title}\n"
        report += "=" * 60 + "\n\n"

        news_count = len(updates.get('news', []))
        product_count = len(updates.get('product_changes', []))
        company_count = len(updates.get('company_updates', []))

        report += f"Total Updates: {news_count + product_count + company_count}\n"
        report += f"  - News: {news_count}\n"
        report += f"  - Product Changes: {product_count}\n"
        report += f"  - Company Updates: {company_count}\n\n"

        # News section
        if updates.get('news'):
            report += f"NEWS ({news_count} items)\n"
            report += "-" * 60 + "\n"
            for item in updates['news'][:10]:
                report += f"\n• [{item.get('competitor_name', 'Unknown')}] {item['title']}\n"
                if item.get('source'):
                    report += f"  Source: {item['source']}\n"
                if item.get('url'):
                    report += f"  URL: {item['url']}\n"
            report += "\n"

        # Product changes
        if updates.get('product_changes'):
            report += f"PRODUCT CHANGES ({product_count} items)\n"
            report += "-" * 60 + "\n"
            for item in updates['product_changes']:
                report += f"\n• [{item.get('competitor_name', 'Unknown')}] "
                report += f"{item.get('product_name', 'Unknown Product')}: "
                report += f"{item.get('change_type', 'update')}\n"
                if item.get('description'):
                    report += f"  {item['description']}\n"
            report += "\n"

        # Company updates
        if updates.get('company_updates'):
            report += f"COMPANY UPDATES ({company_count} items)\n"
            report += "-" * 60 + "\n"
            for item in updates['company_updates']:
                report += f"\n• [{item.get('competitor_name', 'Unknown')}] {item['title']}\n"
                if item.get('description'):
                    report += f"  {item['description']}\n"
            report += "\n"

        return report

    def _generate_html_report(self, updates: Dict, date: str,
                             report_type: str) -> str:
        """Generate HTML format report."""
        if report_type == 'daily':
            title = f"Daily Competitor Report - {date}"
        else:
            title = f"Weekly Competitor Report - Week of {date}"

        news_count = len(updates.get('news', []))
        product_count = len(updates.get('product_changes', []))
        company_count = len(updates.get('company_updates', []))

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; border-bottom: 2px solid #ddd; padding-bottom: 5px; }}
        .summary {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; }}
        .item {{ margin: 15px 0; padding: 10px; border-left: 3px solid #4CAF50; }}
        .competitor {{ color: #2196F3; font-weight: bold; }}
        .source {{ color: #999; font-size: 0.9em; }}
        a {{ color: #2196F3; text-decoration: none; }}
    </style>
</head>
<body>
    <h1>{title}</h1>

    <div class="summary">
        <p><strong>Total Updates:</strong> {news_count + product_count + company_count}</p>
        <ul>
            <li>News: {news_count}</li>
            <li>Product Changes: {product_count}</li>
            <li>Company Updates: {company_count}</li>
        </ul>
    </div>
"""

        # News section
        if updates.get('news'):
            html += f"\n    <h2>News ({news_count} items)</h2>\n"
            for item in updates['news']:
                html += f"""    <div class="item">
        <span class="competitor">[{item.get('competitor_name', 'Unknown')}]</span> {item['title']}<br>
        <span class="source">Source: {item.get('source', 'Unknown')}</span>
"""
                if item.get('url'):
                    html += f"""        | <a href="{item['url']}" target="_blank">Read more</a>
"""
                if item.get('ai_summary'):
                    html += f"""        <p>{item['ai_summary']}</p>
"""
                html += "    </div>\n"

        # Product changes
        if updates.get('product_changes'):
            html += f"\n    <h2>Product Changes ({product_count} items)</h2>\n"
            for item in updates['product_changes']:
                html += f"""    <div class="item">
        <span class="competitor">[{item.get('competitor_name', 'Unknown')}]</span>
        {item.get('product_name', 'Unknown')}: {item.get('change_type', 'update')}<br>
        <p>{item.get('description', '')}</p>
    </div>
"""

        # Company updates
        if updates.get('company_updates'):
            html += f"\n    <h2>Company Updates ({company_count} items)</h2>\n"
            for item in updates['company_updates']:
                html += f"""    <div class="item">
        <span class="competitor">[{item.get('competitor_name', 'Unknown')}]</span> {item['title']}<br>
        <p>{item.get('description', '')}</p>
    </div>
"""

        html += """
</body>
</html>
"""
        return html
