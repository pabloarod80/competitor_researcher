"""
Streamlit Web UI for AI-Powered Competitor Tracker

A user-friendly web interface for managing competitors and tracking updates.

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from competitor_tracker.database import CompetitorDB
from competitor_tracker.fetcher import NewsFetcher, DataEnricher
from competitor_tracker.analyzer import AIAnalyzer
from competitor_tracker.reporter import Reporter
from competitor_tracker.business_analyzer import BusinessImpactAnalyzer


# Page configuration
st.set_page_config(
    page_title="Competitor Tracker",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .competitor-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'db' not in st.session_state:
    st.session_state.db = CompetitorDB("competitors.db")

if 'config' not in st.session_state:
    st.session_state.config = {
        'enable_ai': False,
        'newsapi_key': None,
    }

if 'fetcher' not in st.session_state:
    st.session_state.fetcher = NewsFetcher(st.session_state.config)

if 'analyzer' not in st.session_state:
    st.session_state.analyzer = None  # Initialize when AI is enabled

if 'reporter' not in st.session_state:
    st.session_state.reporter = Reporter(st.session_state.db, st.session_state.analyzer)

if 'business_analyzer' not in st.session_state:
    st.session_state.business_analyzer = BusinessImpactAnalyzer(st.session_state.analyzer)


def home_page():
    """Dashboard/Home page."""
    st.markdown('<p class="main-header">📊 Competitor Tracker Dashboard</p>', unsafe_allow_html=True)

    # Get statistics
    stats = st.session_state.db.get_stats()

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="🏢 Total Competitors",
            value=stats['total_competitors']
        )

    with col2:
        st.metric(
            label="📰 Total News",
            value=stats['total_news']
        )

    with col3:
        st.metric(
            label="📦 Product Changes",
            value=stats['total_product_changes']
        )

    with col4:
        st.metric(
            label="🏛️ Company Updates",
            value=stats['total_company_updates']
        )

    st.markdown("---")

    # Recent activity
    st.subheader("📅 Recent Activity (Last 7 Days)")

    recent_updates = st.session_state.db.get_recent_updates(days=7)

    tab1, tab2, tab3 = st.tabs(["📰 News", "📦 Product Changes", "🏛️ Company Updates"])

    with tab1:
        news = recent_updates.get('news', [])
        if news:
            for item in news[:10]:
                with st.container():
                    st.markdown(f"**[{item.get('competitor_name', 'Unknown')}]** {item['title']}")
                    col_a, col_b, col_c = st.columns([2, 2, 1])
                    with col_a:
                        st.caption(f"📅 {item.get('fetched_at', 'Unknown date')[:10]}")
                    with col_b:
                        st.caption(f"📰 {item.get('source', 'Unknown source')}")
                    with col_c:
                        sentiment = item.get('sentiment', 'neutral')
                        emoji = "🟢" if sentiment == 'positive' else "🔴" if sentiment == 'negative' else "🟡"
                        st.caption(f"{emoji} {sentiment}")
                    if item.get('ai_summary'):
                        st.info(item['ai_summary'])
                    st.markdown("---")
        else:
            st.info("No news items found. Click 'Fetch Updates' to get started!")

    with tab2:
        products = recent_updates.get('product_changes', [])
        if products:
            for item in products:
                st.markdown(f"**[{item.get('competitor_name', 'Unknown')}]** {item.get('product_name', 'Unknown Product')}")
                st.caption(f"Change: {item.get('change_type', 'update')}")
                if item.get('description'):
                    st.write(item['description'])
                st.markdown("---")
        else:
            st.info("No product changes tracked yet.")

    with tab3:
        company = recent_updates.get('company_updates', [])
        if company:
            for item in company:
                st.markdown(f"**[{item.get('competitor_name', 'Unknown')}]** {item['title']}")
                st.caption(f"Type: {item.get('update_type', 'general')}")
                if item.get('description'):
                    st.write(item['description'])
                st.markdown("---")
        else:
            st.info("No company updates tracked yet.")


def add_competitor_page():
    """Page for adding new competitors."""
    st.markdown('<p class="main-header">➕ Add New Competitor</p>', unsafe_allow_html=True)

    with st.form("add_competitor_form"):
        st.subheader("Competitor Information")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Company Name *", placeholder="e.g., Acme Corp")
            website = st.text_input("Website", placeholder="https://example.com")
            industry = st.text_input("Industry", placeholder="e.g., Software, E-commerce")

        with col2:
            headquarters = st.text_input("Headquarters", placeholder="e.g., San Francisco, CA")
            employee_count = st.text_input("Employee Count", placeholder="e.g., 100-500")
            founded_date = st.text_input("Founded Date", placeholder="e.g., 2020")

        description = st.text_area("Description", placeholder="Brief description of the company...")

        keywords = st.text_input(
            "Tracking Keywords (comma-separated)",
            placeholder="e.g., AI, SaaS, product launch, funding",
            help="Keywords to help filter relevant news about this competitor"
        )

        submitted = st.form_submit_button("Add Competitor", type="primary")

        if submitted:
            if not name:
                st.error("⚠️ Company name is required!")
            else:
                try:
                    keyword_list = [k.strip() for k in keywords.split(',')] if keywords else None

                    comp_id = st.session_state.db.add_competitor(
                        name=name,
                        website=website or None,
                        description=description or None,
                        industry=industry or None,
                        tracking_keywords=keyword_list,
                        headquarters=headquarters or None,
                        employee_count=employee_count or None,
                        founded_date=founded_date or None
                    )

                    st.success(f"✅ Successfully added '{name}' (ID: {comp_id})")
                    st.balloons()

                except Exception as e:
                    st.error(f"❌ Error adding competitor: {e}")


def view_competitors_page():
    """Page for viewing and managing competitors."""
    st.markdown('<p class="main-header">🏢 Manage Competitors</p>', unsafe_allow_html=True)

    competitors = st.session_state.db.get_competitors()

    if not competitors:
        st.info("📭 No competitors tracked yet. Add your first competitor to get started!")
        return

    st.write(f"Tracking **{len(competitors)}** competitor(s)")

    # Search/filter
    search = st.text_input("🔍 Search competitors", placeholder="Search by name or industry...")

    if search:
        competitors = [c for c in competitors if
                      search.lower() in c['name'].lower() or
                      (c.get('industry') and search.lower() in c['industry'].lower())]

    # Display competitors
    for comp in competitors:
        with st.expander(f"🏢 {comp['name']}", expanded=False):
            col1, col2 = st.columns([3, 1])

            with col1:
                if comp.get('website'):
                    st.markdown(f"**🌐 Website:** [{comp['website']}]({comp['website']})")
                if comp.get('industry'):
                    st.markdown(f"**🏭 Industry:** {comp['industry']}")
                if comp.get('description'):
                    st.markdown(f"**📝 Description:** {comp['description']}")
                if comp.get('headquarters'):
                    st.markdown(f"**📍 Location:** {comp['headquarters']}")
                if comp.get('employee_count'):
                    st.markdown(f"**👥 Employees:** {comp['employee_count']}")
                if comp.get('tracking_keywords'):
                    keywords = ', '.join(comp['tracking_keywords'])
                    st.markdown(f"**🔑 Keywords:** {keywords}")

            with col2:
                st.markdown(f"**ID:** {comp['id']}")
                st.markdown(f"**Added:** {comp['created_at'][:10]}")

                # Action buttons
                if st.button(f"🗑️ Delete", key=f"delete_{comp['id']}"):
                    if st.session_state.get(f'confirm_delete_{comp["id"]}'):
                        st.session_state.db.delete_competitor(comp['id'])
                        st.success(f"Deleted {comp['name']}")
                        st.rerun()
                    else:
                        st.session_state[f'confirm_delete_{comp["id"]}'] = True
                        st.warning("Click again to confirm deletion")


def fetch_updates_page():
    """Page for fetching competitor updates."""
    st.markdown('<p class="main-header">🔄 Fetch Updates</p>', unsafe_allow_html=True)

    competitors = st.session_state.db.get_competitors()

    if not competitors:
        st.warning("⚠️ No competitors added yet. Add competitors first!")
        return

    st.write("Fetch the latest news and updates for your competitors.")

    col1, col2 = st.columns(2)

    with col1:
        selected_comp = st.selectbox(
            "Select Competitor",
            options=['All Competitors'] + [c['name'] for c in competitors]
        )

    with col2:
        days_back = st.slider("Days to look back", min_value=1, max_value=30, value=7)

    max_results = st.slider("Max results per competitor", min_value=5, max_value=50, value=10)

    if st.button("🔄 Fetch Updates", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        if selected_comp == 'All Competitors':
            comp_list = competitors
        else:
            comp_list = [c for c in competitors if c['name'] == selected_comp]

        total_fetched = 0

        for i, comp in enumerate(comp_list):
            status_text.text(f"Fetching updates for {comp['name']}...")
            progress_bar.progress((i + 1) / len(comp_list))

            try:
                keywords = comp.get('tracking_keywords', [])

                # Fetch news
                news_items = st.session_state.fetcher.fetch_competitor_news(
                    comp['name'],
                    keywords=keywords,
                    days_back=days_back,
                    max_results=max_results
                )

                # Process and store
                for item in news_items:
                    category = st.session_state.fetcher.categorize_news(
                        item.get('title', ''),
                        item.get('content', '')
                    )

                    sentiment = st.session_state.fetcher.analyze_sentiment(
                        f"{item.get('title', '')} {item.get('content', '')}"
                    )

                    ai_summary = None
                    if st.session_state.analyzer:
                        ai_summary = st.session_state.analyzer.summarize_article(
                            item.get('title', ''),
                            item.get('content', '')
                        )

                    st.session_state.db.add_news(
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

            except Exception as e:
                st.error(f"Error fetching for {comp['name']}: {e}")

        progress_bar.progress(1.0)
        status_text.text("")

        st.success(f"✅ Successfully fetched {total_fetched} updates!")

        if total_fetched > 0:
            st.balloons()


def reports_page():
    """Page for generating and viewing reports."""
    st.markdown('<p class="main-header">📊 Reports</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📅 Daily Report", "📆 Weekly Report", "👤 Competitor Profile"])

    with tab1:
        st.subheader("Daily Report")

        report_date = st.date_input("Select Date", value=datetime.now())
        report_format = st.selectbox("Format", ["Text", "HTML"], key="daily_format")

        if st.button("Generate Daily Report", key="gen_daily"):
            date_str = report_date.strftime('%Y-%m-%d')
            format_type = 'html' if report_format == 'HTML' else 'text'

            report = st.session_state.reporter.generate_daily_report(
                date=date_str,
                output_format=format_type
            )

            if format_type == 'html':
                st.components.v1.html(report, height=600, scrolling=True)
            else:
                st.text(report)

            # Download button
            st.download_button(
                label=f"📥 Download Report",
                data=report,
                file_name=f"daily_report_{date_str}.{'html' if format_type == 'html' else 'txt'}",
                mime='text/html' if format_type == 'html' else 'text/plain'
            )

    with tab2:
        st.subheader("Weekly Report")

        week_start = st.date_input("Week Start Date", value=datetime.now())
        week_format = st.selectbox("Format", ["Text", "HTML"], key="week_format")

        if st.button("Generate Weekly Report", key="gen_weekly"):
            date_str = week_start.strftime('%Y-%m-%d')
            format_type = 'html' if week_format == 'HTML' else 'text'

            report = st.session_state.reporter.generate_weekly_report(
                week_start=date_str,
                output_format=format_type
            )

            if format_type == 'html':
                st.components.v1.html(report, height=600, scrolling=True)
            else:
                st.text(report)

            st.download_button(
                label=f"📥 Download Report",
                data=report,
                file_name=f"weekly_report_{date_str}.{'html' if format_type == 'html' else 'txt'}",
                mime='text/html' if format_type == 'html' else 'text/plain'
            )

    with tab3:
        st.subheader("Competitor Profile")

        competitors = st.session_state.db.get_competitors()

        if competitors:
            selected = st.selectbox(
                "Select Competitor",
                options=[c['name'] for c in competitors],
                key="profile_comp"
            )

            days = st.slider("Days of history", 7, 90, 30, key="profile_days")

            if st.button("Generate Profile", key="gen_profile"):
                comp = next(c for c in competitors if c['name'] == selected)

                profile = st.session_state.reporter.generate_competitor_profile(
                    comp['id'],
                    days_back=days
                )

                st.text(profile)

                st.download_button(
                    label=f"📥 Download Profile",
                    data=profile,
                    file_name=f"profile_{comp['name'].replace(' ', '_')}.txt",
                    mime='text/plain'
                )
        else:
            st.info("No competitors added yet.")


def business_insights_page():
    """Business insights and AI-powered competitive intelligence page."""
    st.markdown('<p class="main-header">💡 Business Insights & Impact Analysis</p>', unsafe_allow_html=True)

    competitors = st.session_state.db.get_competitors()

    if not competitors:
        st.warning("⚠️ No competitors added yet. Add competitors first!")
        return

    # Check if AI is enabled
    ai_enabled = st.session_state.config.get('enable_ai', False) and st.session_state.analyzer is not None

    if not ai_enabled:
        st.info("💡 **AI Analysis is currently disabled.** Enable AI in Settings for enhanced insights, or view rule-based analysis below.")

    st.markdown("---")

    # Analysis options
    col1, col2 = st.columns([2, 1])

    with col1:
        analysis_type = st.radio(
            "Analysis Type",
            ["Individual Competitor Analysis", "Executive Briefing (All Competitors)"],
            horizontal=True
        )

    with col2:
        days_range = st.slider("Days of data", 7, 90, 30)

    st.markdown("---")

    if analysis_type == "Individual Competitor Analysis":
        # Individual competitor analysis
        selected_comp = st.selectbox(
            "Select Competitor to Analyze",
            options=[c['name'] for c in competitors]
        )

        company_context = st.text_area(
            "Your Business Context (Optional)",
            placeholder="e.g., We are a B2B SaaS company focused on enterprise customers...",
            help="Provide context about your business to get more relevant insights"
        )

        if st.button("🔍 Analyze Business Impact", type="primary"):
            comp = next(c for c in competitors if c['name'] == selected_comp)

            with st.spinner(f"Analyzing business impact of {selected_comp}..."):
                # Get recent updates
                updates = st.session_state.db.get_recent_updates(
                    days=days_range,
                    competitor_id=comp['id']
                )

                # Combine all updates
                all_updates = (
                    updates.get('news', []) +
                    updates.get('product_changes', []) +
                    updates.get('company_updates', [])
                )

                # Perform analysis
                analysis = st.session_state.business_analyzer.analyze_business_impact(
                    competitor_name=selected_comp,
                    updates=all_updates,
                    your_company_context=company_context if company_context else None
                )

                # Display results
                st.markdown("## Analysis Results")

                # Threat Level Alert
                threat_level = analysis.get('threat_level', 'low')
                if threat_level == 'critical':
                    st.error(f"🔴 **CRITICAL THREAT LEVEL** - Immediate attention required")
                elif threat_level == 'high':
                    st.warning(f"🟠 **HIGH THREAT LEVEL** - Priority monitoring needed")
                elif threat_level == 'medium':
                    st.info(f"🟡 **MEDIUM THREAT LEVEL** - Regular monitoring recommended")
                else:
                    st.success(f"🟢 **LOW THREAT LEVEL** - No immediate concerns")

                # Key metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Threat Level", threat_level.upper())
                with col2:
                    opp_level = analysis.get('opportunity_level', 'low')
                    st.metric("Opportunity Level", opp_level.upper())
                with col3:
                    impact = analysis.get('overall_impact', 'minimal')
                    st.metric("Overall Impact", impact.upper())

                # Executive Summary
                if analysis.get('executive_summary'):
                    st.markdown("### Executive Summary")
                    st.info(analysis['executive_summary'])

                # Key Findings
                if analysis.get('key_findings'):
                    st.markdown("### 📋 Key Findings")
                    for finding in analysis['key_findings']:
                        st.markdown(f"• {finding}")

                # Threats and Opportunities
                col1, col2 = st.columns(2)

                with col1:
                    if analysis.get('threats'):
                        st.markdown("### ⚠️ Threats")
                        for threat in analysis['threats']:
                            st.markdown(f"• {threat}")

                with col2:
                    if analysis.get('opportunities'):
                        st.markdown("### 🎯 Opportunities")
                        for opp in analysis['opportunities']:
                            st.markdown(f"• {opp}")

                # Strategic Recommendations
                if analysis.get('strategic_recommendations'):
                    st.markdown("### 💡 Strategic Recommendations")
                    for i, rec in enumerate(analysis['strategic_recommendations'], 1):
                        st.markdown(f"{i}. {rec}")

                # Action Items
                if analysis.get('action_items'):
                    st.markdown("### ✅ Action Items")

                    # Create a table for action items
                    action_data = []
                    for item in analysis['action_items']:
                        priority_emoji = "🔴" if item.get('priority') == 'high' else "🟡" if item.get('priority') == 'medium' else "🟢"
                        action_data.append({
                            'Priority': f"{priority_emoji} {item.get('priority', 'N/A').upper()}",
                            'Action': item.get('action', 'N/A'),
                            'Department': item.get('department', 'N/A'),
                            'Timeframe': item.get('timeframe', 'N/A')
                        })

                    if action_data:
                        df = pd.DataFrame(action_data)
                        st.dataframe(df, use_container_width=True, hide_index=True)

                # Market Implications
                if analysis.get('market_implications'):
                    st.markdown("### 🌐 Market Implications")
                    for impl in analysis['market_implications']:
                        st.markdown(f"• {impl}")

                # Download analysis
                st.markdown("---")
                import json
                analysis_json = json.dumps(analysis, indent=2)
                st.download_button(
                    label="📥 Download Analysis (JSON)",
                    data=analysis_json,
                    file_name=f"business_analysis_{selected_comp.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )

    else:
        # Executive briefing for all competitors
        if st.button("📊 Generate Executive Briefing", type="primary"):
            with st.spinner("Analyzing all competitors..."):
                all_analyses = []

                for comp in competitors:
                    # Get recent updates
                    updates = st.session_state.db.get_recent_updates(
                        days=days_range,
                        competitor_id=comp['id']
                    )

                    # Combine all updates
                    all_updates = (
                        updates.get('news', []) +
                        updates.get('product_changes', []) +
                        updates.get('company_updates', [])
                    )

                    # Perform analysis
                    analysis = st.session_state.business_analyzer.analyze_business_impact(
                        competitor_name=comp['name'],
                        updates=all_updates
                    )
                    all_analyses.append(analysis)

                # Generate briefing
                briefing = st.session_state.business_analyzer.generate_executive_briefing(all_analyses)

                st.markdown("## Executive Briefing")
                st.text(briefing)

                # Priority Action Items Dashboard
                st.markdown("---")
                st.markdown("## 🎯 Consolidated Action Items")

                action_items = st.session_state.business_analyzer.get_action_items_by_priority(all_analyses)

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("### 🔴 High Priority")
                    if action_items['high']:
                        for item in action_items['high']:
                            st.markdown(f"**{item.get('competitor')}**")
                            st.markdown(f"{item.get('action')}")
                            st.caption(f"{item.get('department')} • {item.get('timeframe')}")
                            st.markdown("---")
                    else:
                        st.info("No high priority actions")

                with col2:
                    st.markdown("### 🟡 Medium Priority")
                    if action_items['medium']:
                        for item in action_items['medium'][:5]:
                            st.markdown(f"**{item.get('competitor')}**")
                            st.markdown(f"{item.get('action')}")
                            st.caption(f"{item.get('department')} • {item.get('timeframe')}")
                            st.markdown("---")
                    else:
                        st.info("No medium priority actions")

                with col3:
                    st.markdown("### 🟢 Low Priority")
                    if action_items['low']:
                        for item in action_items['low'][:5]:
                            st.markdown(f"**{item.get('competitor')}**")
                            st.markdown(f"{item.get('action')}")
                            st.caption(f"{item.get('department')} • {item.get('timeframe')}")
                            st.markdown("---")
                    else:
                        st.info("No low priority actions")

                # Download briefing
                st.markdown("---")
                st.download_button(
                    label="📥 Download Executive Briefing",
                    data=briefing,
                    file_name=f"executive_briefing_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )


def settings_page():
    """Settings and configuration page."""
    st.markdown('<p class="main-header">⚙️ Settings</p>', unsafe_allow_html=True)

    st.subheader("Configuration")

    # AI Settings
    with st.expander("🤖 AI Settings", expanded=True):
        enable_ai = st.checkbox("Enable AI Analysis", value=st.session_state.config.get('enable_ai', False))

        if enable_ai:
            ai_provider = st.selectbox(
                "AI Provider",
                options=["openai", "anthropic", "local"],
                index=0
            )

            if ai_provider == "openai":
                api_key = st.text_input("OpenAI API Key", type="password")
                model = st.text_input("Model", value="gpt-3.5-turbo")
            elif ai_provider == "anthropic":
                api_key = st.text_input("Anthropic API Key", type="password")
                model = st.text_input("Model", value="claude-3-sonnet-20240229")
            else:
                api_key = None
                model = st.text_input("Model", value="llama2")
                ollama_url = st.text_input("Ollama URL", value="http://localhost:11434")

            if st.button("💾 Save AI Settings"):
                st.session_state.config['enable_ai'] = enable_ai
                st.session_state.config['ai_provider'] = ai_provider
                st.session_state.config['ai_model'] = model

                if ai_provider == "openai":
                    st.session_state.config['openai_api_key'] = api_key
                elif ai_provider == "anthropic":
                    st.session_state.config['anthropic_api_key'] = api_key
                else:
                    st.session_state.config['ollama_url'] = ollama_url

                # Reinitialize analyzer
                st.session_state.analyzer = AIAnalyzer(st.session_state.config)
                st.session_state.reporter = Reporter(st.session_state.db, st.session_state.analyzer)
                st.session_state.business_analyzer = BusinessImpactAnalyzer(st.session_state.analyzer)

                st.success("✅ AI settings saved!")

    # News API Settings
    with st.expander("📰 News API Settings"):
        st.write("Get a free API key from [newsapi.org](https://newsapi.org)")
        newsapi_key = st.text_input("NewsAPI Key", type="password")

        if st.button("💾 Save NewsAPI Key"):
            st.session_state.config['newsapi_key'] = newsapi_key
            st.session_state.fetcher = NewsFetcher(st.session_state.config)
            st.success("✅ NewsAPI key saved!")

    # Export Data
    st.markdown("---")
    st.subheader("📤 Export Data")

    col1, col2 = st.columns(2)

    with col1:
        export_format = st.selectbox("Export Format", ["CSV", "JSON"])

    with col2:
        export_days = st.number_input("Days to Export", min_value=1, max_value=365, value=30)

    if st.button("📥 Export Data"):
        import tempfile

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=f'.{export_format.lower()}') as f:
            if export_format == "CSV":
                st.session_state.reporter.export_to_csv(f.name, days_back=export_days)
            else:
                st.session_state.reporter.export_to_json(f.name, days_back=export_days)

            with open(f.name, 'r') as file:
                data = file.read()

            st.download_button(
                label=f"📥 Download {export_format}",
                data=data,
                file_name=f"competitor_data_{datetime.now().strftime('%Y%m%d')}.{export_format.lower()}",
                mime='text/csv' if export_format == 'CSV' else 'application/json'
            )


def main():
    """Main application."""

    # Sidebar navigation
    st.sidebar.title("🎯 Navigation")

    page = st.sidebar.radio(
        "Go to",
        ["🏠 Dashboard", "➕ Add Competitor", "🏢 Manage Competitors",
         "🔄 Fetch Updates", "💡 Business Insights", "📊 Reports", "⚙️ Settings"]
    )

    st.sidebar.markdown("---")

    # Quick stats in sidebar
    stats = st.session_state.db.get_stats()
    st.sidebar.metric("Competitors", stats['total_competitors'])
    st.sidebar.metric("Total News", stats['total_news'])
    st.sidebar.metric("News (24h)", stats['news_last_24h'])

    st.sidebar.markdown("---")
    st.sidebar.caption("AI-Powered Competitor Tracker")
    st.sidebar.caption("Built with Streamlit")

    # Route to pages
    if page == "🏠 Dashboard":
        home_page()
    elif page == "➕ Add Competitor":
        add_competitor_page()
    elif page == "🏢 Manage Competitors":
        view_competitors_page()
    elif page == "🔄 Fetch Updates":
        fetch_updates_page()
    elif page == "💡 Business Insights":
        business_insights_page()
    elif page == "📊 Reports":
        reports_page()
    elif page == "⚙️ Settings":
        settings_page()


if __name__ == '__main__':
    main()
