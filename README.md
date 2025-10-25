# AI-Powered Competitor Tracker

A comprehensive competitor analysis tool that automatically tracks news, product changes, and company updates with AI-powered insights and analysis.

## Features

- **Automated Tracking**: Daily and weekly tracking of competitor activities
- **AI-Powered Business Impact Analysis**:
  - Threat level assessment (Low/Medium/High/Critical)
  - Opportunity identification from competitor weaknesses
  - Strategic recommendations with actionable insights
  - Department-specific action items with priorities
  - Market implications and trend analysis
- **Executive Briefings**: AI-generated executive summaries consolidating all competitive intelligence
- **Multiple Data Sources**:
  - **Perplexity API** (recommended): News + Social Media (Twitter, Reddit, blogs)
  - NewsAPI: Traditional news aggregation
  - Google News RSS: Free fallback option
- **Social Media Monitoring**: Track competitor mentions on Twitter, Reddit, Hacker News, and LinkedIn (with Perplexity)
- **Smart Categorization**: Automatically categorizes updates (product, funding, partnerships, etc.)
- **Sentiment Analysis**: Tracks sentiment of competitor news
- **Flexible Reporting**: Daily briefings, weekly reports, and competitor profiles
- **Multiple Export Formats**: Export to CSV, JSON, HTML, and text
- **Database Storage**: SQLite database for historical tracking
- **Web UI**: User-friendly web interface with Business Insights dashboard
- **CLI Interface**: Powerful command-line interface for automation

## Two Ways to Use

### Option 1: Web UI (Recommended for Beginners)

Launch the web interface for an easy-to-use graphical interface:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

**Web UI Features:**
- Dashboard with real-time statistics
- Easy form to add competitors with name and URL
- Visual competitor management
- One-click update fetching
- Interactive reports with charts
- Export functionality

### Option 2: Command-Line Interface (CLI)

For automation and advanced users, use the powerful CLI:

```bash
python -m competitor_tracker [command] [options]
```

## Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Optional: Install AI providers (for enhanced features)
pip install openai  # For OpenAI GPT models
# or
pip install anthropic  # For Anthropic Claude models
```

### 2. Configuration

Edit `config.yaml` to configure your settings:

```yaml
# Enable AI features (optional)
enable_ai: true
ai_provider: openai
openai_api_key: your-api-key-here

# NewsAPI for better news fetching (optional)
newsapi_key: your-newsapi-key-here
```

### 3. Add Competitors

```bash
# Add your first competitor
python -m competitor_tracker add "Acme Corp" \
  --website https://acme.com \
  --industry "Software" \
  --keywords "SaaS,enterprise software"

# List all competitors
python -m competitor_tracker list
```

### 4. Fetch Updates

```bash
# Fetch updates for all competitors (last 7 days)
python -m competitor_tracker fetch

# Fetch updates for specific competitor
python -m competitor_tracker fetch --competitor-id 1 --days 7
```

### 5. Generate Reports

```bash
# Daily report
python -m competitor_tracker report daily

# Weekly report in HTML format
python -m competitor_tracker report weekly --format html --output report.html

# Competitor profile
python -m competitor_tracker report profile --competitor-id 1
```

## Using the Web UI

The web interface provides an intuitive way to manage your competitor tracking:

### Starting the Web UI

```bash
# Install dependencies first
pip install -r requirements.txt

# Launch the web interface
streamlit run app.py
```

Open your browser to `http://localhost:8501`

### Web UI Pages

**Dashboard**
- View real-time statistics
- See recent news, product changes, and company updates
- Monitor activity across all competitors

**Add Competitor**
- Simple form to add new competitors
- Required: Company Name
- Optional: Website, Industry, Description, Keywords, Location, etc.
- One-click submission

**Manage Competitors**
- View all tracked competitors
- Search and filter by name or industry
- View detailed information for each competitor
- Delete competitors with confirmation

**Fetch Updates**
- Select specific competitor or fetch for all
- Choose how many days back to search
- Set maximum results per competitor
- **Optional: Include Social Media** (Twitter, Reddit, etc. with Perplexity)
- Progress bar shows real-time status
- Automatic categorization and sentiment analysis
- Intelligent source fallback (Perplexity → NewsAPI → Google News)

**Business Insights** 💡 (NEW!)
- **AI-Powered Impact Analysis**: Analyze threat level and business impact of each competitor
- **Threat Assessment**: Get low/medium/high/critical threat ratings
- **Opportunity Identification**: Find market opportunities from competitor weaknesses
- **Strategic Recommendations**: Receive AI-generated strategic advice
- **Action Items Dashboard**: Prioritized action items by department and timeframe
- **Executive Briefings**: Consolidated analysis across all competitors
- **Your Business Context**: Optionally provide your business context for tailored insights
- Works with or without AI (rule-based fallback available)

**Reports**
- Generate daily reports for any date
- Create weekly summaries
- Build detailed competitor profiles
- Choose text or HTML format
- Download reports directly from browser

