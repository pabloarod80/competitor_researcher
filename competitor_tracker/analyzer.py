"""
AI-powered analysis module for competitor tracking.

Provides AI-driven summarization, analysis, and insights generation.
Supports multiple AI providers (OpenAI, Anthropic, local models).
"""

import json
from typing import List, Dict, Optional
from datetime import datetime


class AIAnalyzer:
    """AI-powered content analyzer for competitor intelligence."""

    def __init__(self, config: Dict = None):
        """
        Initialize AI analyzer with configuration.

        Supported providers:
        - openai: OpenAI API (GPT-3.5/GPT-4)
        - anthropic: Anthropic Claude
        - local: Local models (e.g., via Ollama)
        """
        self.config = config or {}
        self.provider = self.config.get('ai_provider', 'openai')
        self.model = self.config.get('ai_model', 'gpt-3.5-turbo')
        self.client = None

        self._initialize_client()

    def _initialize_client(self):
        """Initialize the AI client based on provider."""
        if self.provider == 'openai':
            api_key = self.config.get('openai_api_key')
            if api_key:
                try:
                    import openai
                    self.client = openai.OpenAI(api_key=api_key)
                except ImportError:
                    print("OpenAI library not installed. Run: pip install openai")
            else:
                print("OpenAI API key not provided in config")

        elif self.provider == 'anthropic':
            api_key = self.config.get('anthropic_api_key')
            if api_key:
                try:
                    import anthropic
                    self.client = anthropic.Anthropic(api_key=api_key)
                except ImportError:
                    print("Anthropic library not installed. Run: pip install anthropic")
            else:
                print("Anthropic API key not provided in config")

        elif self.provider == 'local':
            # For local models via Ollama or similar
            self.ollama_base_url = self.config.get('ollama_url', 'http://localhost:11434')
            print(f"Using local AI model at {self.ollama_base_url}")

    def summarize_article(self, title: str, content: str,
                         max_length: int = 150) -> str:
        """
        Generate a concise summary of a news article.

        Args:
            title: Article title
            content: Article content
            max_length: Maximum summary length in words

        Returns:
            AI-generated summary
        """
        if not self.client and self.provider != 'local':
            # Fallback to simple summarization
            return self._simple_summary(content, max_length)

        prompt = f"""Summarize the following news article in {max_length} words or less.
Focus on the key facts and business implications.

Title: {title}

Content: {content}

Summary:"""

        try:
            if self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a business analyst summarizing competitor news."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()

            elif self.provider == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=200,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text.strip()

            elif self.provider == 'local':
                return self._local_ai_request(prompt)

        except Exception as e:
            print(f"AI summarization error: {e}")
            return self._simple_summary(content, max_length)

        return self._simple_summary(content, max_length)

    def analyze_competitive_impact(self, updates: List[Dict],
                                   competitor_name: str) -> Dict:
        """
        Analyze the competitive impact of recent updates.

        Args:
            updates: List of news/updates about the competitor
            competitor_name: Name of the competitor

        Returns:
            Analysis with threat level, opportunities, and recommendations
        """
        if not updates:
            return {
                'threat_level': 'low',
                'summary': 'No recent updates found.',
                'key_insights': [],
                'recommendations': []
            }

        if not self.client and self.provider != 'local':
            return self._simple_impact_analysis(updates, competitor_name)

        # Prepare context from updates
        context = f"Recent updates about {competitor_name}:\n\n"
        for i, update in enumerate(updates[:10], 1):
            context += f"{i}. {update.get('title', 'No title')}\n"
            if update.get('content'):
                context += f"   {update['content'][:200]}...\n"
            context += "\n"

        prompt = f"""{context}

Analyze these updates about {competitor_name} from a competitive intelligence perspective.

Provide:
1. Threat Level (low/medium/high)
2. Key Insights (3-5 bullet points)
3. Strategic Recommendations (2-3 actions)

Format as JSON:
{{
    "threat_level": "low/medium/high",
    "key_insights": ["insight 1", "insight 2", ...],
    "recommendations": ["action 1", "action 2", ...]
}}"""

        try:
            if self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a competitive intelligence analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.3
                )
                result = response.choices[0].message.content.strip()

            elif self.provider == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=500,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                result = response.content[0].text.strip()

            elif self.provider == 'local':
                result = self._local_ai_request(prompt)

            # Try to parse JSON response
            # Remove markdown code blocks if present
            result = result.replace('```json', '').replace('```', '').strip()
            return json.loads(result)

        except Exception as e:
            print(f"AI analysis error: {e}")
            return self._simple_impact_analysis(updates, competitor_name)

    def generate_daily_briefing(self, all_updates: Dict,
                               date: str = None) -> str:
        """
        Generate a daily briefing summarizing all competitor updates.

        Args:
            all_updates: Dictionary containing news, product changes, and company updates
            date: Date for the briefing (defaults to today)

        Returns:
            Formatted daily briefing text
        """
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        total_items = (
            len(all_updates.get('news', [])) +
            len(all_updates.get('product_changes', [])) +
            len(all_updates.get('company_updates', []))
        )

        if total_items == 0:
            return f"Daily Competitor Briefing - {date}\n\nNo updates found for today."

        briefing = f"Daily Competitor Briefing - {date}\n"
        briefing += "=" * 60 + "\n\n"

        # News section
        if all_updates.get('news'):
            briefing += f"NEWS UPDATES ({len(all_updates['news'])} items)\n"
            briefing += "-" * 60 + "\n"
            for item in all_updates['news'][:10]:
                competitor = item.get('competitor_name', 'Unknown')
                title = item.get('title', 'No title')
                briefing += f"\n• [{competitor}] {title}\n"
                if item.get('ai_summary'):
                    briefing += f"  {item['ai_summary']}\n"
                if item.get('url'):
                    briefing += f"  Link: {item['url']}\n"
            briefing += "\n"

        # Product changes section
        if all_updates.get('product_changes'):
            briefing += f"PRODUCT CHANGES ({len(all_updates['product_changes'])} items)\n"
            briefing += "-" * 60 + "\n"
            for item in all_updates['product_changes']:
                competitor = item.get('competitor_name', 'Unknown')
                product = item.get('product_name', 'Unknown')
                change = item.get('change_type', 'update')
                briefing += f"\n• [{competitor}] {product}: {change}\n"
                if item.get('description'):
                    briefing += f"  {item['description']}\n"
            briefing += "\n"

        # Company updates section
        if all_updates.get('company_updates'):
            briefing += f"COMPANY UPDATES ({len(all_updates['company_updates'])} items)\n"
            briefing += "-" * 60 + "\n"
            for item in all_updates['company_updates']:
                competitor = item.get('competitor_name', 'Unknown')
                title = item.get('title', 'No title')
                update_type = item.get('update_type', 'general')
                briefing += f"\n• [{competitor}] {title} ({update_type})\n"
                if item.get('ai_analysis'):
                    briefing += f"  {item['ai_analysis']}\n"
            briefing += "\n"

        return briefing

    def generate_weekly_report(self, all_updates: Dict,
                              week_start: str = None) -> str:
        """
        Generate a comprehensive weekly report with trends and insights.

        Args:
            all_updates: Dictionary containing all updates for the week
            week_start: Start date of the week

        Returns:
            Formatted weekly report
        """
        if not week_start:
            week_start = datetime.now().strftime('%Y-%m-%d')

        report = f"Weekly Competitor Intelligence Report\n"
        report += f"Week of {week_start}\n"
        report += "=" * 60 + "\n\n"

        # Executive summary
        total_news = len(all_updates.get('news', []))
        total_products = len(all_updates.get('product_changes', []))
        total_company = len(all_updates.get('company_updates', []))

        report += "EXECUTIVE SUMMARY\n"
        report += "-" * 60 + "\n"
        report += f"Total Updates: {total_news + total_products + total_company}\n"
        report += f"  - News Articles: {total_news}\n"
        report += f"  - Product Changes: {total_products}\n"
        report += f"  - Company Updates: {total_company}\n\n"

        # Group by competitor
        competitors = {}
        for item in all_updates.get('news', []):
            comp = item.get('competitor_name', 'Unknown')
            if comp not in competitors:
                competitors[comp] = {'news': [], 'products': [], 'company': []}
            competitors[comp]['news'].append(item)

        for item in all_updates.get('product_changes', []):
            comp = item.get('competitor_name', 'Unknown')
            if comp not in competitors:
                competitors[comp] = {'news': [], 'products': [], 'company': []}
            competitors[comp]['products'].append(item)

        for item in all_updates.get('company_updates', []):
            comp = item.get('competitor_name', 'Unknown')
            if comp not in competitors:
                competitors[comp] = {'news': [], 'products': [], 'company': []}
            competitors[comp]['company'].append(item)

        # Report by competitor
        report += "COMPETITOR BREAKDOWN\n"
        report += "-" * 60 + "\n\n"

        for comp_name, data in competitors.items():
            total = len(data['news']) + len(data['products']) + len(data['company'])
            report += f"{comp_name}: {total} updates\n"
            if data['news']:
                report += f"  News: {len(data['news'])}\n"
            if data['products']:
                report += f"  Products: {len(data['products'])}\n"
            if data['company']:
                report += f"  Company: {len(data['company'])}\n"
            report += "\n"

        return report

    def _simple_summary(self, text: str, max_words: int = 50) -> str:
        """Simple fallback summarization without AI."""
        if not text:
            return "No content available."

        # Take first few sentences
        sentences = text.replace('!', '.').replace('?', '.').split('.')
        summary = []
        word_count = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            words = sentence.split()
            if word_count + len(words) <= max_words:
                summary.append(sentence)
                word_count += len(words)
            else:
                break

        return '. '.join(summary) + '.' if summary else text[:200] + '...'

    def _simple_impact_analysis(self, updates: List[Dict],
                                competitor_name: str) -> Dict:
        """Simple fallback impact analysis without AI."""
        # Count different types of updates
        high_impact_keywords = ['acquisition', 'funding', 'merger', 'launch']
        medium_impact_keywords = ['product', 'feature', 'partnership']

        high_impact_count = 0
        medium_impact_count = 0

        insights = []
        for update in updates[:5]:
            text = f"{update.get('title', '')} {update.get('content', '')}".lower()

            if any(kw in text for kw in high_impact_keywords):
                high_impact_count += 1

            if any(kw in text for kw in medium_impact_keywords):
                medium_impact_count += 1

            # Add as insight
            if update.get('title'):
                insights.append(update['title'])

        # Determine threat level
        if high_impact_count >= 2:
            threat_level = 'high'
        elif high_impact_count >= 1 or medium_impact_count >= 3:
            threat_level = 'medium'
        else:
            threat_level = 'low'

        return {
            'threat_level': threat_level,
            'key_insights': insights[:5],
            'recommendations': [
                f"Monitor {competitor_name} activity closely",
                "Review and update competitive strategy"
            ]
        }

    def _local_ai_request(self, prompt: str) -> str:
        """Make request to local AI model (e.g., Ollama)."""
        try:
            import requests

            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )

            if response.status_code == 200:
                return response.json().get('response', '')
            else:
                print(f"Local AI request failed: {response.status_code}")
                return ""

        except Exception as e:
            print(f"Local AI error: {e}")
            return ""
