# Setup Guide for Wood Thumb Owner

**Quick Start - Everything You Need to Know**

---

## ✅ What's Already Configured

Good news! Your system is already set up and ready to use:

### 1. **API Key (Already Configured)**
- ✅ Your Anthropic API key is configured: `sk-ant-api03-...fQAA`
- ✅ This is stored in the `.env` file
- ✅ Cost: ~$13-17/month for typical usage (vs $79-128/month for Intercom)

**If you ever need to change it:**
1. Get a new key from https://console.anthropic.com/settings/keys
2. Update in Dashboard → Settings → API Configuration
3. Or edit the `.env` file directly

### 2. **Email Configuration**
- ✅ Owner email set to: `steinrueckn@gmail.com`
- ✅ This receives notifications for flagged messages

### 3. **Server Running**
- ✅ API Server: http://localhost:8000
- ✅ Admin Dashboard: http://localhost:8000/dashboard/admin.html
- ✅ Chat Widget Test: http://localhost:8000/widget/test.html

---

## 🎯 How to Use the System

### **Admin Dashboard** - Your Control Panel

**URL:** http://localhost:8000/dashboard/admin.html

This is where you manage everything:

#### **Overview Tab**
- See total conversations, response times, confidence scores
- Monitor system health (chat widget, Gmail, API status)
- View recent conversations

#### **Settings Tab** (Most Important!)

**1. AI Assistant Identity**
```
Change the assistant's name: "Nicole" → "Woody" or anything else
Update the greeting message customers see first
Customize the title: "AI Assistant" → "Workshop Guide"
```

**2. Calendar & Scheduling Integration**
```
Workshop booking URL: https://woodthumb.com/workshops
Team event URL: https://woodthumb.com/team-events
Shop time URL: https://woodthumb.com/shop-time

Toggle options:
- Show available times
- Auto-suggest booking links
```

**3. Event Display Settings**
```
Featured workshops to highlight
Show/hide pricing
Detail level: Brief, Moderate, or Detailed
```

**4. Confidence Thresholds**
```
Auto-send threshold: 85% (emails sent automatically above this)
Draft threshold: 60% (emails saved as drafts above this)
Lower threshold = more flagged for your review
```

#### **Knowledge Base Tab**
- Edit Wood Thumb information
- Update workshop details, pricing, policies
- Changes apply immediately

#### **Templates Tab**
- Customize chat widget greeting
- Edit email signature
- Adjust brand voice guidelines

---

## 🤖 Where's the Chat Widget?

The chat widget appears as a **floating button in the bottom-right corner** of any page where it's installed.

### **To See It:**

1. **Test Page:** http://localhost:8000/widget/test.html
   - Scroll down to the bottom of the page
   - Look for a circular button with a chat icon in the bottom-right
   - Click it to open the chat window

2. **On Your Website:**
   - Add this code to your Squarespace site (in the footer):
   ```html
   <link rel="stylesheet" href="https://your-api-url.com/widget/nicole-widget.css">
   <script>
     window.NICOLE_API_URL = 'https://your-api-url.com/api';
   </script>
   <script src="https://your-api-url.com/widget/nicole-widget.js"></script>
   ```

### **Widget Features:**
- ✅ Floating button (bottom-right corner)
- ✅ Opens to chat window when clicked
- ✅ Shows assistant name and greeting
- ✅ Streaming responses (types out in real-time)
- ✅ Conversation history maintained
- ✅ Mobile responsive

---

## 📧 Gmail Integration

### **What It Does:**
- Checks your Gmail inbox every 5 minutes
- Reads new customer emails
- Generates responses based on confidence:
  - **High (>85%)**: Auto-sends reply
  - **Medium (60-85%)**: Saves as draft for you to review
  - **Low (<60%)**: Flags for your personal attention

### **Setup Steps:**

**Not set up yet!** Follow the guide:
- See: `GMAIL_SETUP_STEINRUECKN.md` for detailed instructions
- Takes about 15-20 minutes
- Uses Google Apps Script (no coding required)
- Once set up, runs automatically

**To Monitor Gmail Integration:**
- Dashboard → Gmail Integration tab
- See stats: emails processed, auto-sent, drafts, flagged
- Test connection button

---

## 💰 Cost Breakdown

### **Your Current Setup:**
- **Anthropic API**: $8-12/month (based on usage)
- **Railway Hosting**: $5/month (when deployed to production)
- **Gmail Integration**: Free (via Google Apps Script)
- **Total**: ~$13-17/month

### **vs. Alternatives:**
- **Intercom**: $79-128/month
- **Zendesk**: $55-115/month
- **You Save**: $800-1,200/year! 💰

### **Usage Estimates:**
- ~100 conversations/day = ~$10/month
- ~300 conversations/day = ~$25/month
- Each conversation costs about $0.003-0.005

---

## 🔐 API Key Management

### **Where Your API Key Is:**
The API key is stored in: `/Users/nathanielsteinrueck/nicole/.env`

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### **To Update It:**

**Option 1: Via Dashboard (Easiest)**
1. Go to Dashboard → Settings → API Configuration
2. Update the API key field
3. Click "Update API Settings"
4. Restart the server

**Option 2: Edit .env File Directly**
1. Open `/Users/nathanielsteinrueck/nicole/.env`
2. Update the `ANTHROPIC_API_KEY` line
3. Save
4. Restart server: `pkill -f uvicorn && uvicorn api.main:app --reload`

### **Getting a New API Key:**
1. Go to https://console.anthropic.com/settings/keys
2. Sign in with your Anthropic account
3. Create a new API key
4. Copy and paste into dashboard or .env file

