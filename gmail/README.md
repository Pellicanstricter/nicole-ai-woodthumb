# Nicole Gmail Integration

Google Apps Script that monitors Gmail inbox and uses Nicole API to automatically handle customer service emails.

## Setup Instructions

### 1. Create Google Apps Script Project

1. Go to [script.google.com](https://script.google.com)
2. Click "New Project"
3. Name it "Nicole Gmail Integration"

### 2. Add the Code

1. Delete the default `Code.gs` content
2. Copy `Code.gs` from this directory
3. Click the "+" next to Files and add `Config.gs`
4. Copy `Config.gs` content

### 3. Configure Settings

In `Config.gs`, update:
- `NICOLE_API_URL` - Your deployed Nicole API URL
- `SHEET_ID` - (Optional) Google Sheet ID for logging

### 4. Authorize and Setup

1. Click the "Run" dropdown
2. Select `setup` function
3. Click "Run"
4. Grant permissions when prompted
5. Check logs to verify labels were created

### 5. Create Trigger

1. Click the clock icon (Triggers) in left sidebar
2. Click "+ Add Trigger"
3. Configure:
   - Function: `processNewEmails`
   - Deployment: Head
   - Event source: Time-driven
   - Type: Minutes timer
   - Interval: Every 5 minutes
4. Save

## How It Works

### Email Processing Flow

1. **Every 5 minutes**, script checks for unread emails
2. **Extracts** email content and sender
3. **Calls Nicole API** with email data
4. **Routes response** based on confidence:
   - **High confidence (>85%)**: Auto-send reply
   - **Medium confidence (60-85%)**: Save as draft
   - **Low confidence (<60%)**: Flag for owner review

### Gmail Labels

The script creates these labels automatically:
- `Nicole/Processed` - All emails Nicole has handled
- `Nicole/Auto-Sent` - Emails where Nicole auto-replied
- `Nicole/Draft` - Emails saved as drafts
- `Nicole/Needs Review` - Emails flagged for owner
- `Nicole/Error` - Emails that had processing errors

## Testing

### Test with Latest Email

1. Have an unread test email in your inbox
2. Run `testWithLatestEmail` function
3. Check logs to see API response
4. Email won't be processed (dry run)

### Test Full Flow

1. Send a test email to your Gmail
2. Wait up to 5 minutes for trigger
3. Check labels to see how it was routed
4. Review drafts folder if medium confidence

## Monitoring

### Check Logs

1. Click "Executions" in left sidebar
2. View recent runs and any errors

### Google Sheets Logging (Optional)

1. Create a Google Sheet
2. Copy Sheet ID from URL
3. Update `SHEET_ID` in Config.gs
4. Set `LOG_TO_SHEETS: true`

Sheet will log:
- Timestamp
- From email
- Intent
- Confidence
- Routing decision
- Response preview

## Troubleshooting

### "API call failed"
- Check `NICOLE_API_URL` is correct
- Verify API is running and accessible
- Check API logs for errors

### "No unread emails found"
- Emails may already be marked read
- Check label filters aren't excluding emails
- Verify emails are in inbox (not spam/other folders)

### High error rate
- Review error logs
- Check API rate limits
- Verify confidence thresholds are appropriate

## Customization

### Change Processing Frequency

Edit trigger interval (minimum: every 1 minute, maximum: daily)

### Adjust Confidence Thresholds

Update in `Config.gs` to match your API settings

### Custom Email Filtering

Modify search query in `processNewEmails()`:
```javascript
const query = 'is:unread in:inbox from:specific@domain.com';
```

## Security Notes

- Script runs with your Gmail permissions
- Only you can see the script code
- API calls are logged in Apps Script execution logs
- Consider using a dedicated Gmail account for production
