"""
News and updates fetcher for competitor tracking.

Fetches news, product updates, and company information from various sources.
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
from urllib.parse import quote_plus


class NewsFetcher:
    """Fetches news and updates about competitors."""

    def __init__(self, config: Dict = None):
        """Initialize the news fetcher with configuration."""
        self.config = config or {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_google_news(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Fetch news from Google News RSS (simplified approach).

        Note: For production, consider using proper news APIs like:
        - NewsAPI (newsapi.org)
        - Google News API
        - Bing News Search API
        """
        # This is a simplified implementation
        # In production, you should use proper news APIs

        results = []

        # Google News RSS format
        encoded_query = quote_plus(query)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"

        try:
            response = self.session.get(rss_url, timeout=10)

            if response.status_code == 200:
                # Parse RSS feed (simplified)
                content = response.text

                # This is a basic parser - for production use feedparser library
                import re

                # Extract items from RSS
                items = re.findall(r'<item>(.*?)</item>', content, re.DOTALL)

                for item in items[:max_results]:
                    # Extract title - try multiple patterns
                    title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item, re.DOTALL)
                    if not title_match:
                        # Fallback: try without CDATA
                        title_match = re.search(r'<title>(.*?)</title>', item, re.DOTALL)

                    title = title_match.group(1).strip() if title_match else None

                    # Skip item if no title found
                    if not title:
                        continue

                    # Extract link
                    link_match = re.search(r'<link>(.*?)</link>', item)
                    link = link_match.group(1).strip() if link_match else None

                    # Extract pub date
                    date_match = re.search(r'<pubDate>(.*?)</pubDate>', item)
                    pub_date = date_match.group(1).strip() if date_match else None

                    # Extract description/snippet - try multiple patterns
                    desc_match = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item, re.DOTALL)
                    if not desc_match:
                        desc_match = re.search(r'<description>(.*?)</description>', item, re.DOTALL)
                    description = desc_match.group(1).strip() if desc_match else ""

                    # Extract source
                    source_match = re.search(r'<source.*?>(.*?)</source>', item)
                    source = source_match.group(1).strip() if source_match else "Google News"

                    results.append({
                        'title': title,
                        'url': link,
                        'source': source,
                        'content': description,
                        'published_at': pub_date,
                        'fetched_at': datetime.now().isoformat()
                    })

        except Exception as e:
            print(f"Error fetching Google News: {e}")

        return results

    def fetch_with_newsapi(self, query: str, api_key: str,
                          from_date: str = None, max_results: int = 10) -> List[Dict]:
        """
        Fetch news using NewsAPI (requires API key from newsapi.org).

        Args:
            query: Search query
            api_key: NewsAPI key
            from_date: Start date (YYYY-MM-DD format)
            max_results: Maximum number of results
        """
        if not api_key:
            return []

        url = "https://newsapi.org/v2/everything"

        # Default to last 7 days if no date specified
        if not from_date:
            from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        params = {
            'q': query,
            'from': from_date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': max_results,
            'apiKey': api_key
        }

        results = []

        try:
            response = self.session.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                for article in data.get('articles', []):
                    results.append({
                        'title': article.get('title', ''),
                        'url': article.get('url', ''),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'content': article.get('description', ''),
                        'published_at': article.get('publishedAt', ''),
                        'fetched_at': datetime.now().isoformat()
                    })
            else:
                print(f"NewsAPI error: {response.status_code}")

        except Exception as e:
            print(f"Error fetching from NewsAPI: {e}")

        return results

    def fetch_competitor_news(self, competitor_name: str,
                             keywords: List[str] = None,
                             days_back: int = 7,
                             max_results: int = 10,
                             include_social: bool = False) -> List[Dict]:
        """
        Fetch news about a specific competitor using Perplexity API.

        Args:
            competitor_name: Name of the competitor
            keywords: Additional keywords to search for
            days_back: Number of days to look back
            max_results: Maximum number of results to return
            include_social: Include social media (Twitter, Reddit, etc.)

        Returns:
            List of news items

        Raises:
            ValueError: If Perplexity API key is not configured
        """
        # Check if Perplexity API key is configured
        if not self.config.get('perplexity_api_key'):
            raise ValueError(
                "Perplexity API key is required. Please configure it in Settings.\n"
                "Get your API key at: https://www.perplexity.ai/settings/api"
            )

        try:
            from .perplexity_fetcher import PerplexityFetcher

            perplexity = PerplexityFetcher(
                api_key=self.config['perplexity_api_key'],
                model=self.config.get('perplexity_model', 'sonar-pro')
            )

            results = perplexity.search_competitor_news(
                competitor_name,
                keywords=keywords,
                days_back=days_back,
                include_social=include_social
            )

            return results[:max_results] if results else []

        except Exception as e:
            print(f"Error fetching news from Perplexity: {e}")
            raise

    def fetch_product_updates(self, competitor_name: str,
                            product_keywords: List[str] = None) -> List[Dict]:
        """
        Fetch product-related updates for a competitor using Perplexity API.

        Searches for product launches, feature releases, updates, etc.

        Args:
            competitor_name: Name of the competitor
            product_keywords: Additional product-specific keywords

        Returns:
            List of product update items

        Raises:
            ValueError: If Perplexity API key is not configured
        """
        # Check if Perplexity API key is configured
        if not self.config.get('perplexity_api_key'):
            raise ValueError(
                "Perplexity API key is required. Please configure it in Settings.\n"
                "Get your API key at: https://www.perplexity.ai/settings/api"
            )

        try:
            from .perplexity_fetcher import PerplexityFetcher

            perplexity = PerplexityFetcher(
                api_key=self.config['perplexity_api_key'],
                model=self.config.get('perplexity_model', 'sonar-pro')
            )

            results = perplexity.search_product_updates(
                competitor_name,
                product_keywords=product_keywords
            )

            return results if results else []

        except Exception as e:
            print(f"Error fetching product updates from Perplexity: {e}")
            raise

    def fetch_company_updates(self, competitor_name: str) -> List[Dict]:
        """
        Fetch company-related updates using Perplexity API.

        Searches for funding, acquisitions, leadership changes, and corporate news.

        Args:
            competitor_name: Name of the competitor

        Returns:
            List of company update items

        Raises:
            ValueError: If Perplexity API key is not configured
        """
        # Check if Perplexity API key is configured
        if not self.config.get('perplexity_api_key'):
            raise ValueError(
                "Perplexity API key is required. Please configure it in Settings.\n"
                "Get your API key at: https://www.perplexity.ai/settings/api"
            )

        try:
            from .perplexity_fetcher import PerplexityFetcher

            perplexity = PerplexityFetcher(
                api_key=self.config['perplexity_api_key'],
                model=self.config.get('perplexity_model', 'sonar-pro')
            )

            results = perplexity.search_company_changes(
                competitor_name,
                days_back=30
            )

            return results if results else []

        except Exception as e:
            print(f"Error fetching company updates from Perplexity: {e}")
            raise

    def categorize_news(self, title: str, content: str) -> str:
        """
        Categorize a news item based on keywords.

        Categories: product, company, funding, partnership, general
        """
        text = f"{title} {content}".lower()

        if any(word in text for word in ['product', 'feature', 'launch', 'release', 'update']):
            return 'product'
        elif any(word in text for word in ['funding', 'investment', 'raise', 'series']):
            return 'funding'
        elif any(word in text for word in ['acquisition', 'acquire', 'merger', 'buy']):
            return 'acquisition'
        elif any(word in text for word in ['partnership', 'partner', 'collaborate', 'alliance']):
            return 'partnership'
        elif any(word in text for word in ['ceo', 'executive', 'leadership', 'appoints']):
            return 'leadership'
        else:
            return 'general'

    def analyze_sentiment(self, text: str) -> str:
        """
        Simple sentiment analysis based on keywords.

        For production, use proper sentiment analysis libraries or AI models.
        """
        text = text.lower()

        positive_words = [
            'success', 'growth', 'profit', 'win', 'achievement', 'innovative',
            'breakthrough', 'leading', 'best', 'excellent', 'strong', 'gains'
        ]

        negative_words = [
            'loss', 'decline', 'problem', 'issue', 'concern', 'struggle',
            'fail', 'weak', 'crisis', 'lawsuit', 'drop', 'falls'
        ]

        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'


