"""
Business-focused AI analysis module for competitive intelligence.

Provides strategic insights, threat assessment, and actionable recommendations
based on competitor activities and market changes.
"""

from typing import List, Dict, Optional
from datetime import datetime
import json


class BusinessImpactAnalyzer:
    """
    Analyzes competitor updates for business impact and strategic implications.

    Provides:
    - Threat/opportunity assessment
    - Strategic recommendations
    - Market positioning insights
    - Action items for response
    """

    def __init__(self, ai_analyzer=None):
        """
        Initialize with an AI analyzer instance.

        Args:
            ai_analyzer: AIAnalyzer instance for AI-powered analysis
        """
        self.ai_analyzer = ai_analyzer

    def analyze_business_impact(self, competitor_name: str,
                                updates: List[Dict],
                                your_company_context: str = None) -> Dict:
        """
        Analyze business impact of competitor updates.

        Args:
            competitor_name: Name of the competitor
            updates: List of recent updates about the competitor
            your_company_context: Optional context about your company/business

        Returns:
            Comprehensive business impact analysis
        """
        if not updates:
            return {
                'competitor': competitor_name,
                'threat_level': 'low',
                'opportunity_level': 'low',
                'overall_impact': 'minimal',
                'key_findings': ['No recent activity detected'],
                'strategic_recommendations': [],
                'action_items': [],
                'market_implications': []
            }

        # Use AI if available
        if self.ai_analyzer and self.ai_analyzer.client:
            return self._ai_business_analysis(competitor_name, updates, your_company_context)
        else:
            return self._rule_based_analysis(competitor_name, updates)

    def _ai_business_analysis(self, competitor_name: str,
                             updates: List[Dict],
                             company_context: str = None) -> Dict:
        """Use AI for sophisticated business impact analysis."""

        # Prepare context
        context = f"Competitor: {competitor_name}\n\n"
        context += "Recent Activities:\n"

        for i, update in enumerate(updates[:15], 1):
            context += f"{i}. {update.get('title', 'No title')}\n"
            if update.get('content'):
                context += f"   Details: {update['content'][:300]}\n"
            if update.get('category'):
                context += f"   Category: {update['category']}\n"
            if update.get('sentiment'):
                context += f"   Sentiment: {update['sentiment']}\n"
            context += "\n"

        company_info = ""
        if company_context:
            company_info = f"\nYour Business Context: {company_context}\n"

        prompt = f"""{context}{company_info}

As a strategic business analyst, analyze these competitor activities and provide actionable intelligence.

Provide a comprehensive analysis in the following JSON format:
{{
    "threat_level": "low/medium/high/critical",
    "opportunity_level": "low/medium/high",
    "overall_impact": "minimal/moderate/significant/major",
    "executive_summary": "2-3 sentence overview of the competitive situation",
    "key_findings": [
        "Finding 1: specific insight about what the competitor is doing",
        "Finding 2: ...",
        "Finding 3: ..."
    ],
    "threats": [
        "Specific threat 1 and why it matters",
        "Specific threat 2 and why it matters"
    ],
    "opportunities": [
        "Opportunity 1 you can capitalize on",
        "Opportunity 2 you can capitalize on"
    ],
    "strategic_recommendations": [
        "Strategic recommendation 1 with rationale",
        "Strategic recommendation 2 with rationale",
        "Strategic recommendation 3 with rationale"
    ],
    "action_items": [
        {{
            "priority": "high/medium/low",
            "action": "Specific action to take",
            "department": "Which team should handle this",
            "timeframe": "When to do it"
        }}
    ],
    "market_implications": [
        "Market trend or shift this indicates",
        "What this means for the industry"
    ]
}}

Focus on actionable insights and specific recommendations, not generic observations."""

        try:
            if self.ai_analyzer.provider == 'openai':
                response = self.ai_analyzer.client.chat.completions.create(
                    model=self.ai_analyzer.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a strategic business intelligence analyst specializing in competitive analysis. Provide specific, actionable insights."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1500,
                    temperature=0.4
                )
                result = response.choices[0].message.content.strip()

            elif self.ai_analyzer.provider == 'anthropic':
                response = self.ai_analyzer.client.messages.create(
                    model=self.ai_analyzer.model,
                    max_tokens=1500,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                result = response.content[0].text.strip()

            elif self.ai_analyzer.provider == 'local':
                result = self.ai_analyzer._local_ai_request(prompt)

            # Parse JSON response
            result = result.replace('```json', '').replace('```', '').strip()
            analysis = json.loads(result)
            analysis['competitor'] = competitor_name
            analysis['analyzed_at'] = datetime.now().isoformat()

            return analysis

        except Exception as e:
            print(f"AI business analysis error: {e}")
            return self._rule_based_analysis(competitor_name, updates)

    def _rule_based_analysis(self, competitor_name: str, updates: List[Dict]) -> Dict:
        """Fallback rule-based analysis when AI is not available."""

        # Categorize updates
        categories = {}
        sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}

        for update in updates:
            cat = update.get('category', 'general')
            categories[cat] = categories.get(cat, 0) + 1

            sent = update.get('sentiment', 'neutral')
            sentiments[sent] = sentiments.get(sent, 0) + 1

        # Assess threat level
        threat_level = 'low'
        if categories.get('funding', 0) >= 2 or categories.get('acquisition', 0) >= 1:
            threat_level = 'high'
        elif categories.get('product', 0) >= 3:
            threat_level = 'medium'
        elif len(updates) >= 10:
            threat_level = 'medium'

        # Assess opportunity
        opportunity_level = 'low'
        if sentiments['negative'] > sentiments['positive']:
            opportunity_level = 'medium'
        if categories.get('leadership', 0) >= 2:
            opportunity_level = 'medium'

        # Generate findings
        key_findings = []
        threats = []
        opportunities = []

        if categories.get('product', 0) > 0:
            key_findings.append(f"{competitor_name} has {categories['product']} product-related updates")
            threats.append("Active product development may lead to competitive features")

        if categories.get('funding', 0) > 0:
            key_findings.append(f"Funding activity detected: {categories['funding']} updates")
            threats.append("New funding provides resources for aggressive growth")

        if categories.get('partnership', 0) > 0:
            key_findings.append(f"{categories['partnership']} partnership announcements")
            opportunities.append("Potential partnership gaps in the market")

        if sentiments['negative'] > sentiments['positive']:
            key_findings.append("Negative sentiment detected in recent news")
            opportunities.append("Market dissatisfaction could be an opportunity")

        # Generate recommendations
        recommendations = []
        action_items = []

        if threat_level in ['high', 'critical']:
            recommendations.append(f"Monitor {competitor_name} closely and review competitive strategy")
            action_items.append({
                'priority': 'high',
                'action': f'Schedule competitive strategy review meeting about {competitor_name}',
                'department': 'Product & Strategy',
                'timeframe': 'This week'
            })

        if categories.get('product', 0) > 0:
            recommendations.append("Analyze their product changes for feature gaps and opportunities")
            action_items.append({
                'priority': 'medium',
                'action': 'Product team to review competitor feature releases',
                'department': 'Product',
                'timeframe': 'Within 2 weeks'
            })

        if opportunity_level in ['medium', 'high']:
            recommendations.append("Capitalize on competitor weaknesses with targeted marketing")
            action_items.append({
                'priority': 'medium',
                'action': 'Marketing to develop competitive positioning campaign',
                'department': 'Marketing',
                'timeframe': 'This month'
            })

        # Market implications
        market_implications = []
        if categories.get('funding', 0) > 0:
            market_implications.append("Increased investor interest in this market segment")
        if categories.get('product', 0) >= 3:
            market_implications.append("Rapid innovation cycle in the industry")

        return {
            'competitor': competitor_name,
            'threat_level': threat_level,
            'opportunity_level': opportunity_level,
            'overall_impact': 'significant' if threat_level == 'high' else 'moderate' if threat_level == 'medium' else 'minimal',
            'executive_summary': f"Analysis of {len(updates)} recent updates from {competitor_name}. "
                               f"Threat level: {threat_level}. {len(threats)} threats and {len(opportunities)} opportunities identified.",
            'key_findings': key_findings if key_findings else ['Limited recent activity'],
            'threats': threats if threats else ['No immediate threats identified'],
            'opportunities': opportunities if opportunities else ['No clear opportunities identified'],
            'strategic_recommendations': recommendations if recommendations else ['Continue monitoring'],
            'action_items': action_items,
            'market_implications': market_implications if market_implications else ['No significant market shifts detected'],
            'analyzed_at': datetime.now().isoformat()
        }

    def generate_executive_briefing(self, all_competitors_analysis: List[Dict]) -> str:
        """
        Generate an executive briefing summarizing all competitor analyses.

        Args:
            all_competitors_analysis: List of business impact analyses

        Returns:
            Formatted executive briefing text
        """
        briefing = "COMPETITIVE INTELLIGENCE EXECUTIVE BRIEFING\n"
        briefing += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        briefing += "=" * 70 + "\n\n"

        # Overall summary
        high_threats = [a for a in all_competitors_analysis if a.get('threat_level') in ['high', 'critical']]
        medium_threats = [a for a in all_competitors_analysis if a.get('threat_level') == 'medium']

        briefing += "EXECUTIVE SUMMARY\n"
        briefing += "-" * 70 + "\n"
        briefing += f"Competitors Analyzed: {len(all_competitors_analysis)}\n"
        briefing += f"High-Priority Threats: {len(high_threats)}\n"
        briefing += f"Medium-Priority Threats: {len(medium_threats)}\n\n"

        # High priority section
        if high_threats:
            briefing += "🔴 HIGH PRIORITY ITEMS\n"
            briefing += "-" * 70 + "\n"
            for analysis in high_threats:
                briefing += f"\n{analysis['competitor']}:\n"
                briefing += f"  Threat Level: {analysis['threat_level'].upper()}\n"
                briefing += f"  Impact: {analysis.get('overall_impact', 'N/A')}\n"
                if analysis.get('executive_summary'):
                    briefing += f"  Summary: {analysis['executive_summary']}\n"

                if analysis.get('threats'):
                    briefing += f"\n  Key Threats:\n"
                    for threat in analysis['threats'][:3]:
                        briefing += f"    • {threat}\n"

                if analysis.get('action_items'):
                    priority_actions = [a for a in analysis['action_items'] if a.get('priority') == 'high']
                    if priority_actions:
                        briefing += f"\n  Immediate Actions Required:\n"
                        for action in priority_actions:
                            briefing += f"    • {action['action']} ({action.get('department', 'N/A')})\n"

                briefing += "\n"

        # Medium priority section
        if medium_threats:
            briefing += "\n🟡 MEDIUM PRIORITY ITEMS\n"
            briefing += "-" * 70 + "\n"
            for analysis in medium_threats:
                briefing += f"\n{analysis['competitor']}: {analysis.get('executive_summary', 'N/A')}\n"

        # Opportunities
        all_opportunities = []
        for analysis in all_competitors_analysis:
            if analysis.get('opportunities'):
                all_opportunities.extend([(analysis['competitor'], opp) for opp in analysis['opportunities']])

        if all_opportunities:
            briefing += "\n\n🟢 MARKET OPPORTUNITIES\n"
            briefing += "-" * 70 + "\n"
            for competitor, opp in all_opportunities[:5]:
                briefing += f"  • [{competitor}] {opp}\n"

        # Strategic recommendations
        briefing += "\n\nSTRATEGIC RECOMMENDATIONS\n"
        briefing += "-" * 70 + "\n"
        all_recommendations = []
        for analysis in all_competitors_analysis:
            if analysis.get('strategic_recommendations'):
                all_recommendations.extend(analysis['strategic_recommendations'])

        for i, rec in enumerate(all_recommendations[:7], 1):
            briefing += f"{i}. {rec}\n"

        return briefing

    def get_action_items_by_priority(self, analyses: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Extract and organize all action items by priority.

        Returns:
            Dict with 'high', 'medium', 'low' priority lists
        """
        action_items = {'high': [], 'medium': [], 'low': []}

        for analysis in analyses:
            for item in analysis.get('action_items', []):
                priority = item.get('priority', 'low')
                item_copy = item.copy()
                item_copy['competitor'] = analysis['competitor']
                action_items[priority].append(item_copy)

        return action_items
