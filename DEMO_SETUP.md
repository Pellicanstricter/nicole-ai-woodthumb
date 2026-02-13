# Nicole Demo Setup Guide

Complete guide to test Nicole locally with steinrueckn@gmail.com

## Step 1: Get Anthropic API Key (5 minutes)

### Option A: You Already Have an Account
1. Go to https://console.anthropic.com/settings/keys
2. Log in with your account
3. Click "Create Key"
4. Name it "Nicole Demo"
5. Copy the key (starts with `sk-ant-`)

### Option B: New Account (Free Credits)
1. Go to https://console.anthropic.com
2. Sign up (you get $5 free credit)
3. Verify your email
4. Go to Settings → API Keys
5. Create a new key
6. Copy the key

### Add Key to .env File
```bash
cd /Users/nathanielsteinrueck/nicole
nano .env  # or use any text editor
```

Replace `your_key_here_get_from_anthropic_console` with your actual key:
```env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
```

Save and exit (Ctrl+X, then Y, then Enter in nano)

---

## Step 2: Install Dependencies & Start Server (2 minutes)

```bash
cd /Users/nathanielsteinrueck/nicole

# Make startup script executable (if not already)
chmod +x start.sh

# Start the server
./start.sh
```

You should see:
```
🪵 Starting Nicole for Wood Thumb...
✅ Nicole is ready!
🌐 Starting FastAPI server...
   API: http://localhost:8000
   Health: http://localhost:8000/api/health
```

**Keep this terminal window open!** The server needs to keep running.

---

## Step 3: Test the API (2 minutes)

Open a **new terminal window** and run these tests:

### Test 1: Health Check
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "api_key_configured": true,
  "environment": "development"
}
```

### Test 2: Knowledge Base
```bash
curl http://localhost:8000/api/knowledge
```

Expected: Shows word count and status

### Test 3: Send a Chat Message
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What workshops do you offer?",
    "conversation_history": [],
    "stream": false
  }'
```

Expected: Nicole responds with workshop information

---

## Step 4: Test Chat Widget in Browser (5 minutes)

### Open Test Page
```bash
# From the nicole directory
open widget/test.html
# Or manually: Open widget/test.html in Chrome/Safari/Firefox
```

### Test Interactions
1. **Widget appears** - Look for chat button in bottom-right corner
2. **Click to open** - Widget should expand
3. **Send test messages:**
   - "What workshops do you offer?"
   - "How much is shop time?"
   - "Tell me about team events"
   - "I want to book a cutting board workshop"

### What to Check
- ✅ Widget loads and displays properly
- ✅ Messages stream in real-time (typing effect)
- ✅ Responses are relevant and helpful
- ✅ Widget is themed correctly (dark with brown accents)
- ✅ Mobile responsive (resize browser window)

---

## Step 5: Test Email Processing (Without Gmail Integration)

You can test the email endpoint directly without setting up Gmail Apps Script yet.

### Test Email Endpoint
```bash
curl -X POST http://localhost:8000/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "from_email": "test@example.com",
    "subject": "Workshop Question",
    "body": "Hi, I would like to know what beginner workshops you have available and the pricing. Thanks!",
    "thread_id": "test-thread-123"
  }'
```

### Check Response
The API will return:
```json
{
  "response": "Nicole's email response...",
  "intent": "workshop_inquiry",
  "confidence": 0.92,
  "routing": "auto_send",
  "reasoning": "Clear workshop inquiry..."
}
```

### Test Different Scenarios

**High Confidence (should auto-send):**
```bash
curl -X POST http://localhost:8000/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "from_email": "customer@example.com",
    "subject": "What are your hours?",
    "body": "Hi, what are your operating hours? Thanks",
    "thread_id": "test-2"
  }'
```

**Medium Confidence (should draft):**
```bash
curl -X POST http://localhost:8000/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "from_email": "corporate@company.com",
    "subject": "Team Building Event",
    "body": "We are interested in hosting a team event for 25 people. Can you provide more details on what you offer and pricing?",
    "thread_id": "test-3"
  }'
```

**Low Confidence (should flag):**
```bash
curl -X POST http://localhost:8000/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "from_email": "artist@example.com",
    "subject": "Custom Artistic Collaboration",
    "body": "I am a multimedia artist interested in collaborating on an experimental installation piece involving reclaimed wood. Would you be open to discussing a very unique partnership?",
    "thread_id": "test-4"
  }'
```

---

## Step 6: Optional - Gmail Integration Demo (15 minutes)

If you want to test the full Gmail integration with steinrueckn@gmail.com:

### Setup Google Apps Script

1. **Go to Apps Script**
   - Visit https://script.google.com
   - Sign in with steinrueckn@gmail.com

2. **Create New Project**
   - Click "+ New Project"
   - Name it "Nicole Demo - Gmail"

3. **Add Code Files**
   - Delete default Code.gs content
   - Copy from: `/Users/nathanielsteinrueck/nicole/gmail/Code.gs`
   - Click "+" next to Files → Script
   - Name it "Config"
   - Copy from: `/Users/nathanielsteinrueck/nicole/gmail/Config.gs`

