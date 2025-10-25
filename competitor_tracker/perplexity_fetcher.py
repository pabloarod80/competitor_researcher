"""
Perplexity API integration for news and social media search.

Uses Perplexity's search API to gather comprehensive information about
competitors from news sources, social media, and the broader web.
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class PerplexityFetcher:
    """
    Fetches competitor information using Perplexity API.

    Perplexity provides AI-powered search across:
    - News articles
    - Social media (Twitter, Reddit, etc.)
    - Blog posts and press releases
    - Company announcements
    - Industry publications
    """

    def __init__(self, api_key: str, model: str = "llama-3.1-sonar-large-128k-online"):
        """
        Initialize Perplexity fetcher.

        Args:
            api_key: Perplexity API key
            model: Model to use for search
                   Options:
                   - llama-3.1-sonar-small-128k-online (fastest, most cost-effective)
                   - llama-3.1-sonar-large-128k-online (more comprehensive, default)
                   - llama-3.1-sonar-huge-128k-online (most detailed)
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.perplexity.ai/chat/completions"

    def search_competitor_news(self,
                               competitor_name: str,
                               keywords: List[str] = None,
                               days_back: int = 7,
                               include_social: bool = True) -> List[Dict]:
        """
        Search for news and updates about a competitor.

        Args:
            competitor_name: Name of the competitor
            keywords: Additional keywords to search for
            days_back: Number of days to look back
            include_social: Include social media mentions

        Returns:
            List of structured news items with source attribution
        """
        # Build search query
        query = self._build_search_query(
            competitor_name,
            keywords,
            days_back,
            include_social
        )

        # Call Perplexity API
        response = self._call_perplexity_api(query)

        if not response:
            return []

        # Parse response and extract structured data
        results = self._parse_search_results(response, competitor_name)

        return results

    def search_product_updates(self,
                              competitor_name: str,
                              product_keywords: List[str] = None) -> List[Dict]:
        """
        Search for product launches, updates, and feature announcements.

        Args:
            competitor_name: Name of the competitor
            product_keywords: Product-specific keywords

        Returns:
            List of product-related updates
        """
        product_terms = [
            "product launch", "new feature", "release", "update",
            "announces", "unveils", "introduces", "beta"
        ]

        if product_keywords:
            product_terms.extend(product_keywords)

        query = f"""Find recent product launches, feature releases, and product updates from {competitor_name}.

Focus on:
- New product announcements
- Feature releases and updates
- Beta programs
- Product discontinuations
- Pricing changes

Search the last 30 days. Include sources and dates.
Provide specific details about each product update."""

        response = self._call_perplexity_api(query)

        if not response:
            return []

        results = self._parse_search_results(response, competitor_name)

        # Tag as product updates
        for result in results:
            result['category'] = 'product_update'

        return results

    def search_social_media_sentiment(self,
                                     competitor_name: str,
                                     days_back: int = 7) -> Dict:
        """
        Search social media for sentiment and trending discussions.

        Args:
            competitor_name: Name of the competitor
            days_back: Number of days to analyze

        Returns:
            Sentiment analysis with key themes
        """
        query = f"""Analyze recent social media discussions about {competitor_name} from the last {days_back} days.

Search Twitter, Reddit, Hacker News, and LinkedIn.

Provide:
1. Overall sentiment (positive/negative/neutral)
2. Key themes being discussed
3. Notable complaints or praise
4. Trending topics related to the company
5. Customer feedback highlights

Include specific examples and sources."""

        response = self._call_perplexity_api(query)

        if not response:
            return {
                'sentiment': 'neutral',
                'themes': [],
                'mentions': []
            }

        # Parse sentiment analysis
        return self._parse_sentiment_analysis(response, competitor_name)

    def search_company_changes(self,
                              competitor_name: str,
                              days_back: int = 30) -> List[Dict]:
        """
        Search for company-level changes (funding, leadership, M&A, etc.).

        Args:
            competitor_name: Name of the competitor
            days_back: Number of days to look back

        Returns:
            List of company updates
        """
        query = f"""Find recent company news and changes for {competitor_name} from the last {days_back} days.

Focus on:
- Funding announcements and investment rounds
- Leadership changes (CEO, executives)
- Mergers and acquisitions
- Strategic partnerships
- Office expansions or closures
- Layoffs or hiring sprees
- Revenue/financial announcements

Provide specific details, amounts, and sources."""

        response = self._call_perplexity_api(query)

        if not response:
            return []

        results = self._parse_search_results(response, competitor_name)

        # Tag as company updates
        for result in results:
            result['category'] = 'company_update'

        return results

    def get_competitive_intelligence_summary(self,
                                            competitor_name: str,
                                            days_back: int = 7) -> Dict:
        """
        Get a comprehensive competitive intelligence summary.

        Args:
            competitor_name: Name of the competitor
            days_back: Number of days to analyze

        Returns:
            Comprehensive summary with multiple dimensions
        """
        query = f"""Provide a comprehensive competitive intelligence summary for {competitor_name} from the last {days_back} days.

Include:
1. Recent News: Major announcements and coverage
2. Product Updates: New features, launches, changes
3. Social Media Buzz: What people are saying online
4. Company Changes: Funding, hiring, partnerships
5. Market Position: Industry analysis and competitive moves
6. Customer Sentiment: Positive and negative feedback

For each item, include:
- Specific details
- Dates
- Sources (with URLs when available)
- Significance/impact

Be comprehensive and factual."""

        response = self._call_perplexity_api(query)

        if not response:
            return {
                'summary': 'No information found',
                'updates': []
            }

        return self._parse_intelligence_summary(response, competitor_name)

    def _build_search_query(self,
                           competitor_name: str,
                           keywords: List[str],
                           days_back: int,
                           include_social: bool) -> str:
        """Build search query for Perplexity."""

        sources = "news articles, press releases, and industry publications"
        if include_social:
            sources += ", social media (Twitter, Reddit, LinkedIn, Hacker News), and blog posts"

        keyword_text = ""
        if keywords:
            keyword_text = f"\nFocus on these topics: {', '.join(keywords)}"

        query = f"""Find recent updates and news about {competitor_name} from the last {days_back} days.

Search {sources}.{keyword_text}

Provide:
- News headlines and summaries
- Sources and publication dates
- URLs when available
- Key details and significance

Organize by date (most recent first)."""

        return query

    def _call_perplexity_api(self, query: str) -> Optional[str]:
        """
        Call Perplexity API with a search query.

        Args:
            query: Search query to send

        Returns:
            Response text from Perplexity
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a competitive intelligence researcher. Provide factual, detailed information with sources. Always include dates and URLs when available."
                },
                {
                    "role": "user",
                    "content": query
                }
            ],
            "temperature": 0.2,
            "max_tokens": 4000,
            "return_citations": True,
            "search_recency_filter": "month"  # Focus on recent information
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                content = data.get('choices', [{}])[0].get('message', {}).get('content', '')

                # Extract citations if available
                citations = data.get('citations', [])

                return content
            else:
                print(f"Perplexity API error: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"Error calling Perplexity API: {e}")
            return None

    def _parse_search_results(self, response: str, competitor_name: str) -> List[Dict]:
        """
        Parse Perplexity response into structured news items.

        Args:
            response: Raw response from Perplexity
            competitor_name: Name of competitor

        Returns:
            List of structured news items
        """
        results = []

        # Split response into individual items
        # Perplexity typically formats responses with clear sections
        lines = response.split('\n')

        current_item = {}

        for line in lines:
            line = line.strip()

            if not line:
                if current_item:
                    results.append(current_item)
                    current_item = {}
                continue

            # Try to extract structured information
            if line.startswith('- ') or line.startswith('* ') or line.startswith('• '):
                # This is likely a news item
                title = line[2:].strip()
                current_item = {
                    'title': title,
                    'competitor_name': competitor_name,
                    'source': 'Perplexity Search',
                    'content': '',
                    'url': None,
                    'published_at': None,
                    'fetched_at': datetime.now().isoformat()
                }
            elif line.startswith('http'):
                # This is likely a URL
                if current_item:
                    current_item['url'] = line
            elif current_item and not current_item.get('content'):
                # This is likely content/description
                current_item['content'] = line

        # Add last item if exists
        if current_item:
            results.append(current_item)

        # If parsing didn't work well, create a single comprehensive item
        if not results:
            results.append({
                'title': f'Competitive Intelligence Update: {competitor_name}',
                'competitor_name': competitor_name,
                'source': 'Perplexity Search',
                'content': response,
                'url': None,
                'published_at': datetime.now().isoformat(),
                'fetched_at': datetime.now().isoformat()
            })

        return results

    def _parse_sentiment_analysis(self, response: str, competitor_name: str) -> Dict:
        """Parse sentiment analysis from Perplexity response."""

        # Extract sentiment
        sentiment = 'neutral'
        if any(word in response.lower() for word in ['mostly positive', 'positive sentiment', 'favorable']):
            sentiment = 'positive'
        elif any(word in response.lower() for word in ['mostly negative', 'negative sentiment', 'critical']):
            sentiment = 'negative'

        # Extract themes (simplified - could be more sophisticated)
        themes = []
        theme_keywords = ['theme:', 'topic:', 'discussion:', 'trend:']
        for line in response.split('\n'):
            for keyword in theme_keywords:
                if keyword in line.lower():
                    themes.append(line.strip())

        return {
            'competitor': competitor_name,
            'sentiment': sentiment,
            'themes': themes,
            'summary': response,
            'analyzed_at': datetime.now().isoformat()
        }

    def _parse_intelligence_summary(self, response: str, competitor_name: str) -> Dict:
        """Parse comprehensive intelligence summary."""

        return {
            'competitor': competitor_name,
            'summary': response,
            'generated_at': datetime.now().isoformat(),
            'source': 'Perplexity AI Search'
        }
