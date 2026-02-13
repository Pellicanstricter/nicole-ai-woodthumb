# Gmail Setup Guide for steinrueckn@gmail.com

**Complete step-by-step guide to connect Nicole to your Gmail account**

## What This Will Do

Once set up, Nicole will:
- ✅ Check steinrueckn@gmail.com inbox every 5 minutes
- ✅ Read new unread emails
- ✅ Analyze them and generate responses
- ✅ **High confidence (>85%)**: Auto-send reply immediately
- ✅ **Medium confidence (60-85%)**: Save as Gmail draft for your review
- ✅ **Low confidence (<60%)**: Flag email and add detailed note
- ✅ Organize emails with labels like `Nicole/Auto-Sent`, `Nicole/Draft`, etc.

## Security Note

You will be granting permissions through **Google's official Apps Script** platform. This is:
- ✅ Owned and secured by Google
- ✅ Only accessible by you (steinrueckn@gmail.com)
- ✅ Can be revoked anytime
- ✅ Does NOT share your password with anyone
- ✅ Uses OAuth (same security as Gmail add-ons)

---

## Step 1: Go to Google Apps Script (2 minutes)

1. **Open your browser** and go to: https://script.google.com
2. **Sign in** with steinrueckn@gmail.com if not already signed in
3. You'll see the Google Apps Script dashboard

---

## Step 2: Create New Project (1 minute)

1. Click the **"+ New Project"** button (top left)
2. A new editor will open with `Code.gs` and some default code
3. **Rename the project:**
   - Click "Untitled project" at the top
   - Change name to: **Nicole Gmail Integration**
   - Click anywhere outside to save

---

## Step 3: Add the Code Files (5 minutes)

### 3a. Replace Code.gs

1. **Select ALL the default code** in Code.gs (Cmd+A or Ctrl+A)
2. **Delete it**
3. **Copy the code from**:  `/Users/nathanielsteinrueck/nicole/gmail/Code.gs`
4. **Paste it** into the empty Code.gs file

To copy the code, run this in your terminal:
```bash
cat /Users/nathanielsteinrueck/nicole/gmail/Code.gs | pbcopy
```
Then paste in the Apps Script editor

### 3b. Add Config.gs

1. Click the **"+"** icon next to "Files" in the left sidebar
2. Select **"Script"**
3. Name it: **Config**
4. **Copy the code from**: `/Users/nathanielsteinrueck/nicole/gmail/Config.gs`
5. **Paste it** into Config.gs

To copy:
```bash
cat /Users/nathanielsteinrueck/nicole/gmail/Config.gs | pbcopy
```

### 3c. Update Config.gs with API URL

⚠️ **IMPORTANT:** We need to make Nicole accessible from the internet.

**For now, use ngrok to expose your local server:**

```bash
# In a NEW terminal window (keep Nicole server running)
brew install ngrok  # if not installed

# Expose port 8000
ngrok http 8000
```

You'll see output like:
```
Forwarding  https://a1b2c3d4.ngrok.io -> http://localhost:8000
```

Copy the **HTTPS URL** (e.g., `https://a1b2c3d4.ngrok.io`)

Now in Config.gs, update line 8:
```javascript
// CHANGE THIS LINE:
NICOLE_API_URL: 'http://localhost:8000/api',

// TO THIS (using YOUR ngrok URL):
NICOLE_API_URL: 'https://a1b2c3d4.ngrok.io/api',
```

**Save** (Cmd+S or Ctrl+S)

---

## Step 4: Run Initial Setup (3 minutes)

1. At the top of the editor, find the **dropdown menu** (currently says "Select function")
2. Click it and select: **setup**
3. Click the **▶ Run** button (play icon)

### Grant Permissions

A dialog will appear:

1. **"Authorization required"** → Click **Review permissions**
2. **Choose your account** → steinrueckn@gmail.com
3. **"Google hasn't verified this app"** → Click **Advanced**
4. Click **"Go to Nicole Gmail Integration (unsafe)"**
   - Don't worry! This is YOUR script, it's safe
5. **Review permissions** → Click **Allow**

The script needs:
- Read and modify Gmail messages
- Create labels
- Send emails on your behalf

### Check Execution Log