### **API Key Security:**
- ✅ Never share your API key publicly
- ✅ Never commit it to GitHub (already in .gitignore)
- ✅ Rotate keys every 3-6 months
- ✅ Monitor usage at https://console.anthropic.com/account/usage

---

## 🚀 Daily Operations

### **What You Need to Do:**

#### **Weekly (~15 minutes):**
1. Check Dashboard → Overview for stats
2. Review any flagged emails (Gmail integration)
3. Update knowledge base if offerings change
4. Monitor conversation quality

#### **Monthly (~30 minutes):**
1. Review analytics (Dashboard → Analytics)
2. Check which questions are most common
3. Update featured workshops based on season
4. Review API usage and costs

#### **As Needed:**
1. Update booking URLs when schedule changes
2. Adjust confidence thresholds based on results
3. Customize assistant identity for campaigns
4. Edit templates for seasonal greetings

---

## 🛠️ Common Tasks

### **Task 1: Update Workshop Schedule**
1. Dashboard → Settings → Calendar & Scheduling
2. Update workshop booking URL if changed
3. Click "Save Scheduling Settings"
4. Done! Nicole will use new URL immediately

### **Task 2: Change Assistant Name**
1. Dashboard → Settings → AI Assistant Identity
2. Change name (e.g., "Nicole" → "Woody")
3. Update greeting message
4. Click "Save Identity Settings"
5. Test in chat widget

### **Task 3: Highlight Seasonal Workshops**
1. Dashboard → Settings → Event Display Settings
2. Update featured events list
3. Click "Save Event Settings"
4. Nicole will emphasize these workshops

### **Task 4: Adjust Auto-Send Threshold**
1. Dashboard → Settings → Confidence Thresholds
2. Move slider up (more cautious) or down (more aggressive)
3. Click "Save Thresholds"
4. Restart server for changes to apply

### **Task 5: Edit Workshop Information**
1. Dashboard → Knowledge Base
2. Edit the markdown content
3. Update pricing, descriptions, policies
4. Click "Save Changes"
5. Changes apply immediately

---

## 📱 Accessing from Different Devices

### **On Your Computer:**
- Dashboard: http://localhost:8000/dashboard/admin.html
- Chat Widget Test: http://localhost:8000/widget/test.html

### **On Your Phone/Tablet:**
- Find your computer's local IP address
- Use: http://[YOUR-IP]:8000/dashboard/admin.html
- Example: http://192.168.1.100:8000/dashboard/admin.html

### **In Production (After Deployment):**
- Dashboard: https://your-domain.com/dashboard/admin.html
- Chat widget automatically embeds on your website

---

## 🆘 Troubleshooting

### **Problem: Chat widget not showing**
**Solutions:**
1. Check the test page bottom-right corner
2. Scroll down to see the floating button
3. Hard refresh the page (Cmd+Shift+R on Mac)
4. Check server is running: http://localhost:8000/api/health

### **Problem: Changes not applying**
**Solutions:**
1. Click "Save" button after editing
2. Wait 5 seconds for settings to persist
3. Refresh the chat widget page
4. Check dashboard_config.json was updated

### **Problem: Server not running**
**Solutions:**
1. Open Terminal
2. Navigate to project: `cd /Users/nathanielsteinrueck/nicole`
3. Start server: `uvicorn api.main:app --reload`
4. Check health: http://localhost:8000/api/health

### **Problem: API key not working**
**Solutions:**
1. Verify key is correct (starts with sk-ant-api03-)
2. Check key hasn't expired
3. Test key at https://console.anthropic.com
4. Check API usage limits not exceeded

---

## 📞 Support Resources

### **Documentation:**
- `README.md` - Full technical documentation
- `QUICKSTART.md` - Quick setup guide
- `DASHBOARD_FEATURES.md` - Dashboard feature guide
- `DEPLOYMENT.md` - Production deployment guide
- `GMAIL_SETUP_STEINRUECKN.md` - Gmail integration setup

### **Testing:**
- Widget test page: http://localhost:8000/widget/test.html
- API health check: http://localhost:8000/api/health
- Dashboard: http://localhost:8000/dashboard/admin.html

### **Monitoring:**
- Server logs: `/tmp/nicole_server.log`
- API usage: https://console.anthropic.com/account/usage
- Dashboard stats: Real-time in Overview tab

---

## ✅ Initial Setup Checklist

Before going live, verify:

- [x] API key configured and working
- [x] Owner email set correctly
- [x] Dashboard accessible
- [x] Chat widget loads on test page
- [ ] Gmail integration configured (optional)
- [ ] Knowledge base updated with accurate info
- [ ] Booking URLs point to correct pages
- [ ] Test conversations work correctly
- [ ] Confidence thresholds adjusted
- [ ] Deploy to production server (Railway/Fly.io)

---

## 🎓 Training Recommendation

**15-Minute Walkthrough:**

1. **Minute 1-3:** Open dashboard, explore tabs
2. **Minute 4-6:** Change assistant name and greeting
3. **Minute 7-9:** Update booking URLs
4. **Minute 10-12:** Test chat widget with new settings
5. **Minute 13-15:** Review analytics and conversation history

**Do this together with the developer or owner to ensure comfort with the system!**

---

## 🎉 You're All Set!

**The system is configured and ready to use.**

**Next Steps:**
1. Open the dashboard: http://localhost:8000/dashboard/admin.html
2. Customize the assistant identity and settings
3. Test the chat widget: http://localhost:8000/widget/test.html
4. Set up Gmail integration (optional)
5. Deploy to production when ready

**Questions?** Refer to the documentation files or contact your developer.

---

**Nicole is ready to help Wood Thumb customers! 🪵✨**
