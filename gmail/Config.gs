/**
 * Configuration for Nicole Gmail Integration
 * Update these values for your setup
 */

function getConfig() {
  return {
    // Nicole API URL (update with your deployed API URL)
    NICOLE_API_URL: 'http://localhost:8000/api',  // Change to production URL

    // Gmail Labels
    PROCESSED_LABEL: 'Nicole/Processed',
    AUTO_SENT_LABEL: 'Nicole/Auto-Sent',
    DRAFT_LABEL: 'Nicole/Draft',
    FLAG_LABEL: 'Nicole/Needs Review',
    ERROR_LABEL: 'Nicole/Error',

    // Confidence Thresholds (should match API settings)
    HIGH_CONFIDENCE: 0.85,
    MEDIUM_CONFIDENCE: 0.60,

    // Google Sheets Logging (optional)
    LOG_TO_SHEETS: false,
    SHEET_ID: '',  // Add your Google Sheet ID if logging enabled

    // Rate Limiting
    MAX_EMAILS_PER_RUN: 10
  };
}