**Settings**
- Configure AI providers (OpenAI, Anthropic, or local models)
- Add NewsAPI key for better news coverage
- Export all data to CSV or JSON
- Manage system configuration

### Web UI Screenshots

The interface includes:
- Clean, modern design
- Responsive layout
- Real-time updates
- Progress indicators
- Download buttons for all reports
- Color-coded sentiment indicators

## CLI Usage Examples

### Adding Competitors

```bash
# Basic competitor
python -m competitor_tracker add "Competitor Inc"

# With full details
python -m competitor_tracker add "Tech Rival" \
  --website https://techrival.com \
  --industry "Cloud Computing" \
  --description "Cloud infrastructure provider" \
  --keywords "cloud,infrastructure,DevOps"
```

### Fetching Updates

```bash
# Fetch last 7 days of updates
python -m competitor_tracker fetch --days 7

# Fetch with custom limits
python -m competitor_tracker fetch --days 14 --max-results 20

# Fetch for specific competitor
python -m competitor_tracker fetch --competitor-id 1
```

### Generating Reports

```bash
# Daily report (text format)
python -m competitor_tracker report daily

# Daily report for specific date
python -m competitor_tracker report daily --date 2024-10-25

# Weekly report
python -m competitor_tracker report weekly

# Weekly report in JSON format
python -m competitor_tracker report weekly --format json --output weekly.json

# Competitor profile (30 days of history)
python -m competitor_tracker report profile --competitor-id 1 --days 30
```

### Exporting Data

```bash
# Export to CSV (last 30 days)
python -m competitor_tracker export data.csv --format csv --days 30

# Export to JSON
python -m competitor_tracker export data.json --format json --days 60
```

### Other Commands

```bash
# Show statistics
python -m competitor_tracker stats

# Delete competitor
python -m competitor_tracker delete 1

# Delete without confirmation
python -m competitor_tracker delete 1 --force
```

## Configuration Options

### AI Providers

The tool supports multiple AI providers for enhanced analysis:

#### OpenAI (GPT-3.5/GPT-4)

```yaml
enable_ai: true
ai_provider: openai
ai_model: gpt-3.5-turbo
openai_api_key: your-api-key-here
```

#### Anthropic (Claude)

```yaml
enable_ai: true
ai_provider: anthropic
ai_model: claude-3-sonnet-20240229
anthropic_api_key: your-api-key-here
```

#### Local Models (Ollama)

```yaml
enable_ai: true
ai_provider: local
ai_model: llama2
ollama_url: http://localhost:11434
```

### News Sources

The system supports multiple news sources with automatic fallback:

#### Perplexity API (⭐ Recommended)

**Best option for comprehensive intelligence gathering!**

Perplexity provides AI-powered search across:
- News articles from thousands of sources
- Social media (Twitter, Reddit, LinkedIn, Hacker News)
- Blog posts and industry publications
- Company announcements and press releases
- Real-time web search

Get your API key at [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api)

```yaml
perplexity_api_key: pplx-your-api-key-here
perplexity_model: llama-3.1-sonar-large-128k-online
```

**Why Perplexity?**
- Searches across news AND social media
- AI-powered understanding of queries
- Real-time and recent information
- Better at finding product launches and company changes
- Includes source citations

**Cost:** ~$0.005 per search (200 searches for $1)

#### NewsAPI (Alternative)

Traditional news aggregator with good coverage:

