# AI-Powered Competitor Tracker - Installation & Testing Guide

Complete step-by-step instructions to install, configure, and test your new competitor tracking system.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Basic Configuration](#basic-configuration)
4. [Optional: API Keys Setup](#optional-api-keys-setup)
5. [Testing the System](#testing-the-system)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required
- **Python 3.8 or higher**
- **Git** (to clone the repository)
- **Terminal/Command Prompt** access

### Check Your Python Version
```bash
python --version
# or
python3 --version
```

Should show: `Python 3.8.x` or higher

---

## Installation

### Step 1: Clone or Navigate to the Repository

If you already have the code:
```bash
cd /path/to/git_test
```

If you need to clone it:
```bash
git clone <your-repo-url>
cd git_test
```

### Step 2: Create a Virtual Environment (Recommended)

**On Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- requests (for fetching news)
- PyYAML (for configuration)
- streamlit (for web UI)
- pandas (for data handling)

**Wait for installation to complete** (30-60 seconds)

### Step 4: Verify Installation

```bash
python -c "import streamlit; print('Streamlit installed successfully!')"
```

Should print: `Streamlit installed successfully!`

---

## Basic Configuration

### Step 5: Review Configuration File

Open `config.yaml` in a text editor:

```bash
# Linux/Mac
nano config.yaml

# Or use any text editor
code config.yaml  # VS Code
vim config.yaml   # Vim
```

**Default configuration works out of the box!** No changes needed for basic testing.

```yaml
# Competitor Tracker Configuration

# Database settings
database: competitors.db

# Enable AI-powered analysis
enable_ai: false  # Start with this disabled

# Tracking Settings
default_fetch_days: 7
default_max_results: 10
```

**Save and close** the file (in nano: Ctrl+X, then Y, then Enter)

---

## Optional: API Keys Setup

You can test the system WITHOUT any API keys using Google News RSS (free).
Add these later for enhanced features.

### Option A: Perplexity API (Recommended - Best Results)

**What you get:** News + Social Media (Twitter, Reddit, etc.)

1. Go to https://www.perplexity.ai/settings/api
2. Sign up and get your API key (starts with `pplx-`)
3. Edit `config.yaml`:

```yaml
# Uncomment and add your key:
perplexity_api_key: pplx-your-actual-key-here
perplexity_model: llama-3.1-sonar-large-128k-online
```

**Cost:** ~$0.005 per search (200 searches for $1)

### Option B: AI Analysis (OpenAI or Anthropic)

**What you get:** AI-powered business impact analysis and recommendations

**For OpenAI:**
1. Go to https://platform.openai.com/api-keys
2. Create an API key
3. Edit `config.yaml`:

```yaml
enable_ai: true
ai_provider: openai
ai_model: gpt-3.5-turbo
openai_api_key: sk-your-actual-key-here
```

**For Anthropic Claude:**
1. Go to https://console.anthropic.com/
2. Get API key
3. Edit `config.yaml`:

```yaml
enable_ai: true
ai_provider: anthropic
ai_model: claude-3-sonnet-20240229
anthropic_api_key: sk-ant-your-actual-key-here
```

### Option C: NewsAPI (Alternative to Perplexity)

**What you get:** Traditional news aggregation

1. Go to https://newsapi.org/
2. Sign up for free API key
3. Edit `config.yaml`:

```yaml
newsapi_key: your-newsapi-key-here
```

**Note:** You can skip all API keys for initial testing!

---

## Testing the System

### Test 1: Launch the Web UI

```bash
streamlit run app.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**Open your browser** and go to: `http://localhost:8501`

You should see the **Competitor Tracker Dashboard**!

✅ **Success indicator:** You see the dashboard with navigation sidebar

❌ **If it fails:** See [Troubleshooting](#troubleshooting) below

---

### Test 2: Add Your First Competitor

**In the Web UI:**

1. Click **"➕ Add Competitor"** in the sidebar
2. Fill in the form:
   - **Company Name:** `OpenAI`
   - **Website:** `https://openai.com`
   - **Industry:** `Artificial Intelligence`
   - **Keywords:** `GPT, ChatGPT, AI, machine learning`
3. Click **"Add Competitor"** button

✅ **Success indicator:** You see "Successfully added 'OpenAI'" with balloons animation

4. **Add a second competitor** (repeat above):
   - **Company Name:** `Anthropic`
   - **Website:** `https://anthropic.com`
   - **Industry:** `Artificial Intelligence`
   - **Keywords:** `Claude, AI safety, LLM`

---

### Test 3: View Competitors

1. Click **"🏢 Manage Competitors"** in sidebar
2. You should see both competitors listed
3. Click the expander to see details

✅ **Success indicator:** Both OpenAI and Anthropic are visible with all details

---

### Test 4: Fetch News Updates

1. Click **"🔄 Fetch Updates"** in sidebar
2. Select **"All Competitors"** from dropdown
3. Set **"Days to look back"** to `7`
4. Set **"Max results"** to `10`
5. Click **"🔄 Fetch Updates"** button

**What happens:**
- Progress bar appears
- Status shows "Fetching updates for OpenAI..."
- Then "Fetching updates for Anthropic..."
- Success message with total count

✅ **Success indicator:** "Successfully fetched X updates!" with balloons

**Note:** This uses Google News RSS (free, no API key needed)

---

### Test 5: View Dashboard

1. Click **"🏠 Dashboard"** in sidebar
2. Check the metrics at the top:
   - Total Competitors: 2
   - Total News: (should be > 0)
3. Scroll down to see recent news items

✅ **Success indicator:** You see news articles for OpenAI and Anthropic

---

### Test 6: Generate a Report

1. Click **"📊 Reports"** in sidebar
2. Select **"📅 Daily Report"** tab
3. Choose today's date
4. Format: **Text**
5. Click **"Generate Daily Report"**

✅ **Success indicator:** You see a formatted report with news items

6. Try **"👤 Competitor Profile"** tab:
   - Select **OpenAI**
   - Click **"Generate Profile"**

✅ **Success indicator:** Detailed profile of OpenAI with activity summary

---

### Test 7: Business Insights (Basic Version)

1. Click **"💡 Business Insights"** in sidebar
2. Select **"Individual Competitor Analysis"**
3. Choose **OpenAI**
4. (Optional) Add business context: `We are an AI startup building enterprise tools`
5. Click **"🔍 Analyze Business Impact"**

**What happens:**
- System analyzes recent OpenAI news
- Generates threat assessment
- Provides recommendations

✅ **Success indicator:** You see threat level, key findings, and action items

**Note:** Without AI enabled, you get rule-based analysis (still useful!)

---

### Test 8: Export Data

1. Go to **"⚙️ Settings"**
2. Scroll to **"📤 Export Data"**
3. Select **CSV** format
4. Days: **30**
5. Click **"📥 Export Data"**
6. Download the file

✅ **Success indicator:** CSV file downloads with your competitor data

---

## Testing Advanced Features (With API Keys)

### Test 9: Perplexity Social Media Search (If You Have API Key)

1. Go to **"⚙️ Settings"**
2. Expand **"🔍 Perplexity API Settings"**
3. Enter your API key
4. Select model: `llama-3.1-sonar-large-128k-online`
5. Click **"💾 Save Perplexity Settings"**

Then:

6. Go to **"🔄 Fetch Updates"**
7. Select **OpenAI**
8. Check **"🐦 Include Social Media"** (this option now appears!)
9. Click **"🔄 Fetch Updates"**

✅ **Success indicator:** You get news + social media mentions from Twitter, Reddit, etc.

---

### Test 10: AI Business Analysis (If You Have OpenAI/Anthropic Key)

1. Go to **"⚙️ Settings"**
2. Expand **"🤖 AI Settings"**
3. Check **"Enable AI Analysis"**
4. Select provider (OpenAI or Anthropic)
5. Enter API key
6. Enter model name
7. Click **"💾 Save AI Settings"**

Then:

8. Go to **"💡 Business Insights"**
9. Select **OpenAI**
10. Add context: `We are a B2B SaaS company targeting enterprises`
11. Click **"🔍 Analyze Business Impact"**

✅ **Success indicator:** Much more sophisticated analysis with AI-generated insights!

---

## CLI Testing (Optional)

Test the command-line interface:

### Add a competitor via CLI:
```bash
python -m competitor_tracker add "Google DeepMind" \
  --website https://deepmind.google \
  --industry "Artificial Intelligence"
```

### List all competitors:
```bash
python -m competitor_tracker list
```

### Fetch updates:
```bash
python -m competitor_tracker fetch --days 7
```

### Generate daily report:
```bash
python -m competitor_tracker report daily
```

### View statistics:
```bash
python -m competitor_tracker stats
```

✅ **Success indicator:** All commands work without errors

---

## Verification Checklist

After completing all tests, verify:

- [ ] Web UI launches successfully
- [ ] Can add competitors via web form
- [ ] Can view competitors list
- [ ] Can fetch news updates (even without API keys)
- [ ] Dashboard shows statistics
- [ ] Can generate reports
- [ ] Can perform business impact analysis
- [ ] Can export data to CSV/JSON
- [ ] Database file `competitors.db` exists
- [ ] (Optional) Social media search works with Perplexity
- [ ] (Optional) AI analysis works with OpenAI/Anthropic

---

## Troubleshooting

### Issue: "streamlit: command not found"

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall streamlit
pip install streamlit
```

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
# Install requirements again
pip install -r requirements.txt
```

### Issue: Web UI won't open in browser

**Solution:**
1. Check the terminal output for the URL
2. Manually open: `http://localhost:8501`
3. Try: `http://127.0.0.1:8501`
4. Check if port 8501 is already in use:
   ```bash
   # Kill existing streamlit processes
   pkill -f streamlit
   # Try again
   streamlit run app.py
   ```

### Issue: "No news found" when fetching

**Solutions:**
1. Check internet connection
2. Try a different competitor name (e.g., "Microsoft", "Apple")
3. Increase "Days to look back" slider
4. Add a NewsAPI or Perplexity key for better results

### Issue: Database errors

**Solution:**
```bash
# Delete and recreate database
rm competitors.db
# Restart the app - it will recreate the database
streamlit run app.py
```

### Issue: Import errors with perplexity_fetcher

**Solution:**
This is normal if you don't have Perplexity configured. The system will fall back to Google News RSS automatically.

### Issue: AI analysis fails

**Solutions:**
1. Verify API key is correct
2. Check you have API credits/balance
3. Try without AI (rule-based analysis still works)
4. Check terminal for specific error messages

### Issue: Port already in use

**Solution:**
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

---

## Quick Start Script

Create a file `quick_test.sh` for rapid testing:

```bash
#!/bin/bash

echo "🚀 Starting Competitor Tracker Quick Test..."

# Activate virtual environment
source venv/bin/activate

# Launch web UI
echo "📊 Launching Web UI..."
streamlit run app.py

# Note: Press Ctrl+C to stop
```

Make it executable:
```bash
chmod +x quick_test.sh
./quick_test.sh
```

---

## What to Test First

**Recommended testing order:**

1. ✅ **Start here:** Basic web UI (no API keys needed)
2. ✅ **Next:** Add competitors and fetch news with Google News RSS
3. ✅ **Then:** Generate reports and exports
4. ⭐ **Optional:** Add Perplexity for social media
5. ⭐ **Optional:** Add AI for business analysis

---

## Getting Help

If you encounter issues:

1. Check the terminal output for error messages
2. Review the [Troubleshooting](#troubleshooting) section
3. Check `config.yaml` for typos
4. Verify Python version is 3.8+
5. Try in a fresh virtual environment

---

## Next Steps After Testing

Once everything works:

1. **Set up automation:**
   ```bash
   # Add to crontab for daily updates
   0 8 * * * cd /path/to/git_test && source venv/bin/activate && python -m competitor_tracker fetch
   ```

2. **Add more competitors** relevant to your business

3. **Configure API keys** for enhanced features

4. **Schedule reports:**
   ```bash
   # Daily report email
   0 9 * * * cd /path/to/git_test && source venv/bin/activate && python -m competitor_tracker report daily --output /tmp/daily.txt
   ```

5. **Explore the Business Insights** page for strategic analysis

---

## Success Criteria

✅ **Your installation is successful if:**
- Web UI loads at http://localhost:8501
- You can add and view competitors
- News fetching works (even with Google News RSS)
- Reports generate successfully
- Database persists data between sessions

---

**Congratulations!** You now have a fully functional AI-powered competitor tracking system! 🎉
