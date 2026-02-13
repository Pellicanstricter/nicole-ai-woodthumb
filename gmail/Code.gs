/**
 * Nicole Gmail Integration
 * Google Apps Script that monitors Gmail and calls Nicole API
 *
 * Setup:
 * 1. Go to script.google.com
 * 2. Create new project
 * 3. Paste this code
 * 4. Update NICOLE_API_URL in Config.gs
 * 5. Run setup() function to authorize
 * 6. Set time-based trigger: processNewEmails every 5 minutes
 */


/**
 * Process new emails in inbox
 * Called every 5 minutes by trigger
 */
function processNewEmails() {
  const config = getConfig();

  // Search for unread emails in inbox
  const query = 'is:unread in:inbox -label:' + config.PROCESSED_LABEL;
  const threads = GmailApp.search(query, 0, 10); // Process max 10 at a time

  Logger.log(`Found ${threads.length} unread threads to process`);

  threads.forEach(thread => {
    try {
      const messages = thread.getMessages();
      const latestMessage = messages[messages.length - 1];

      // Skip if it's our own reply
      if (latestMessage.getFrom().includes(Session.getActiveUser().getEmail())) {
        Logger.log('Skipping own reply');
        return;
      }

      // Get email details
      const fromEmail = extractEmail(latestMessage.getFrom());
      const subject = latestMessage.getSubject();
      const body = latestMessage.getPlainBody();
      const threadId = thread.getId();

      Logger.log(`Processing email from: ${fromEmail}`);

      // Call Nicole API
      const response = callNicoleAPI({
        from_email: fromEmail,
        subject: subject,
        body: body,
        thread_id: threadId
      });

      if (!response) {
        Logger.log('API call failed, will retry next run');
        return;
      }

      // Handle response based on routing decision
      handleResponse(thread, response, fromEmail);

      // Mark as processed
      GmailApp.getUserLabelByName(config.PROCESSED_LABEL).addToThread(thread);

    } catch (error) {
      Logger.log(`Error processing thread: ${error}`);
      // Add error label for manual review
      GmailApp.getUserLabelByName(config.ERROR_LABEL).addToThread(thread);
    }
  });
}


/**
 * Call Nicole API with email data
 */
function callNicoleAPI(emailData) {
  const config = getConfig();

  try {
    const response = UrlFetchApp.fetch(config.NICOLE_API_URL + '/email', {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(emailData),
      muteHttpExceptions: true
    });

    if (response.getResponseCode() !== 200) {
      Logger.log(`API error: ${response.getContentText()}`);
      return null;
    }

    return JSON.parse(response.getContentText());

  } catch (error) {
    Logger.log(`API call error: ${error}`);
    return null;
  }
}


/**
 * Handle API response based on routing decision
 */
function handleResponse(thread, response, fromEmail) {
  const config = getConfig();

  Logger.log(`Routing: ${response.routing}, Confidence: ${response.confidence}`);

  switch (response.routing) {
    case 'auto_send':
      // High confidence - send reply automatically
      sendReply(thread, response.response);
      GmailApp.getUserLabelByName(config.AUTO_SENT_LABEL).addToThread(thread);
      Logger.log('Auto-sent reply');
      break;

    case 'draft':
      // Medium confidence - save as draft
      createDraft(thread, response.response);
      GmailApp.getUserLabelByName(config.DRAFT_LABEL).addToThread(thread);
      Logger.log('Created draft');
      break;

    case 'flag':
      // Low confidence - flag for owner
      flagForReview(thread, response);
      GmailApp.getUserLabelByName(config.FLAG_LABEL).addToThread(thread);
      Logger.log('Flagged for review');
      break;
  }

  // Log to Google Sheet (if enabled)
  if (config.LOG_TO_SHEETS) {
    logToSheet(fromEmail, response);
  }
}


/**
 * Send reply to thread
 */
function sendReply(thread, responseText) {
  thread.reply(responseText, {
    from: Session.getActiveUser().getEmail(),
    name: 'Wood Thumb (via Nicole)'
  });
  thread.markRead();
}


/**
 * Create draft reply
 */
function createDraft(thread, responseText) {
  const message = thread.getMessages()[thread.getMessages().length - 1];

  GmailApp.createDraft(
    message.getFrom(),
    message.getSubject(),
    responseText,
    {
      inReplyTo: message.getId(),
      references: message.getId()
    }
  );
}


/**
 * Flag email for owner review
 */
function flagForReview(thread, response) {
  const summary = `
⚠️ NICOLE: This email requires your attention

Intent: ${response.intent}
Confidence: ${(response.confidence * 100).toFixed(0)}%
Reasoning: ${response.reasoning}

---
Nicole's suggested response (review before sending):

${response.response}
  `;

  // Add note to thread by replying to self as draft
  const message = thread.getMessages()[thread.getMessages().length - 1];
  GmailApp.createDraft(
    message.getFrom(),
    'Re: ' + message.getSubject(),
    summary
  );

  // Star the thread
  thread.markImportant();
  thread.addLabel(GmailApp.getUserLabelByName(getConfig().FLAG_LABEL));
}


/**
 * Extract email address from "Name <email>" format
 */
function extractEmail(fromString) {
  const match = fromString.match(/<(.+?)>/);
  return match ? match[1] : fromString;
}


/**
 * Log conversation to Google Sheet
 */
function logToSheet(fromEmail, response) {
  const config = getConfig();

  try {
    const sheet = SpreadsheetApp.openById(config.SHEET_ID).getActiveSheet();
    sheet.appendRow([
      new Date(),
      fromEmail,
      response.intent,
      response.confidence,
      response.routing,
      response.response.substring(0, 500) // First 500 chars
    ]);
  } catch (error) {
    Logger.log(`Sheet logging error: ${error}`);
  }
}


/**
 * Setup function - run once to create labels
 */
function setup() {
  const config = getConfig();

  // Create labels if they don't exist
  const labels = [
    config.PROCESSED_LABEL,
    config.AUTO_SENT_LABEL,
    config.DRAFT_LABEL,
    config.FLAG_LABEL,
    config.ERROR_LABEL
  ];

  labels.forEach(labelName => {
    try {
      GmailApp.getUserLabelByName(labelName) || GmailApp.createLabel(labelName);
      Logger.log(`Created/verified label: ${labelName}`);
    } catch (error) {
      Logger.log(`Error creating label ${labelName}: ${error}`);
    }
  });

  Logger.log('Setup complete! Now set up a time-based trigger for processNewEmails()');
}


/**
 * Test function - process one test email
 */
function testWithLatestEmail() {
  const threads = GmailApp.search('is:unread in:inbox', 0, 1);

  if (threads.length === 0) {
    Logger.log('No unread emails found');
    return;
  }

  const thread = threads[0];
  const message = thread.getMessages()[thread.getMessages().length - 1];

  Logger.log('Testing with email:');
  Logger.log(`From: ${message.getFrom()}`);
  Logger.log(`Subject: ${message.getSubject()}`);

  const response = callNicoleAPI({
    from_email: extractEmail(message.getFrom()),
    subject: message.getSubject(),
    body: message.getPlainBody(),
    thread_id: thread.getId()
  });

  Logger.log('API Response:');
  Logger.log(JSON.stringify(response, null, 2));
}