4. **Update Config**
   In Config.gs, change:
   ```javascript
   NICOLE_API_URL: 'http://localhost:8000/api',
   ```

   **IMPORTANT:** For local testing, you need to expose localhost. Options:

   **Option A: Use ngrok (Recommended for Demo)**
   ```bash
   # Install ngrok
   brew install ngrok  # Mac

   # In a new terminal, expose your local server
   ngrok http 8000
   ```

   Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`) and update Config.gs:
   ```javascript
   NICOLE_API_URL: 'https://abc123.ngrok.io/api',
   ```

5. **Run Setup**
   - Select `setup` function from dropdown
   - Click Run (▶)
   - Grant permissions (review carefully)
   - Check logs - should see labels created

6. **Test Manually**
   - Send test email to steinrueckn@gmail.com from another address
   - Select `testWithLatestEmail` function
   - Click Run
   - Check logs for API response

7. **Create Trigger (Optional)**
   - Click clock icon (⏰)
   - "+ Add Trigger"
   - Function: `processNewEmails`
   - Event: Time-driven
   - Interval: Every 5 minutes
   - Save

---

## Demo Testing Checklist

### Basic Functionality
- [ ] API server starts without errors
- [ ] Health check returns healthy status
- [ ] Knowledge base loads correctly
- [ ] Chat endpoint accepts messages
- [ ] Email endpoint processes requests

### Chat Widget
- [ ] Widget button appears on test page
- [ ] Widget opens when clicked
- [ ] Messages send successfully
- [ ] Responses stream in real-time
- [ ] Responses are relevant and accurate
- [ ] Widget is mobile responsive
- [ ] Styling matches Wood Thumb theme

### Email Processing (API Level)
- [ ] High confidence queries route to "auto_send"
- [ ] Medium confidence routes to "draft"
- [ ] Low confidence routes to "flag"
- [ ] Intent classification is accurate
- [ ] Confidence scores are reasonable
- [ ] Email responses are well-formatted

### Gmail Integration (If Setup)
- [ ] Apps Script connects to API
- [ ] Labels are created in Gmail
- [ ] Test email is processed
- [ ] Response appears in Gmail (draft or sent)
- [ ] Labels are applied correctly

---

## Common Issues & Solutions

### Issue: "API key not configured"
**Solution:** Make sure you added your Anthropic API key to `.env` file

### Issue: "Module not found" errors
**Solution:**
```bash
cd /Users/nathanielsteinrueck/nicole
pip install -r requirements.txt
```

### Issue: Widget doesn't load
**Solution:**
- Make sure API server is running
- Check browser console (F12) for errors
- Verify URL in test.html matches server: `http://localhost:8000`

### Issue: Port 8000 already in use
**Solution:**
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn api.main:app --reload --port 8001
```

### Issue: Gmail Apps Script can't reach localhost
**Solution:** Use ngrok to expose localhost:
```bash
ngrok http 8000
# Use the HTTPS URL in Config.gs
```

---

## Test Message Ideas

Try these with the chat widget:

**Basic Questions:**
- "What workshops do you have?"
- "How much does shop time cost?"
- "Where are you located?"
- "What are your hours?"

**Booking Related:**
- "I want to book a cutting board workshop"
- "How do I reserve shop time?"
- "Can I book a private workshop?"

**Team Events:**
- "We're looking for a team building activity for 15 people"
- "Do you do corporate events?"
- "What's included in team events?"

**Custom Work:**
- "Can you make a custom dining table?"
- "I need a bookshelf built"
- "How much for a custom project?"

**Complex/Edge Cases:**
- "I've never worked with wood before, where do I start?"
- "Do you offer classes for kids?"
- "Can I bring my own wood?"

---

## Success Criteria

Nicole is working correctly if:

✅ **Responses are relevant** - Answers match the question
✅ **Brand voice is consistent** - Warm, casual, helpful tone
✅ **Information is accurate** - Matches knowledge base
✅ **Routing makes sense** - Confidence levels match complexity
✅ **Widget is functional** - No crashes, smooth UX
✅ **Performance is good** - Responses within 2-3 seconds

---

## Next Steps After Demo

Once demo testing is successful:

1. **Update Knowledge Base** - Edit `knowledge/woodthumb.md` with real Wood Thumb info
2. **Deploy to Production** - Follow `DEPLOYMENT.md` guide
3. **Setup Production Gmail** - Use real info@woodthumb.com
4. **Add to Squarespace** - Integrate widget on live site
5. **Monitor & Iterate** - Adjust based on real usage

---

## Getting Help

- Full docs: `README.md`
- Deployment guide: `DEPLOYMENT.md`
- Gmail setup: `gmail/README.md`
- API documentation: http://localhost:8000/docs (when running)

---

**Ready to test!** 🚀

Start with Step 1 (get API key) and work through each step. The entire demo setup should take about 30 minutes.
