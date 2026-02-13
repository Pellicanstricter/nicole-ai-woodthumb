# Nicole 🪵

**Unified AI Customer Service Agent for Wood Thumb**

Nicole is a custom-built AI customer service system that handles both website chat and email inquiries for Wood Thumb, a community woodshop in Oakland, California. Built with Claude API (Anthropic), FastAPI, and Google Apps Script.

## Why Nicole?

- **$5-20/month** vs $79-165/month for Intercom/Zendesk
- Fully customized to Wood Thumb's brand voice and offerings
- Single AI brain, multiple channels (chat + email, expandable to SMS/Instagram)
- Intelligent routing: auto-send high-confidence replies, draft medium-confidence, flag complex requests
- Complete control over data, responses, and behavior

## Architecture

```
┌─────────────────────────────────────────────────┐
│          INBOUND CHANNELS                       │
├─────────────────────────────────────────────────┤
│  💬 Website Chat    │  📧 Gmail    │  📱 Future │
└──────────┬──────────┴──────┬───────┴────────────┘
           │                 │
           ▼                 ▼
┌─────────────────────────────────────────────────┐
│       NICOLE CORE ENGINE (FastAPI)              │
├─────────────────────────────────────────────────┤
│  🧠 Intent Classifier                           │
│  📚 Knowledge Base (Wood Thumb content)         │
│  🤖 Response Generator (Claude Sonnet)          │
│  🔀 Response Router (confidence-based)          │
└──────────┬──────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────┐
│          OUTBOUND ACTIONS                       │
├─────────────────────────────────────────────────┤
│  💬 Chat Reply  │  📤 Auto-Send  │  📝 Draft    │
│  🔔 Owner Alert │  🔗 Booking Links             │
└─────────────────────────────────────────────────┘
```

## Features

### For Customers
- **Instant answers** via website chat widget
- **24/7 availability** for common questions
- Warm, friendly Wood Thumb brand voice
- Direct booking links to Acuity scheduling
- Seamless handoff to owner for complex requests

### For Wood Thumb Owner
- **Automated email triage**
  - High confidence → Auto-send
  - Medium confidence → Save as draft for review
  - Low confidence → Flag with summary
- **Gmail integration** checks inbox every 5 minutes
- **Conversation logging** (optional Google Sheets)
- Zero maintenance after setup

## Project Structure

```
nicole/
├── api/                    # FastAPI application
│   ├── main.py            # App entry, routes, CORS
│   ├── chat.py            # Chat endpoint (streaming support)
│   ├── email.py           # Email endpoint
│   ├── nicole.py          # Core AI logic
│   ├── prompts.py         # System prompt + knowledge base
│   ├── intents.py         # Intent classification
│   └── config.py          # Settings (env vars)
│
├── widget/                 # Chat widget
│   ├── nicole-widget.js   # Vanilla JS widget
│   └── nicole-widget.css  # Wood Thumb themed styles
│
├── gmail/                  # Google Apps Script
│   ├── Code.gs            # Email processing logic
│   ├── Config.gs          # Settings
│   └── README.md          # Setup instructions
│
├── knowledge/              # Knowledge base
│   ├── scraper.py         # Web scraper
│   └── woodthumb.md       # Structured content
│
├── Dockerfile             # Production container
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## Quick Start

### Prerequisites
- Python 3.11+
- Anthropic API key ([get one here](https://console.anthropic.com))
- Gmail account (for email integration)
- Git

### 1. Clone and Setup

```bash
# Clone repository
git clone <your-repo-url>
cd nicole

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### 2. Configure Environment

Edit `.env`:
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ENVIRONMENT=development
HIGH_CONFIDENCE_THRESHOLD=0.85
MEDIUM_CONFIDENCE_THRESHOLD=0.60
OWNER_EMAIL=info@woodthumb.com
```

### 3. Run Locally

```bash
# From project root
python -m uvicorn api.main:app --reload --port 8000
```

Visit:
- API: http://localhost:8000
- Health: http://localhost:8000/api/health
- Chat test: http://localhost:8000/api/chat/test
- Widget: Open `widget/test.html` in browser (create simple HTML file with widget script)

### 4. Test Chat Widget

Create `test.html`:
```html
<!DOCTYPE html>
<html>
<head>
  <title>Nicole Test</title>
</head>
<body>
  <h1>Test Page</h1>
  <script src="http://localhost:8000/widget/nicole-widget.js"></script>
</body>
</html>
```

## Deployment

### Option A: Railway.app (Recommended)

1. Create Railway account at [railway.app](https://railway.app)
2. Install Railway CLI: `npm install -g @railway/cli`
3. Login: `railway login`
4. Initialize: `railway init`
5. Add environment variables in Railway dashboard
6. Deploy: `railway up`

Railway will automatically:
- Build Docker container
- Set up HTTPS
- Provide production URL
- Monitor health checks

**Cost:** $5-10/month

### Option B: Fly.io

1. Install flyctl: `brew install flyctl` (Mac) or [other platforms](https://fly.io/docs/hands-on/install-flyctl/)
2. Login: `fly auth login`
3. Launch: `fly launch`
4. Set secrets: `fly secrets set ANTHROPIC_API_KEY=your_key`
5. Deploy: `fly deploy`

**Cost:** Free tier available, ~$5/month for production

### Option C: Docker (Self-hosted)

```bash
# Build image
docker build -t nicole .

