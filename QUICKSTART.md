# Nicole Quick Start Guide

Get Nicole up and running in 5 minutes.

## Setup (First Time Only)

```bash
# 1. Navigate to project
cd nicole

# 2. Copy environment template
cp .env.example .env

# 3. Edit .env and add your Anthropic API key
# Get key from: https://console.anthropic.com
nano .env  # or use your preferred editor
```

Add your API key:
```env
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

## Start Development Server

```bash
# Easy way (uses start.sh script)
./start.sh

# Manual way
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

Server will start at: **http://localhost:8000**

## Test the Chat Widget

1. Open `widget/test.html` in your browser
2. Click chat button in bottom-right
3. Try asking: "What workshops do you offer?"

## Test the API Directly

```bash
# Health check
curl http://localhost:8000/api/health

# Knowledge base info
curl http://localhost:8000/api/knowledge

# Send chat message
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are your hours?",
    "conversation_history": [],
    "stream": false
  }'
```

## Next Steps

1. **Update Knowledge Base**: Edit `knowledge/woodthumb.md` with accurate Wood Thumb info
2. **Test Email Endpoint**: See `DEPLOYMENT.md` for Gmail integration
3. **Deploy**: Follow `DEPLOYMENT.md` for Railway or Fly.io deployment
4. **Integrate Widget**: Add to Squarespace once deployed

## Common Commands

```bash
# Start server
./start.sh

# Run in background
uvicorn api.main:app --host 0.0.0.0 --port 8000 &

# Check logs
tail -f logs/nicole.log

# Stop server
pkill -f uvicorn

# Scrape Wood Thumb website (optional)
python knowledge/scraper.py
```

## Project Structure Overview

```
nicole/
├── api/              # FastAPI backend
│   ├── main.py      # Entry point
│   ├── chat.py      # Chat endpoint
│   ├── email.py     # Email endpoint
│   └── nicole.py    # AI logic
│
├── widget/          # Chat widget
│   ├── nicole-widget.js
│   └── nicole-widget.css
│
├── gmail/           # Gmail integration
│   └── Code.gs      # Google Apps Script
│
└── knowledge/       # Content
    └── woodthumb.md # Knowledge base
```

## Need Help?

- Full documentation: See `README.md`
- Deployment guide: See `DEPLOYMENT.md`
- Gmail setup: See `gmail/README.md`
- API docs: http://localhost:8000/docs (when running)

## Troubleshooting

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**"API key not configured" error:**
- Check `.env` file exists
- Verify `ANTHROPIC_API_KEY` is set correctly

**Widget doesn't load:**
- Ensure server is running: http://localhost:8000/api/health
- Check browser console for errors
- Verify widget script URL is correct

**Port already in use:**
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
uvicorn api.main:app --reload --port 8001
```

---

**Ready to go!** 🚀

Nicole should now be running locally. Test the chat widget and explore the API documentation at http://localhost:8000/docs
