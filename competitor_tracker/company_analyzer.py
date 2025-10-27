"""
Company information extractor.

Automatically extracts company information from their website to improve
news search relevance without requiring manual keyword entry.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re


class CompanyAnalyzer:
    """Extract company information from their website."""

    def __init__(self):
        """Initialize the company analyzer."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def extract_company_info(self, company_name: str, website_url: str) -> Dict[str, str]:
        """
        Extract company information from their website.

        Args:
            company_name: Name of the company
            website_url: URL of the company's website

        Returns:
            Dictionary with extracted information:
            - description: Company description
            - products: Key products/services
            - industry: Industry/sector
            - focus_areas: Main focus areas
        """
        info = {
            'description': '',
            'products': '',
            'industry': '',
            'focus_areas': ''
        }

        try:
            # Fetch the homepage
            response = self.session.get(website_url, timeout=10)
            if response.status_code != 200:
                return info

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc and meta_desc.get('content'):
                info['description'] = meta_desc.get('content', '').strip()

            # Extract og:description as fallback
            if not info['description']:
                og_desc = soup.find('meta', attrs={'property': 'og:description'})
                if og_desc and og_desc.get('content'):
                    info['description'] = og_desc.get('content', '').strip()

            # Extract text from common sections
            about_text = self._extract_about_section(soup)
            if about_text and not info['description']:
                info['description'] = about_text[:500]  # First 500 chars

            # Extract keywords from meta tags
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            if meta_keywords and meta_keywords.get('content'):
                keywords = meta_keywords.get('content', '').strip()
                info['focus_areas'] = keywords

            # Try to identify industry from content
            info['industry'] = self._identify_industry(soup, info['description'])

            # Extract product information
            info['products'] = self._extract_products(soup)

        except Exception as e:
            print(f"Error extracting info from {website_url}: {e}")

        return info

    def _extract_about_section(self, soup: BeautifulSoup) -> str:
        """Extract text from About section of the website."""
        about_text = ''

        # Look for common about section selectors
        about_selectors = [
            'section.about',
            'div.about',
            'section#about',
            'div#about',
            '.about-section',
            '.company-description'
        ]

        for selector in about_selectors:
            section = soup.select_one(selector)
            if section:
                about_text = section.get_text(separator=' ', strip=True)
                break

        # Look for h1 or h2 with "About" in it
        if not about_text:
            for heading in soup.find_all(['h1', 'h2', 'h3']):
                if 'about' in heading.get_text().lower():
                    # Get the next sibling paragraph or div
                    next_elem = heading.find_next(['p', 'div'])
                    if next_elem:
                        about_text = next_elem.get_text(separator=' ', strip=True)
                        break

        return about_text

    def _identify_industry(self, soup: BeautifulSoup, description: str) -> str:
        """Identify the company's industry from content."""
        text = (description + ' ' + soup.get_text()).lower()

        industries = {
            'ai': ['artificial intelligence', 'machine learning', 'ai', 'llm', 'neural network'],
            'software': ['software', 'saas', 'platform', 'application', 'app'],
            'fintech': ['financial', 'fintech', 'banking', 'payment', 'crypto'],
            'ecommerce': ['ecommerce', 'e-commerce', 'online shopping', 'marketplace'],
            'healthcare': ['health', 'medical', 'healthcare', 'pharma', 'biotech'],
            'cybersecurity': ['security', 'cybersecurity', 'encryption', 'privacy'],
            'cloud': ['cloud', 'infrastructure', 'hosting', 'servers'],
            'data': ['data', 'analytics', 'database', 'big data'],
        }

        for industry, keywords in industries.items():
            if any(keyword in text for keyword in keywords):
                return industry

        return 'technology'

    def _extract_products(self, soup: BeautifulSoup) -> str:
        """Extract product names and services from the website."""
        products = []

        # Look for product sections
        product_selectors = [
            'section.products',
            'div.products',
            'section#products',
            '.product-list',
            '.services'
        ]

        for selector in product_selectors:
            section = soup.select_one(selector)
            if section:
                # Find product names in headings
                for heading in section.find_all(['h2', 'h3', 'h4']):
                    product_name = heading.get_text(strip=True)
                    if product_name and len(product_name) < 50:  # Reasonable product name length
                        products.append(product_name)

        return ', '.join(products[:5])  # Limit to 5 products

    def generate_search_context(self, company_name: str, company_info: Dict[str, str]) -> str:
        """
        Generate search context for Perplexity based on extracted company info.

        Args:
            company_name: Name of the company
            company_info: Extracted company information

        Returns:
            Search context string to help Perplexity find relevant news
        """
        context_parts = [company_name]

        if company_info.get('industry'):
            context_parts.append(f"({company_info['industry']} company)")

        if company_info.get('description'):
            # Extract key phrases from description
            desc = company_info['description']
            # Simple keyword extraction - could be enhanced with NLP
            if len(desc) > 200:
                desc = desc[:200] + '...'
            context_parts.append(desc)

        if company_info.get('products'):
            context_parts.append(f"Products: {company_info['products']}")

        return ' '.join(context_parts)
