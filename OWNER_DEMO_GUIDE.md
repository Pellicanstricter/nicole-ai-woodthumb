# Nicole Demo Guide for Wood Thumb Owner

**Complete walkthrough to demonstrate Nicole's AI customer service capabilities**

---

## Quick Demo Overview (5 minutes)

Nicole is an AI assistant that handles customer inquiries through:
1. **Website Chat Widget** - Real-time conversations on your website
2. **Gmail Integration** - Automatic email processing with intelligent routing

**Cost:** $13-17/month vs $79-128/month for Intercom
**Savings:** ~$800-1,200/year

---

## Part 1: Chat Widget Demo (3 minutes)

### How to Show the Chat Widget

1. **Open the test page:**
   ```
   Open: /Users/nathanielsteinrueck/nicole/widget/test.html
   ```
   Or double-click `widget/test.html` in Finder

2. **You'll see:**
   - A Wood Thumb themed page
   - A chat button in the bottom-right corner (🪵)
   - Click it to open the chat widget

### Demo Conversation Scripts

Try these questions to show Nicole's capabilities:

#### **Script 1: Workshop Inquiry**
**You Type:** "What workshops do you offer?"

**Nicole Will:**
- List all workshops (cutting board, side table, spoon carving, etc.)
- Include pricing ($75-$150)
- Mention beginner-friendly
- Provide booking link
- Ask engaging follow-up question

**Owner Notes:**
- Natural, warm tone
- Accurate information
- Includes call-to-action (booking link)

---

#### **Script 2: Pricing Question**
**You Type:** "How much does shop time cost?"

**Nicole Will:**
- State $30-40/hour pricing
- Explain membership affects pricing
- List what's included (tools, workspace)
- Suggest booking process

**Owner Notes:**
- Doesn't fabricate pricing
- Provides helpful context

---

#### **Script 3: Team Event**
**You Type:** "We want to do a team building event for 15 people"

**Nicole Will:**
- Acknowledge group size
- Suggest appropriate projects
- Provide pricing estimate ($85-120/person)
- Offer to collect more details or connect with owner

**Owner Notes:**
- Handles complex inquiries gracefully
- Knows when to involve human

---

#### **Script 4: Multi-Turn Conversation**
**Turn 1:** "I'm interested in woodworking"
- Nicole welcomes, asks how she can help

**Turn 2:** "I've never done it before"
- Reassures it's beginner-friendly
- Suggests workshops

**Turn 3:** "What's the easiest project?"
- Recommends specific workshops (cutting board, spoon)
- Includes booking link

**Owner Notes:**
- Maintains context across conversation
- Natural conversation flow

---

#### **Script 5: Out of Scope Question**
**You Type:** "Do you teach welding?"

**Nicole Will:**
- Politely clarify focus is woodworking
- Not fabricate false offerings
- Suggest contacting owner for other questions

**Owner Notes:**
- Stays honest and on-brand
- Doesn't make up information

---

## Part 2: Email Processing Demo (5 minutes)

### How Email Processing Works

**Every 5 minutes, Nicole:**
1. Checks Gmail inbox for new emails
2. Reads the email content
3. Analyzes intent and generates response
4. Routes based on confidence:
   - **High (>85%)**: Auto-sends reply
   - **Medium (60-85%)**: Saves as draft for review
   - **Low (<60%)**: Flags with detailed note

### Demo Email Scenarios

You can test these directly via API (without Gmail setup) to show the owner:

#### **Test 1: Simple FAQ (Auto-Send)**

Run this command:
```bash
curl -X POST http://localhost:8000/api/email \
  -H 'Content-Type: application/json' \
  -d '{
    "from_email": "customer@example.com",
    "subject": "Workshop Hours",
    "body": "Hi, what are your workshop hours? Thanks!",
    "thread_id": "demo-1"
  }'
```

**Show the owner:**
- Intent: `policy_question` or `general_info`
- Confidence: >85%
- Routing: `auto_send`
- Response: Professional email with hours info

**Explain:** "This type of simple question would get an immediate auto-reply"

---

#### **Test 2: Team Event (Draft)**

```bash
curl -X POST http://localhost:8000/api/email \
  -H 'Content-Type: application/json' \
  -d '{
    "from_email": "corporate@company.com",
    "subject": "Team Event Inquiry",
    "body": "We are interested in hosting a team event for 20 people. Can you provide details about your offerings and pricing?",
    "thread_id": "demo-2"
  }'
```

