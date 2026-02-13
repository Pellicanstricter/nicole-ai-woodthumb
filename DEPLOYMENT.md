# Nicole Deployment Guide

Complete step-by-step guide for deploying Nicole to production.

## Pre-Deployment Checklist

- [ ] Anthropic API key obtained
- [ ] Knowledge base reviewed and updated
- [ ] Environment variables configured
- [ ] Local testing completed
- [ ] Gmail account ready for integration
- [ ] Domain/hosting decided (Railway, Fly.io, or self-hosted)

---

## Railway Deployment (Recommended)

### Step 1: Prepare Repository

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial Nicole implementation"

# Push to GitHub (create repo first on github.com)
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your Nicole repository
6. Railway will auto-detect Dockerfile

### Step 3: Configure Environment Variables

In Railway dashboard → Variables, add:

```
ANTHROPIC_API_KEY=sk-ant-xxxxx
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000
HIGH_CONFIDENCE_THRESHOLD=0.85
MEDIUM_CONFIDENCE_THRESHOLD=0.60
OWNER_EMAIL=info@woodthumb.com
```

### Step 4: Generate Domain

1. In Railway dashboard → Settings
2. Click "Generate Domain"
3. Copy the URL (e.g., `nicole-production.up.railway.app`)

### Step 5: Update Widget Configuration

Update the widget script URL in your Squarespace site:
```html
<script>
  window.NICOLE_API_URL = 'https://nicole-production.up.railway.app/api';
</script>
<script src="https://nicole-production.up.railway.app/widget/nicole-widget.js"></script>
```

### Step 6: Configure CORS

Update `api/main.py` to include your domain:
```python
allow_origins=[
    "https://woodthumb.com",
    "https://www.woodthumb.com",
    # Add your Squarespace domain
]
```

Commit and push changes - Railway will auto-deploy.

---

## Fly.io Deployment

### Step 1: Install Fly CLI

```bash
# Mac
brew install flyctl

# Linux
curl -L https://fly.io/install.sh | sh

# Windows
pwsh -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

### Step 2: Login and Launch

```bash
fly auth login
cd nicole
fly launch
```

Follow prompts:
- App name: `nicole-woodthumb`
- Region: Choose closest to you
- Database: No
- Deploy now: No (we need to set secrets first)

### Step 3: Set Secrets

```bash
fly secrets set ANTHROPIC_API_KEY=sk-ant-xxxxx
fly secrets set ENVIRONMENT=production
fly secrets set OWNER_EMAIL=info@woodthumb.com
```

### Step 4: Deploy

```bash
fly deploy
```

### Step 5: Get URL

```bash
fly status
# Copy the hostname (e.g., nicole-woodthumb.fly.dev)
```

### Step 6: Update Widget

Use the Fly.io URL in your widget configuration.

---

## Squarespace Integration

### Add Chat Widget

1. Go to Squarespace dashboard
2. Settings → Advanced → Code Injection
3. Add to **Footer** (loads on all pages):

```html
<!-- Nicole Chat Widget -->
<link rel="stylesheet" href="https://your-deployed-url/widget/nicole-widget.css">
<script>
  window.NICOLE_API_URL = 'https://your-deployed-url/api';
</script>
<script src="https://your-deployed-url/widget/nicole-widget.js"></script>
```

4. Save and test on your live site

### Troubleshooting Widget

If widget doesn't appear:
1. Check browser console (F12) for errors
2. Verify API URL is correct
3. Test API health: `https://your-deployed-url/api/health`
4. Check CORS settings in `api/main.py`

---

## Gmail Integration Setup

### Step 1: Create Apps Script Project

