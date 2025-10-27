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

    def __init__(self, api_key: str, model: str = "sonar-pro"):
        """
        Initialize Perplexity fetcher.

        Args:
            api_key: Perplexity API key
            model: Model to use for search (2025 Sonar models)
                   Options:
                   - sonar (lightweight, fast, affordable)
                   - sonar-pro (advanced, better for complex queries - DEFAULT)
                   - sonar-reasoning (adds chain-of-thought reasoning)
                   - sonar-reasoning-pro (most advanced reasoning)
        """
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.perplexity.ai/chat/completions"

    def search_competitor_news(self,
                               competitor_name: str,
                               keywords: List[str] = None,
                               days_back: int = 7,
                               include_social: bool = True,
                               company_context: str = None) -> List[Dict]:
        """
        Search for news and updates about a competitor.

        Args:
            competitor_name: Name of the competitor
            keywords: Additional keywords to search for (deprecated - use company_context)
            days_back: Number of days to look back
            include_social: Include social media mentions
            company_context: Rich context about the company (description, industry, products)

        Returns:
            List of structured news items with source attribution
        """
        # Build search query
        query = self._build_search_query(
            competitor_name,
            keywords,
            days_back,
            include_social,
            company_context
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
                           include_social: bool,
                           company_context: str = None) -> str:
        """Build search query for Perplexity."""

        sources = "news articles, press releases, and industry publications"
        if include_social:
            sources += ", social media (Twitter, Reddit, LinkedIn, Hacker News), and blog posts"

        # Use rich company context if available, otherwise fall back to keywords
        context_text = ""
        if company_context:
            context_text = f"\n\nCompany context: {company_context}"
            context_text += "\nUse this context to find relevant news about this company's products, services, and industry."
        elif keywords:
            context_text = f"\nFocus on these topics: {', '.join(keywords)}"

        query = f"""Find recent updates and news about {competitor_name} from the last {days_back} days.

Search {sources}.{context_text}

For each news item you find, provide the response in this EXACT format:

TITLE: [headline or title of the news]
SOURCE: [source name]
DATE: [publication date]
URL: [article URL if available]
SUMMARY: [brief summary of the article]

---

Find 5-10 recent news items and format each one using the structure above. Separate each item with --- .
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

        # Split response by separator ---
        items = response.split('---')

        for item_text in items:
            item_text = item_text.strip()
            if not item_text:
                continue

            # Initialize item with defaults
            item = {
                'title': '',
                'competitor_name': competitor_name,
                'source': 'Perplexity Search',
                'content': '',
                'url': None,
                'published_at': None,
                'fetched_at': datetime.now().isoformat()
            }

            # Parse each line looking for structured fields
            lines = item_text.split('\n')
            for line in lines:
                line = line.strip()

                if line.startswith('TITLE:'):
                    item['title'] = line.replace('TITLE:', '').strip()
                elif line.startswith('SOURCE:'):
                    item['source'] = line.replace('SOURCE:', '').strip()
                elif line.startswith('DATE:'):
                    item['published_at'] = line.replace('DATE:', '').strip()
                elif line.startswith('URL:'):
                    url = line.replace('URL:', '').strip()
                    if url and url.lower() != 'n/a' and url.lower() != 'not available':
                        item['url'] = url
                elif line.startswith('SUMMARY:'):
                    item['content'] = line.replace('SUMMARY:', '').strip()
                elif line and not any(line.startswith(prefix) for prefix in ['TITLE:', 'SOURCE:', 'DATE:', 'URL:', 'SUMMARY:']):
                    # Continuation of previous field (likely summary)
                    if item.get('content'):
                        item['content'] += ' ' + line
                    elif not item.get('title'):
                        # If no title yet, this might be it
                        item['title'] = line

            # Only add item if it has a title
            if item['title']:
                results.append(item)

        # If parsing didn't produce any results, try alternative parsing
        if not results:
            # Try to extract from bullet points or numbered lists
            lines = response.split('\n')
            current_item = None

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Check if line starts with bullet or number
                if line.startswith(('- ', '* ', '• ', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                    # Save previous item if exists
                    if current_item and current_item.get('title'):
                        results.append(current_item)

                    # Start new item
                    # Remove bullet/number prefix
                    for prefix in ['- ', '* ', '• ']:
                        if line.startswith(prefix):
                            line = line[len(prefix):].strip()
                            break

                    # Remove number prefix (e.g., "1. ")
                    import re
                    line = re.sub(r'^\d+\.\s*', '', line)

                    current_item = {
                        'title': line,
                        'competitor_name': competitor_name,
                        'source': 'Perplexity Search',
                        'content': '',
                        'url': None,
                        'published_at': None,
                        'fetched_at': datetime.now().isoformat()
                    }
                elif current_item:
                    # Add to content of current item
                    if line.startswith('http'):
                        current_item['url'] = line
                    elif current_item['content']:
                        current_item['content'] += ' ' + line
                    else:
                        current_item['content'] = line

            # Add last item
            if current_item and current_item.get('title'):
                results.append(current_item)

        # Final fallback: create single comprehensive item
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
