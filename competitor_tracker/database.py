"""
Database module for competitor tracking.

Manages SQLite database for storing competitors, news, product updates,
and analysis results.
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path


class CompetitorDB:
    """Manages the competitor tracking database."""

    def __init__(self, db_path: str = "competitors.db"):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = None
        self.init_db()

    def init_db(self):
        """Initialize database and create tables if they don't exist."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()

        # Competitors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS competitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                website TEXT,
                description TEXT,
                industry TEXT,
                founded_date TEXT,
                headquarters TEXT,
                employee_count TEXT,
                tracking_keywords TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # News/Updates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                competitor_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                url TEXT,
                source TEXT,
                content TEXT,
                category TEXT,
                sentiment TEXT,
                ai_summary TEXT,
                published_at TIMESTAMP,
                fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (competitor_id) REFERENCES competitors (id)
            )
        """)

        # Product Changes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                competitor_id INTEGER NOT NULL,
                product_name TEXT,
                change_type TEXT,
                description TEXT,
                impact_analysis TEXT,
                source_url TEXT,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (competitor_id) REFERENCES competitors (id)
            )
        """)

        # Company Updates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS company_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                competitor_id INTEGER NOT NULL,
                update_type TEXT,
                title TEXT,
                description TEXT,
                impact_level TEXT,
                source_url TEXT,
                ai_analysis TEXT,
                published_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (competitor_id) REFERENCES competitors (id)
            )
        """)

        # Tracking History table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracking_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                competitor_id INTEGER NOT NULL,
                tracking_date DATE NOT NULL,
                items_found INTEGER DEFAULT 0,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (competitor_id) REFERENCES competitors (id)
            )
        """)

        self.conn.commit()

    def add_competitor(self, name: str, website: str = None,
                      description: str = None, industry: str = None,
                      tracking_keywords: List[str] = None, **kwargs) -> int:
        """Add a new competitor to track."""
        cursor = self.conn.cursor()

        keywords_json = json.dumps(tracking_keywords) if tracking_keywords else None

        cursor.execute("""
            INSERT INTO competitors
            (name, website, description, industry, tracking_keywords, founded_date,
             headquarters, employee_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, website, description, industry, keywords_json,
              kwargs.get('founded_date'), kwargs.get('headquarters'),
              kwargs.get('employee_count')))

        self.conn.commit()
        return cursor.lastrowid

    def get_competitors(self) -> List[Dict[str, Any]]:
        """Get all competitors."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM competitors ORDER BY name")
        rows = cursor.fetchall()

        competitors = []
        for row in rows:
            comp = dict(row)
            if comp['tracking_keywords']:
                comp['tracking_keywords'] = json.loads(comp['tracking_keywords'])
            competitors.append(comp)

        return competitors

    def get_competitor_by_id(self, competitor_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific competitor by ID."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM competitors WHERE id = ?", (competitor_id,))
        row = cursor.fetchone()

        if row:
            comp = dict(row)
            if comp['tracking_keywords']:
                comp['tracking_keywords'] = json.loads(comp['tracking_keywords'])
            return comp
        return None

    def add_news(self, competitor_id: int, title: str, url: str = None,
                 source: str = None, content: str = None, category: str = None,
                 sentiment: str = None, ai_summary: str = None,
                 published_at: str = None) -> int:
        """Add a news item for a competitor."""
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO news
            (competitor_id, title, url, source, content, category, sentiment,
             ai_summary, published_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (competitor_id, title, url, source, content, category, sentiment,
              ai_summary, published_at))

        self.conn.commit()
        return cursor.lastrowid

    def add_product_change(self, competitor_id: int, product_name: str,
                          change_type: str, description: str,
                          impact_analysis: str = None, source_url: str = None) -> int:
        """Add a product change record."""
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO product_changes
            (competitor_id, product_name, change_type, description,
             impact_analysis, source_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (competitor_id, product_name, change_type, description,
              impact_analysis, source_url))

        self.conn.commit()
        return cursor.lastrowid

    def add_company_update(self, competitor_id: int, update_type: str,
                          title: str, description: str = None,
                          impact_level: str = None, source_url: str = None,
                          ai_analysis: str = None, published_at: str = None) -> int:
        """Add a company update record."""
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO company_updates
            (competitor_id, update_type, title, description, impact_level,
             source_url, ai_analysis, published_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (competitor_id, update_type, title, description, impact_level,
              source_url, ai_analysis, published_at))

        self.conn.commit()
        return cursor.lastrowid

    def get_news_by_date_range(self, competitor_id: int = None,
                               start_date: str = None, end_date: str = None) -> List[Dict]:
        """Get news items within a date range."""
        cursor = self.conn.cursor()

        query = "SELECT n.*, c.name as competitor_name FROM news n JOIN competitors c ON n.competitor_id = c.id WHERE 1=1"
        params = []

        if competitor_id:
            query += " AND n.competitor_id = ?"
            params.append(competitor_id)

        if start_date:
            query += " AND n.fetched_at >= ?"
            params.append(start_date)

        if end_date:
            query += " AND n.fetched_at <= ?"
            params.append(end_date)

        query += " ORDER BY n.fetched_at DESC"

        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def get_recent_updates(self, days: int = 7, competitor_id: int = None) -> Dict:
        """Get all recent updates (news, product changes, company updates)."""
        cursor = self.conn.cursor()

        date_filter = f"datetime('now', '-{days} days')"

        # Get news
        news_query = f"""
            SELECT n.*, c.name as competitor_name
            FROM news n
            JOIN competitors c ON n.competitor_id = c.id
            WHERE n.fetched_at >= {date_filter}
        """
        if competitor_id:
            news_query += f" AND n.competitor_id = {competitor_id}"
        news_query += " ORDER BY n.fetched_at DESC"

        cursor.execute(news_query)
        news = [dict(row) for row in cursor.fetchall()]

        # Get product changes
        product_query = f"""
            SELECT p.*, c.name as competitor_name
            FROM product_changes p
            JOIN competitors c ON p.competitor_id = c.id
            WHERE p.detected_at >= {date_filter}
        """
        if competitor_id:
            product_query += f" AND p.competitor_id = {competitor_id}"
        product_query += " ORDER BY p.detected_at DESC"

        cursor.execute(product_query)
        product_changes = [dict(row) for row in cursor.fetchall()]

        # Get company updates
        company_query = f"""
            SELECT u.*, c.name as competitor_name
            FROM company_updates u
            JOIN competitors c ON u.competitor_id = c.id
            WHERE u.created_at >= {date_filter}
        """
        if competitor_id:
            company_query += f" AND u.competitor_id = {competitor_id}"
        company_query += " ORDER BY u.created_at DESC"

        cursor.execute(company_query)
        company_updates = [dict(row) for row in cursor.fetchall()]

        return {
            'news': news,
            'product_changes': product_changes,
            'company_updates': company_updates
        }

    def update_competitor(self, competitor_id: int, **kwargs):
        """Update competitor information."""
        cursor = self.conn.cursor()

        # Build update query dynamically
        allowed_fields = ['name', 'website', 'description', 'industry',
                         'founded_date', 'headquarters', 'employee_count']

        updates = []
        values = []

        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = ?")
                values.append(value)
            elif field == 'tracking_keywords' and isinstance(value, list):
                updates.append("tracking_keywords = ?")
                values.append(json.dumps(value))

        if updates:
            updates.append("updated_at = CURRENT_TIMESTAMP")
            values.append(competitor_id)

            query = f"UPDATE competitors SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, values)
            self.conn.commit()

    def delete_competitor(self, competitor_id: int):
        """Delete a competitor and all associated data."""
        cursor = self.conn.cursor()

        # Delete all related records
        cursor.execute("DELETE FROM news WHERE competitor_id = ?", (competitor_id,))
        cursor.execute("DELETE FROM product_changes WHERE competitor_id = ?", (competitor_id,))
        cursor.execute("DELETE FROM company_updates WHERE competitor_id = ?", (competitor_id,))
        cursor.execute("DELETE FROM tracking_history WHERE competitor_id = ?", (competitor_id,))
        cursor.execute("DELETE FROM competitors WHERE id = ?", (competitor_id,))

        self.conn.commit()

    def get_stats(self) -> Dict[str, Any]:
        """Get overall statistics."""
        cursor = self.conn.cursor()

        cursor.execute("SELECT COUNT(*) as count FROM competitors")
        total_competitors = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM news")
        total_news = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM product_changes")
        total_product_changes = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM company_updates")
        total_company_updates = cursor.fetchone()['count']

        cursor.execute("""
            SELECT COUNT(*) as count FROM news
            WHERE fetched_at >= datetime('now', '-1 day')
        """)
        news_last_24h = cursor.fetchone()['count']

        return {
            'total_competitors': total_competitors,
            'total_news': total_news,
            'total_product_changes': total_product_changes,
            'total_company_updates': total_company_updates,
            'news_last_24h': news_last_24h
        }

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