1. Go to [script.google.com](https://script.google.com)
2. Click "+ New Project"
3. Rename to "Nicole Gmail Integration"

### Step 2: Add Code Files

**Code.gs:**
1. Delete default code
2. Paste contents from `gmail/Code.gs`

**Config.gs:**
1. Click "+" next to Files → Script
2. Name it "Config"
3. Paste contents from `gmail/Config.gs`
4. **Update `NICOLE_API_URL`** with your deployed URL

### Step 3: Initial Setup

1. Select `setup` function from dropdown
2. Click Run (▶)
3. Grant permissions when prompted
4. Review execution log - should see labels created

### Step 4: Create Trigger

1. Click clock icon (⏰) in sidebar
2. "+ Add Trigger"
3. Configure:
   - Function: `processNewEmails`
   - Event source: Time-driven
   - Type: Minutes timer
   - Interval: Every 5 minutes
4. Save

### Step 5: Test

**Manual test:**
1. Send test email to your Gmail
2. Select `testWithLatestEmail` function
3. Click Run
4. Check logs for API response

**Automatic test:**
1. Send test email
2. Wait 5 minutes
3. Check inbox for Nicole's response or draft
4. Verify labels were applied

---

## Post-Deployment Verification

### Health Checks

```bash
# API health
curl https://your-deployed-url/api/health

# Knowledge base loaded
curl https://your-deployed-url/api/knowledge

# Chat endpoint
curl -X POST https://your-deployed-url/api/chat/test
```

### Widget Test

1. Visit your Squarespace site
2. Look for chat button (bottom-right)
3. Click and send test message
4. Verify streaming response

### Email Test

1. Send email to Gmail from different address
2. Wait 5 minutes for trigger
3. Check Gmail labels:
   - `Nicole/Processed`
   - `Nicole/Auto-Sent` (high confidence)
   - `Nicole/Draft` (medium confidence)
   - `Nicole/Needs Review` (low confidence)

---

## Monitoring Setup

### UptimeRobot (Free)

1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Create account
3. Add monitor:
   - Type: HTTP(S)
   - URL: `https://your-deployed-url/api/health`
   - Interval: 5 minutes
4. Set up email alerts

### Railway Monitoring

Built-in:
- Deployment logs in dashboard
- Metrics (CPU, memory, requests)
- Auto-restart on failures

### Gmail Monitoring

Check Apps Script executions:
1. script.google.com → Your project
2. Click executions (⚡) in sidebar
3. Review logs and errors

---

## Updating After Deployment

### Update Knowledge Base

1. Edit `knowledge/woodthumb.md`
2. Commit and push to Git
3. Railway auto-deploys
4. Verify: `curl https://your-url/api/knowledge`

### Update Widget

1. Edit `widget/nicole-widget.js` or `.css`
2. Commit and push
3. Clear browser cache to see changes

### Update Gmail Script

1. Edit in script.google.com
2. Save (Ctrl+S)
3. Changes apply immediately

---

## Rollback Procedure

### Railway

1. Dashboard → Deployments
2. Find previous working deployment
3. Click "⋮" → Redeploy

### Fly.io

```bash
fly releases
fly deploy --image <previous-image-id>
```

### Gmail Script

1. script.google.com → Your project
2. File → See version history
3. Select working version → Restore

---

## Common Issues

### High API Costs

**Solution:**
- Increase confidence thresholds (fewer auto-sends)
- Reduce `max_tokens` in `api/nicole.py`
- Add rate limiting
- Cache common responses

### Wrong Responses

**Solution:**
- Update knowledge base
- Improve system prompt
- Add example conversations
- Review intent classification

### Email Not Processing

**Check:**
- Google Apps Script trigger is active
- API URL is correct (not localhost!)
- API is accessible (health check passes)
- Gmail labels exist
- Execution logs for errors

### Widget Loading Slow

**Solution:**
- Enable CDN (Cloudflare)
- Minify JS/CSS
- Reduce initial payload
- Use lazy loading

---

## Security Notes

- Never commit `.env` file (use `.env.example`)
- Rotate API keys regularly
- Use Railway's secret management
- Set up HTTPS (automatic with Railway/Fly)
- Review Gmail script permissions
- Monitor API usage in Anthropic console

---

## Need Help?

- Railway docs: [docs.railway.app](https://docs.railway.app)
- Fly.io docs: [fly.io/docs](https://fly.io/docs)
- Anthropic API: [docs.anthropic.com](https://docs.anthropic.com)
- FastAPI: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)

---

**Deployment complete!** 🎉

Nicole is now live and handling customer inquiries for Wood Thumb.