**Show the owner:**
- Intent: `team_event_inquiry`
- Confidence: 60-85%
- Routing: `draft`
- Response: Detailed team event information

**Explain:** "This would be saved as a draft in Gmail for you to review and personalize before sending"

---

#### **Test 3: Complex Custom Work (Flag)**

```bash
curl -X POST http://localhost:8000/api/email \
  -H 'Content-Type: application/json' \
  -d '{
    "from_email": "artist@studio.com",
    "subject": "Custom Art Installation",
    "body": "I am working on a multimedia installation involving reclaimed wood and need very specific custom pieces with unusual dimensions and artistic requirements.",
    "thread_id": "demo-3"
  }'
```

**Show the owner:**
- Intent: `custom_work_inquiry` or `other`
- Confidence: <60%
- Routing: `flag`
- Response: Polite response + flag for owner review

**Explain:** "Complex or unusual requests get flagged so you can handle them personally with Nicole's suggested response as a starting point"

---

## Part 3: Gmail Integration Demo (Optional - 15 minutes)

If you want to show the FULL automation with real Gmail:

### Setup Steps (One-Time)

1. **Go to Google Apps Script:**
   - Visit: https://script.google.com
   - Sign in with Wood Thumb's Gmail (info@woodthumb.com or steinrueckn@gmail.com for demo)

2. **Create Project:**
   - Click "+ New Project"
   - Name it "Nicole - Wood Thumb"

3. **Add Code:**
   - Copy `gmail/Code.gs` content
   - Copy `gmail/Config.gs` content
   - Update API URL in Config

4. **Run Setup:**
   - Select `setup` function
   - Grant Gmail permissions
   - Verify labels created

5. **Test:**
   - Send test email to your Gmail
   - Run `testWithLatestEmail` function
   - Check response in logs

6. **Enable Automation:**
   - Create time-based trigger
   - Set to run `processNewEmails` every 5 minutes

### Live Demo Flow

1. **Send test email** from another account
2. **Wait 5 minutes** (or run manually)
3. **Show in Gmail:**
   - Email labeled `Nicole/Processed`
   - Response sent (auto-send)
   - OR draft created (medium confidence)
   - OR flagged with note (low confidence)

---

## Part 4: Owner Dashboard Needs

### What the Owner Needs to Manage

Based on Wood Thumb's needs, here's what should be in a dashboard:

#### **1. Knowledge Base Management**
- Edit workshop details (names, descriptions, pricing)
- Update shop time policies
- Modify team event packages
- Change hours/location/contact info
- **Current:** Edit `knowledge/woodthumb.md` file
- **Future:** Web dashboard with forms

#### **2. Confidence Threshold Controls**
- Adjust auto-send threshold (currently 85%)
- Adjust draft threshold (currently 60%)
- **Current:** Edit `.env` file
- **Future:** Dashboard sliders

#### **3. Conversation Monitoring**
- View recent chats and emails
- See what Nicole responded
- Check confidence scores
- **Current:** Check Gmail labels, Apps Script logs
- **Future:** Dashboard with conversation history

#### **4. Response Templates**
- Edit greeting message
- Customize email signatures
- Adjust brand voice
- **Current:** Edit `api/prompts.py`
- **Future:** Template editor in dashboard

#### **5. Analytics**
- Number of conversations handled
- Auto-send vs draft ratio
- Common question topics
- Customer satisfaction
- **Current:** Manual log review
- **Future:** Dashboard with charts

---

## Demo Script for Owner Presentation

### Introduction (1 minute)

> "I want to show you Nicole, an AI assistant that can handle your customer service inquiries through both your website chat and Gmail. It costs about $15/month instead of $80-120/month for services like Intercom or Zendesk."

### Chat Demo (3 minutes)

1. Open widget test page
2. Show chat button: "This would appear on every page of your website"
3. Type: "What workshops do you offer?"
4. Wait for response
5. Point out:
   - Natural conversation
   - Accurate workshop info
   - Booking link included
   - Fast response (2-3 seconds)

6. Try another: "How much for team event for 20 people?"
7. Show how it handles complex inquiries

### Email Demo (3 minutes)

1. Show API endpoint test (or live Gmail if set up)
2. Run simple FAQ test
3. Explain: "This type gets auto-replied immediately"
4. Run team event test
5. Explain: "This creates a draft for you to review"
6. Run complex test
7. Explain: "This gets flagged for your personal attention"

### Value Proposition (2 minutes)

