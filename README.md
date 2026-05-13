<p align="center">
  <img src="https://raw.githubusercontent.com/radishsoups/the-paper-boy/main/workflows/images/icon.png" width="90" />
</p>

# the paper boy

An AI-powered news summarization system that automatically fetches tech news articles, summarizes key insights using Google's Gemini model, and delivers daily digests right to your email inbox.

## Features

- **Automated News Fetching**: Retrieves curated tech news articles daily
- **AI Summarization**: Uses Google Gemini 2.5 Flash to intelligently summarize tech trends, AI developments, and company updates
- **Email Delivery**: Sends beautifully formatted HTML email summaries
- **Scheduled Execution**: Runs automatically at 8:00 AM daily via APScheduler
- **REST API**: Trigger news summaries on-demand via FastAPI endpoint
- **Agent-Based Architecture**: Built on Google's Agent Development Kit (ADK)

## Project Structure

```
agent/
├── agents/
│   └── news_agent.py         # AI agent for news summarization
├── api/
│   └── main.py               # FastAPI application
├── services/
│   ├── email_service.py      # Email sending functionality
│   └── news_fetcher.py       # News retrieval service
├── workflows/
│   └── run_daily_news.py     # Main workflow orchestration
├── scheduler.py              # APScheduler configuration
├── package.json              # Node.js dependencies
└── README.md                 # This file
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 16+ (for Google ADK devtools)
- Google Cloud account with Gemini API access
- Email service credentials (SMTP or mail service API)

### 1. Clone and Navigate to Project

```bash
cd agent
```

### 2. Create Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install fastapi uvicorn apscheduler google-adk python-dotenv
```

### 4. Install Node.js Dependencies

```bash
npm install
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Google Gemini API
GOOGLE_API_KEY=your_google_api_key_here

# Email Configuration
SMTP_SERVER=your_smtp_server
SMTP_PORT=587
EMAIL_FROM=your_email@example.com
EMAIL_PASSWORD=your_email_password
RECIPIENT_EMAIL=target@example.com

# Optional: News API Configuration
NEWS_API_KEY=your_news_api_key_here
```

## Usage

### Option 1: Run with Scheduler (Automatic Daily)

```bash
python scheduler.py
```

This starts the scheduler that runs the news summarization every day at 8:00 AM.

### Option 2: Run FastAPI Server (On-Demand)

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

**Trigger news summary:**
```bash
curl http://localhost:8000/run-news
```

### Option 3: Manual Execution

```bash
python -c "from workflows.run_daily_news import run_daily_news; import asyncio; asyncio.run(run_daily_news('2024-05-13'))"
```

## How It Works

1. **News Fetching**: The `news_fetcher` service retrieves relevant tech news articles
2. **AI Summarization**: Articles are processed through the `news_agent` which uses Gemini to:
   - Summarize key tech trends
   - Highlight AI developments
   - Include major company updates
3. **Email Formatting**: Summary is formatted as HTML email
4. **Delivery**: Email is sent to configured recipient

## API Endpoints

- `GET /run-news` - Triggers immediate news summarization and delivery for today's date

## Configuration

### Scheduled Execution Time

Edit `scheduler.py` to change the daily run time:

```python
scheduler.add_job(
    lambda: run_daily_news(str(date.today())),
    "cron",
    hour=8,      # Change hour (0-23)
    minute=0,    # Change minute (0-59)
)
```

### News Summarization Prompt

Customize the summarization behavior by editing `CLASSIFICATION_INSTRUCTION` in `agents/news_agent.py`.

## Requirements

- **google-adk**: ^1.1.0 (Agent Development Kit)
- **fastapi**: Latest
- **uvicorn**: Latest (ASGI server)
- **apscheduler**: Latest (Task scheduling)
- **python-dotenv**: Latest (Environment configuration)

## Troubleshooting

**Issue**: "API key not found"
- Ensure `.env` file exists in project root with valid `GOOGLE_API_KEY`

**Issue**: "Email not sending"
- Verify SMTP credentials in `.env`
- Check firewall/port 587 is accessible
- For Gmail, use App Passwords instead of account password

**Issue**: "No JSON found in output"
- Check Gemini API response format
- Verify agent instruction prompt is properly configured
