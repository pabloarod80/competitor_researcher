# AI-Powered Competitor Tracker

A comprehensive competitor analysis tool that automatically tracks news, product changes, and company updates with AI-powered insights and analysis.

## Features

- **Automated Tracking**: Daily and weekly tracking of competitor activities
- **AI-Powered Analysis**: Intelligent summarization and competitive impact analysis
- **Multiple Data Sources**: Fetches news from Google News, NewsAPI, and more
- **Smart Categorization**: Automatically categorizes updates (product, funding, partnerships, etc.)
- **Sentiment Analysis**: Tracks sentiment of competitor news
- **Flexible Reporting**: Daily briefings, weekly reports, and competitor profiles
- **Multiple Export Formats**: Export to CSV, JSON, HTML, and text
- **Database Storage**: SQLite database for historical tracking
- **CLI Interface**: Easy-to-use command-line interface

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

## Usage Examples

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

#### Google News RSS (Free, no API key required)

Default fallback source. Works without any configuration.

#### NewsAPI (Recommended)

For better news coverage, get a free API key from [newsapi.org](https://newsapi.org):

```yaml
newsapi_key: your-newsapi-key-here
```

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