1. After granting permissions, the setup will run
2. Click **"Execution log"** tab at the bottom
3. You should see:
```
Info: Created/verified label: Nicole/Processed
Info: Created/verified label: Nicole/Auto-Sent
Info: Created/verified label: Nicole/Draft
Info: Created/verified label: Nicole/Needs Review
Info: Created/verified label: Nicole/Error
Info: Setup complete! Now set up a time-based trigger for processNewEmails()
```

### Verify Labels in Gmail

1. Go to Gmail: https://mail.google.com
2. Look in the left sidebar under your folders
3. You should see a new **"Nicole"** section with sub-labels:
   - Nicole/Processed
   - Nicole/Auto-Sent
   - Nicole/Draft
   - Nicole/Needs Review
   - Nicole/Error

---

## Step 5: Test with One Email (5 minutes)

Before setting up automatic processing, let's test manually:

### 5a. Send a Test Email

1. From **another email address** (or use a different Gmail account)
2. Send an email TO: **steinrueckn@gmail.com**
3. **Subject:** "Workshop Question"
4. **Body:** "Hi, what workshops do you have for beginners? How much are they?"

### 5b. Run Manual Test

Back in Google Apps Script:

1. Select function: **testWithLatestEmail**
2. Click **▶ Run**
3. Wait 10-15 seconds

### 5c. Check Execution Log

You should see:
```
Info: Testing with email:
Info: From: sender@example.com
Info: Subject: Workshop Question
Info: API Response:
{
  "response": "...[Nicole's response]...",
  "intent": "workshop_inquiry",
  "confidence": 0.92,
  "routing": "auto_send"
}
```

### 5d. Check Gmail

1. Go to your Gmail inbox
2. You should see:
   - The test email now has the `Nicole/Processed` label
   - Based on the routing in the log:
     - **If "auto_send"**: Nicole replied to the email automatically
     - **If "draft"**: Check Drafts folder for Nicole's response
     - **If "flag"**: Email is starred with a note from Nicole

---

## Step 6: Set Up Automatic Trigger (3 minutes)

Now make Nicole check your inbox automatically every 5 minutes:

### 6a. Create Trigger

1. In the left sidebar, click the **⏰ clock icon** ("Triggers")
2. Click **"+ Add Trigger"** button (bottom right)

### 6b. Configure Trigger

Set these options:

- **Choose which function to run:** `processNewEmails`
- **Choose which deployment should run:** Head
- **Select event source:** Time-driven
- **Select type of time based trigger:** Minutes timer
- **Select minute interval:** Every 5 minutes

### 6c. Save

1. Click **"Save"**
2. You may need to authorize again - if so, follow same steps as Step 4

### 6d. Verify Trigger Active

1. You should see your new trigger listed
2. It shows: `processNewEmails`, "Time-driven", "Every 5 minutes"
3. Status should be **Active** ✅

---

## Step 7: Test Full Automatic Flow (5 minutes)

Now let's test the complete automation:

### 7a. Send Another Test Email

From a different email, send to steinrueckn@gmail.com:

**Test 1 - High Confidence (Should Auto-Send):**
- Subject: "Your Hours"
- Body: "Hi, what are your operating hours?"

Wait 5-6 minutes, then check Gmail:
- Should have Nicole's auto-reply
- Email labeled `Nicole/Auto-Sent`

**Test 2 - Medium Confidence (Should Draft):**
- Subject: "Team Event"
- Body: "We're interested in a team event for 15 people. Can you provide details and pricing?"

Wait 5-6 minutes, then check:
- Draft reply in Drafts folder
- Email labeled `Nicole/Draft`

**Test 3 - Low Confidence (Should Flag):**
- Subject: "Complex Request"
- Body: "I need a completely custom artisan piece for an installation art project with very specific requirements"

Wait 5-6 minutes, then check:
- Email is starred/flagged
- Draft contains Nicole's summary and suggested response
- Email labeled `Nicole/Needs Review`

---

## Step 8: Monitor & Adjust (Ongoing)

### Check Executions

1. Apps Script → **Executions** (lightning bolt icon)
2. See all recent runs of `processNewEmails`
3. Click any to see logs

### Adjust Confidence Thresholds (Optional)