Get a free API key from [newsapi.org](https://newsapi.org):

```yaml
newsapi_key: your-newsapi-key-here
```

#### Google News RSS (Free Fallback)

Default fallback source. Works without any configuration. Limited to news articles only.

## Database Schema

The tool uses SQLite with the following tables:

- **competitors**: Company information and tracking settings
- **news**: News articles and updates
- **product_changes**: Product launches, updates, and changes
- **company_updates**: Corporate news (funding, acquisitions, leadership)
- **tracking_history**: Historical tracking data

## Architecture

### Modules

- **database.py**: SQLite database operations
- **fetcher.py**: News fetching from various sources
- **analyzer.py**: AI-powered analysis and summarization
- **reporter.py**: Report generation and data export
- **cli.py**: Command-line interface

### Data Flow

1. **Fetch**: Retrieve news from sources (Google News, NewsAPI)
2. **Categorize**: Classify updates (product, funding, partnership, etc.)
3. **Analyze**: AI summarization and sentiment analysis
4. **Store**: Save to SQLite database
5. **Report**: Generate daily/weekly reports

## Business Impact Analysis

The system provides AI-powered competitive intelligence to help you understand how competitor actions affect your business and what you should do about it.

### How It Works

1. **Data Collection**: System fetches and categorizes competitor news, product changes, and company updates
2. **AI Analysis**: Analyzes updates for business impact using AI (or rule-based fallback)
3. **Threat Assessment**: Assigns threat levels (Low/Medium/High/Critical)
4. **Opportunity Identification**: Finds market opportunities from competitor weaknesses
5. **Strategic Recommendations**: Generates specific, actionable recommendations
6. **Action Items**: Creates prioritized action items with departments and timeframes

### What You Get

**For Each Competitor:**
- **Threat Level**: Low, Medium, High, or Critical
- **Opportunity Level**: Assessment of exploitable weaknesses
- **Executive Summary**: 2-3 sentence overview of the situation
- **Key Findings**: 3-5 specific insights about competitor activity
- **Threats**: Specific risks to your business and why they matter
- **Opportunities**: Ways to capitalize on competitor weaknesses
- **Strategic Recommendations**: What your company should do strategically
- **Action Items**: Specific tasks with:
  - Priority (High/Medium/Low)
  - Action description
  - Responsible department
  - Timeframe

**Executive Briefing (All Competitors):**
- High-priority threats summary
- Medium-priority monitoring items
- Market opportunities across all competitors
- Consolidated action items by priority
- Overall strategic recommendations

### Example Analysis Output

```
🔴 HIGH THREAT LEVEL - Priority monitoring needed

Threat Level: HIGH
Opportunity Level: MEDIUM
Overall Impact: SIGNIFICANT

Executive Summary:
Competitor X announced $50M Series B funding and launched 3 new enterprise features.
High threat due to increased resources and product acceleration. However, negative
customer sentiment presents an opportunity.

Key Findings:
• Secured $50M Series B from top-tier investors
• Launched AI-powered analytics feature directly competing with our core offering
• Customer reviews show frustration with implementation complexity

Threats:
• New funding enables aggressive sales and marketing expansion
• AI analytics feature matches 80% of our functionality at lower price point

Opportunities:
• Poor implementation experience creating customer churn
• No white-glove onboarding service (our differentiator)

Strategic Recommendations:
1. Accelerate AI feature development to maintain technical lead
2. Double down on customer success and implementation support
3. Launch competitive positioning campaign highlighting ease of implementation

Action Items:
Priority  | Action                                    | Department  | Timeframe
----------|-------------------------------------------|-------------|------------
HIGH      | Review and enhance AI feature roadmap     | Product     | This week
HIGH      | Competitive battle card for sales team    | Marketing   | This week
MEDIUM    | Customer success expansion plan           | Operations  | This month
```

### Using Business Insights in the Web UI

1. Navigate to **💡 Business Insights**
2. Choose analysis type:
   - **Individual Competitor**: Deep dive on one competitor
   - **Executive Briefing**: Overview of all competitors
3. Optionally add your business context for tailored insights
4. Click "Analyze Business Impact"
5. Review results: threats, opportunities, recommendations, action items
6. Download analysis as JSON for sharing

### Enabling AI for Enhanced Analysis

The Business Impact Analysis works in two modes:

**With AI (Recommended):**
- More sophisticated analysis
- Context-aware recommendations
- Natural language insights
- Customized to your business context

**Without AI (Rule-Based):**
- Still functional and useful
- Keyword-based threat detection
- Pattern-based opportunity identification
- Generic but actionable recommendations

To enable AI:
1. Go to **⚙️ Settings**
2. Enable AI Analysis
3. Choose provider (OpenAI, Anthropic, or local)
4. Add API key
5. Save settings

## Advanced Features

### Automated Daily/Weekly Tracking

Set up cron jobs for automated tracking:

```bash
# Daily fetch at 8 AM
0 8 * * * cd /path/to/tracker && python -m competitor_tracker fetch

# Daily report at 9 AM
0 9 * * * cd /path/to/tracker && python -m competitor_tracker report daily --output /tmp/daily.txt

# Weekly report on Monday at 9 AM
0 9 * * 1 cd /path/to/tracker && python -m competitor_tracker report weekly --format html --output /tmp/weekly.html
```

### Custom Keywords

Track specific topics by adding keywords:

```bash
python -m competitor_tracker add "Competitor" \
  --keywords "AI,machine learning,product launch,funding,acquisition"
```

### Integration with Other Tools

Export data for use in other tools:

```bash
# Export to CSV for Excel/Google Sheets
python -m competitor_tracker export competitors.csv --format csv

# Export to JSON for programmatic access
python -m competitor_tracker export competitors.json --format json
```

## Roadmap

- [ ] Email notifications for important updates
- [ ] Slack/Discord integration
- [ ] Web dashboard
- [ ] More data sources (Twitter, LinkedIn, Product Hunt)
- [ ] Automated competitive analysis reports
- [ ] Machine learning for trend detection
- [ ] Multi-language support

## Troubleshooting

### No updates found

- Check your internet connection
- Verify competitor names are spelled correctly
- Try increasing `--days` parameter
- Consider adding NewsAPI key for better coverage

### AI features not working

- Verify API keys are correct in `config.yaml`
- Check that AI provider library is installed
- Ensure `enable_ai: true` in config

### Database errors

- Delete `competitors.db` and restart (will lose data)
- Check file permissions
- Ensure SQLite is available

## License

MIT License - feel free to use and modify for your needs.

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.