class DataEnricher:
    """Enriches fetched data with additional context and analysis."""

    def __init__(self):
        """Initialize data enricher."""
        pass

    def extract_key_points(self, text: str, max_points: int = 3) -> List[str]:
        """
        Extract key points from text.

        This is a simplified version - for production use NLP libraries.
        """
        if not text:
            return []

        # Split into sentences
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        # Return first few sentences as key points
        return sentences[:max_points]

    def detect_change_type(self, text: str) -> str:
        """Detect the type of product/company change from text."""
        text = text.lower()

        if 'new feature' in text or 'introduces' in text:
            return 'new_feature'
        elif 'pricing' in text or 'price' in text:
            return 'pricing_change'
        elif 'rebranding' in text or 'rebrand' in text:
            return 'rebrand'
        elif 'discontinue' in text or 'sunset' in text:
            return 'product_discontinuation'
        elif 'acquisition' in text or 'acquire' in text:
            return 'acquisition'
        else:
            return 'general_update'

    def assess_impact(self, category: str, sentiment: str) -> str:
        """Assess the potential impact level of an update."""
        if category in ['funding', 'acquisition'] and sentiment == 'positive':
            return 'high'
        elif category == 'product' and sentiment in ['positive', 'neutral']:
            return 'medium'
        elif sentiment == 'negative':
            return 'medium'
        else:
            return 'low'