# Run container
docker run -d \
  -p 8000:8000 \
  -e ANTHROPIC_API_KEY=your_key \
  -e ENVIRONMENT=production \
  --name nicole \
  nicole
```

## Setup Components

### Chat Widget Integration

After deploying API, add to Squarespace website:

1. Go to Settings → Advanced → Code Injection
2. Add to Footer:

```html
<script>
  // Update with your deployed API URL
  window.NICOLE_API_URL = 'https://your-app.railway.app/api';
</script>
<script src="https://your-app.railway.app/widget/nicole-widget.js"></script>
```

### Gmail Integration

See detailed setup in `gmail/README.md`:

1. Go to [script.google.com](https://script.google.com)
2. Create new project, paste `gmail/Code.gs` and `gmail/Config.gs`
3. Update `NICOLE_API_URL` with deployed API
4. Run `setup()` function to authorize
5. Create time trigger: run `processNewEmails` every 5 minutes

## Customization

### Update Knowledge Base

Edit `knowledge/woodthumb.md` with latest:
- Workshop offerings and pricing
- Shop time policies
- Team event packages
- Custom work process
- Hours, location, contact info

Restart API to reload knowledge.

### Adjust Confidence Thresholds

In `.env`:
```env
# Higher = more cautious (fewer auto-sends)
HIGH_CONFIDENCE_THRESHOLD=0.90

# Lower = more aggressive (more auto-sends)
HIGH_CONFIDENCE_THRESHOLD=0.75
```

### Modify Brand Voice

Edit `api/prompts.py` SYSTEM_PROMPT to adjust:
- Tone (formal vs casual)
- Response length
- Personality traits
- Special instructions

### Change Widget Colors

Edit `widget/nicole-widget.css`:
```css
:root {
  --nicole-accent: #8b7355;  /* Wood Thumb brown */
  --nicole-primary: #1a1a1a; /* Dark background */
  /* ... */
}
```

## Monitoring

### Health Checks
- API: `https://your-app.railway.app/api/health`
- Knowledge: `https://your-app.railway.app/api/knowledge`

### Logs
- **Railway**: View in dashboard under Deployments
- **Fly.io**: `fly logs`
- **Gmail**: script.google.com → Executions

### Conversation Logging (Optional)

1. Create Google Sheet
2. Add sheet ID to `.env`: `GOOGLE_SHEETS_ID=your_sheet_id`
3. Set `LOG_TO_SHEETS=true`

Logs: timestamp, email, intent, confidence, routing, response

## Cost Breakdown

**Monthly Operating Costs:**

| Service | Cost |
|---------|------|
| Claude API (Sonnet) | $3-10 (based on usage) |
| Railway/Fly.io hosting | $5 |
| Gmail integration | Free |
| **Total** | **$8-15/month** |

**Compare to:**
- Intercom + Fin: $79-128/month
- Zendesk Suite: $55-165/month
- Tidio + AI: $70-100/month

**Savings: ~$600-1,800/year**

## Troubleshooting

### Chat widget not appearing
- Check browser console for errors
- Verify API URL is correct in widget script
- Ensure CORS allows your domain (update `api/main.py`)

### Gmail integration not working
- Check Google Apps Script execution logs
- Verify API URL is accessible (not localhost!)
- Ensure trigger is set up correctly
- Review Gmail labels for processing status

### High API costs
- Reduce max_tokens in `api/nicole.py`
- Increase confidence thresholds (fewer auto-sends)
- Add caching for common questions
- Monitor usage in Anthropic console

### Wrong responses
- Update knowledge base with correct info
- Adjust system prompt for better guidance
- Review intent classification accuracy
- Consider adding example conversations

## Development

### Run tests
```bash
pytest tests/
```

### Format code
```bash
black api/
```

### Type checking
```bash
mypy api/
```

### Update dependencies
```bash
pip freeze > requirements.txt
```

## Roadmap

- [ ] Instagram DM integration
- [ ] SMS support (Twilio)
- [ ] Admin dashboard (Flask/React)
- [ ] Analytics & reporting
- [ ] Multi-language support
- [ ] Voice interface (phone calls)
- [ ] Booking system integration (direct Acuity API)

## Support

For issues, questions, or contributions:
- Check existing documentation in `/gmail/README.md`
- Review Claude API docs: [docs.anthropic.com](https://docs.anthropic.com)
- FastAPI docs: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

## License

MIT License - Feel free to adapt for your own business!

---

**Built with ❤️ for Wood Thumb**

*Nicole is powered by Claude (Anthropic) and designed to make woodworking more accessible, one conversation at a time.*