If Nicole is too cautious (creating too many drafts) or too aggressive (auto-sending when it shouldn't):

1. Edit `Config.gs`
2. Change these values:
```javascript
HIGH_CONFIDENCE: 0.85,  // Increase to be more cautious (0.90)
MEDIUM_CONFIDENCE: 0.60, // Adjust as needed
```

### Stop Processing Temporarily

1. Go to Triggers (⏰)
2. Click three dots (⋮) next to trigger
3. Click "Delete"
4. Nicole stops checking emails

### Resume Processing

1. Follow Step 6 again to recreate trigger

---

## Troubleshooting

### "No unread emails found" in test

**Solution:** Make sure you have an unread email in your inbox

### "API call failed"

**Solutions:**
1. Check ngrok is still running (it expires after 8 hours on free plan)
2. Update `Config.gs` with new ngrok URL if it changed
3. Verify Nicole server is running: `curl http://localhost:8000/api/health`

### Emails not being processed

**Check:**
1. Trigger is active (⏰ Triggers page)
2. No errors in Executions log
3. Emails are actually in inbox (not spam/promotions)
4. Emails are unread

### Too many auto-sends

**Solution:** Increase `HIGH_CONFIDENCE` threshold in Config.gs to 0.90 or higher

### Not enough auto-sends (everything is drafts)

**Solution:** Decrease `HIGH_CONFIDENCE` threshold to 0.75 or 0.80

---

## Production Deployment (When Ready)

For permanent use (not just testing):

### Deploy Nicole API

1. Follow `DEPLOYMENT.md` to deploy to Railway or Fly.io
2. Get permanent production URL (e.g., `https://nicole-woodthumb.up.railway.app`)
3. Update `Config.gs` with production URL:
```javascript
NICOLE_API_URL: 'https://nicole-woodthumb.up.railway.app/api',
```

### Switch to Production Gmail

If you want to use this for the actual business email (info@woodthumb.com):

1. Sign in to Apps Script with that account
2. Follow all same steps above
3. Create separate project for production

---

## What Happens Behind the Scenes

Every 5 minutes, the script:

1. **Searches Gmail** for: `is:unread in:inbox -label:Nicole/Processed`
2. **Gets latest message** from each thread
3. **Calls Nicole API** with email content
4. **Nicole analyzes** the email:
   - Classifies intent (workshop inquiry, team event, etc.)
   - Generates appropriate response
   - Assigns confidence score
   - Decides routing (auto-send, draft, or flag)
5. **Takes action** based on routing:
   - **Auto-send**: Sends reply immediately
   - **Draft**: Creates draft for your review
   - **Flag**: Stars email and adds detailed note
6. **Adds label** to track processing status
7. **Repeats** in 5 minutes

---

## Security & Privacy

### What Nicole Can Access

- ✅ Read emails in your inbox
- ✅ Send emails as you
- ✅ Create drafts
- ✅ Create and apply labels
- ✅ Star/flag emails

### What Nicole CANNOT Access

- ❌ Your Gmail password
- ❌ Emails in other accounts
- ❌ Contacts outside of email threads
- ❌ Google Drive files
- ❌ Calendar events

### How to Revoke Access

If you ever want to disconnect Nicole:

1. Go to: https://myaccount.google.com/permissions
2. Find "Nicole Gmail Integration"
3. Click "Remove Access"

---

## Support

### If Something Goes Wrong

1. **Check Execution logs** in Apps Script
2. **Test manually** using `testWithLatestEmail`
3. **Verify API** is accessible: Test with curl
4. **Review trigger** is still active

### Common Issues

- **ngrok URL expired**: Restart ngrok, update Config.gs
- **Port 8000 not accessible**: Restart Nicole server
- **Permission denied**: Re-authorize in Apps Script

---

## Next Steps After Testing

Once you're comfortable with how Nicole works:

1. ✅ Deploy Nicole API to production (Railway/Fly.io)
2. ✅ Update Config.gs with production URL
3. ✅ Adjust confidence thresholds based on results
4. ✅ Consider setting up for production email account
5. ✅ Monitor first week closely, make adjustments
6. ✅ Update knowledge base with real business info

---

**You're all set!** 🎉

Nicole will now help manage your Gmail inbox automatically, with intelligent routing to ensure important emails get your personal attention while routine questions are handled instantly.

Questions? Run through the troubleshooting section or test manually using the functions in Apps Script.