**Time Saved:**
- 70% of inquiries auto-handled (FAQs, basic info)
- 25% drafted for quick review (team events, bookings)
- 5% flagged for personal attention (complex custom work)

**Cost Savings:**
- Nicole: $15/month
- Intercom: $79-128/month
- **Save: $800-1,200/year**

**Better Experience:**
- 24/7 instant responses
- Never miss an inquiry
- Consistent Wood Thumb voice
- Frees you for actual woodworking

### Implementation Plan (1 minute)

**Week 1:**
- Deploy Nicole to production server
- Add chat widget to website
- Set up Gmail integration

**Week 2:**
- Monitor and adjust confidence thresholds
- Review auto-sent emails for quality
- Update knowledge base as needed

**Week 3:**
- Analyze which questions come up most
- Fine-tune responses
- Consider adding FAQ page

**Ongoing:**
- Monthly review of conversations
- Update pricing/offerings as they change
- ~15 minutes/week maintenance

---

## Common Owner Questions & Answers

### "What if Nicole gives wrong information?"

**Answer:** Nicole only uses information from the knowledge base we provide. She won't make up prices or offerings. If unsure, she routes to you. We can start with higher confidence thresholds (more drafts, fewer auto-sends) and adjust as you gain trust.

### "Can I review messages before they're sent?"

**Answer:** Yes! You control the confidence thresholds. Set it to only auto-send at 95% confidence, and everything else becomes drafts you review first.

### "What about complex custom work requests?"

**Answer:** Nicole knows when to involve you. Complex, unusual, or high-value inquiries get flagged with a summary and suggested response, but YOU make the final call.

### "How do I update information when pricing changes?"

**Answer:** Edit one file (`knowledge/woodthumb.md`) and restart the server. Takes 2 minutes. Future: dashboard with forms.

### "What if a customer wants to talk to a real person?"

**Answer:** Nicole always identifies as an AI and can hand off to you. She can say "Let me have the owner reach out to you directly" for sensitive matters.

### "Is my customer data secure?"

**Answer:**
- Nicole runs on YOUR server (Railway/Fly.io)
- Gmail integration uses Google's secure OAuth
- No third parties access your data
- Anthropic (Claude API) processes messages but doesn't store customer data

### "Can I turn it off?"

**Answer:** Yes, instantly:
- Chat widget: Remove one line from website
- Gmail: Delete trigger in Google Apps Script
- Complete control at all times

---

## Next Steps After Demo

If owner approves:

### Immediate (Today):
- [ ] Gather accurate Wood Thumb information
- [ ] Review knowledge base accuracy
- [ ] Approve brand voice and tone

### This Week:
- [ ] Update `knowledge/woodthumb.md` with real data
- [ ] Deploy to Railway (15 min)
- [ ] Set up Gmail integration (20 min)
- [ ] Add chat widget to Squarespace (10 min)

### Week 1:
- [ ] Monitor all conversations
- [ ] Review auto-sent emails
- [ ] Adjust confidence thresholds
- [ ] Collect feedback

### Week 2-4:
- [ ] Analyze common questions
- [ ] Refine responses
- [ ] Consider dashboard needs
- [ ] Plan future enhancements

---

## Future Enhancements (Optional)

### Phase 2 (Month 2-3):
- Web dashboard for managing knowledge base
- Conversation analytics and reporting
- SMS/text message support
- Instagram DM integration

### Phase 3 (Month 4-6):
- Direct booking system integration (Acuity API)
- Automated follow-ups
- Customer satisfaction surveys
- Multi-language support

---

## Support & Training

### For Owner:
- **Knowledge Base Updates:** 5-minute video tutorial
- **Dashboard Access:** Login credentials and walkthrough
- **Emergency Contact:** Direct line for issues
- **Monthly Check-in:** 15-minute call to review performance

### Documentation:
- Quick reference guide (1-page)
- Video tutorials for common tasks
- FAQ for troubleshooting
- Direct support contact

---

## Demo Checklist

Before presenting to owner:

- [ ] Server running (localhost:8000 or deployed)
- [ ] Chat widget test page works
- [ ] Test all demo conversation scripts
- [ ] Email endpoint tests work
- [ ] Have cost comparison ready
- [ ] Know time savings estimates
- [ ] Have implementation timeline
- [ ] Prepare answers to common questions

---

**Ready to demo!** 🚀

This should take about 10-15 minutes total and clearly show the value Nicole brings to Wood Thumb.
