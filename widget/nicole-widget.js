/**
 * Nicole Chat Widget
 * Embeddable chat widget for Wood Thumb website
 *
 * Usage: Add this script tag to your website:
 * <script src="https://your-api-url.com/widget/nicole-widget.js"></script>
 */

(function() {
  'use strict';

  // Configuration
  const CONFIG = {
    apiUrl: 'http://localhost:8000/api',  // Change in production
    streamingEnabled: true
  };

  // State
  let conversationHistory = [];
  let isOpen = false;
  let isProcessing = false;

  // Create widget HTML
  function createWidget() {
    const widgetHTML = `
      <!-- Widget Button -->
      <button class="nicole-widget-button" id="nicole-open-btn" aria-label="Open chat">
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"/>
        </svg>
      </button>

      <!-- Widget Container -->
      <div class="nicole-widget-container hidden" id="nicole-widget">
        <!-- Header -->
        <div class="nicole-widget-header">
          <div class="nicole-widget-title">
            <div class="nicole-widget-avatar">N</div>
            <div class="nicole-widget-name">
              <h3>Nicole</h3>
              <p>AI Assistant</p>
            </div>
          </div>
          <button class="nicole-widget-close" id="nicole-close-btn" aria-label="Close chat">×</button>
        </div>

        <!-- Messages -->
        <div class="nicole-widget-messages" id="nicole-messages">
          <div class="nicole-message">
            <div class="nicole-message-avatar">N</div>
            <div class="nicole-message-wrapper">
              <div class="nicole-message-content">
                Hi! I'm Nicole, Wood Thumb's AI assistant. How can I help?
              </div>
            </div>
          </div>
          <div class="nicole-quick-replies" id="nicole-quick-replies">
            <button class="nicole-quick-reply" data-message="What workshops do you offer?">Workshops</button>
            <button class="nicole-quick-reply" data-message="How much do workshops cost?">Pricing</button>
            <button class="nicole-quick-reply" data-message="I want to plan a team event">Team Event</button>
            <button class="nicole-quick-reply" data-message="Tell me about shop time">Shop Time</button>
          </div>
        </div>

        <!-- Input -->
        <div class="nicole-widget-input">
          <textarea
            id="nicole-input"
            placeholder="Type your message..."
            rows="1"
          ></textarea>
          <button id="nicole-send-btn">Send</button>
        </div>
      </div>
    `;

    // Inject CSS
    const style = document.createElement('link');
    style.rel = 'stylesheet';
    style.href = CONFIG.apiUrl.replace('/api', '/widget/nicole-widget.css');
    document.head.appendChild(style);

    // Inject HTML
    const container = document.createElement('div');
    container.innerHTML = widgetHTML;
    document.body.appendChild(container);
  }

  // Toggle widget
  function toggleWidget() {
    const widget = document.getElementById('nicole-widget');
    isOpen = !isOpen;

    if (isOpen) {
      widget.classList.remove('hidden');
      document.getElementById('nicole-input').focus();
    } else {
      widget.classList.add('hidden');
    }
  }

  // Sanitize HTML but allow specific tags
  function sanitizeHtml(html) {
    const div = document.createElement('div');
    div.textContent = html;
    let sanitized = div.innerHTML;

    // Allow <strong> tags for bold event names
    sanitized = sanitized.replace(/&lt;strong&gt;/g, '<strong>').replace(/&lt;\/strong&gt;/g, '</strong>');

    // Allow <ul> and <li> tags for lists
    sanitized = sanitized.replace(/&lt;ul&gt;/g, '<ul>').replace(/&lt;\/ul&gt;/g, '</ul>');
    sanitized = sanitized.replace(/&lt;li&gt;/g, '<li>').replace(/&lt;\/li&gt;/g, '</li>');

    return sanitized;
  }

  // Add message to UI
  function addMessage(content, isUser = false, bookingLink = null) {
    const messagesContainer = document.getElementById('nicole-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `nicole-message ${isUser ? 'user' : ''}`;

    let messageHTML = `
      <div class="nicole-message-avatar">${isUser ? 'Y' : 'N'}</div>
      <div class="nicole-message-wrapper">
        <div class="nicole-message-content">${isUser ? escapeHtml(content) : sanitizeHtml(content)}</div>
    `;

    // Add Book Now chip if booking link provided
    if (bookingLink && !isUser) {
      messageHTML += `
        <div class="nicole-booking-chip">
          <a href="${bookingLink}" target="_blank" rel="noopener">Book Now</a>
        </div>
      `;
    }

    messageHTML += `</div>`; // Close wrapper

    messageDiv.innerHTML = messageHTML;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;

    return messageDiv;
  }

  // Show typing indicator
  function showTyping() {
    const messagesContainer = document.getElementById('nicole-messages');
    const typingDiv = document.createElement('div');
    typingDiv.id = 'nicole-typing-indicator';
    typingDiv.className = 'nicole-message';
    typingDiv.innerHTML = `
      <div class="nicole-message-avatar">N</div>
      <div class="nicole-message-wrapper">
        <div class="nicole-message-content">
          <div class="nicole-typing">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    `;
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  // Remove typing indicator
  function removeTyping() {
    const typing = document.getElementById('nicole-typing-indicator');
    if (typing) typing.remove();
  }

  // Hide quick replies after first interaction
  function hideQuickReplies() {
    const quickReplies = document.getElementById('nicole-quick-replies');
    if (quickReplies) {
      quickReplies.style.display = 'none';
    }
  }

  // Send message (streaming)
  async function sendMessage(message) {
    if (!message.trim() || isProcessing) return;

    isProcessing = true;
    const sendBtn = document.getElementById('nicole-send-btn');
    const input = document.getElementById('nicole-input');
    sendBtn.disabled = true;

    // Hide quick replies after first message
    hideQuickReplies();

    // Add user message
    addMessage(message, true);
    conversationHistory.push({ role: 'user', content: message });
    input.value = '';
    input.style.height = 'auto';

    showTyping();

    try {
      const response = await fetch(`${CONFIG.apiUrl}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: message,
          conversation_history: conversationHistory,
          stream: CONFIG.streamingEnabled
        })
      });

      removeTyping();

      if (CONFIG.streamingEnabled) {
        // Handle streaming response
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let botMessage = null;
        let fullResponse = '';

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.slice(6));

                if (data.type === 'chunk') {
                  fullResponse += data.content;

                  if (!botMessage) {
                    botMessage = addMessage('');
                  }

                  const contentDiv = botMessage.querySelector('.nicole-message-content');
                  contentDiv.innerHTML = sanitizeHtml(fullResponse);

                } else if (data.type === 'complete') {
                  conversationHistory.push({
                    role: 'assistant',
                    content: data.response
                  });

                  // Add action chips based on response content
                  if (botMessage) {
                    const messageWrapper = botMessage.querySelector('.nicole-message-wrapper');
                    const followUpChips = getFollowUpChips(fullResponse);

                    // Show follow-up chips if available
                    if (followUpChips.length > 0) {
                      const chipsContainer = document.createElement('div');
                      chipsContainer.className = 'nicole-action-chips';

                      followUpChips.forEach(chip => {
                        if (chip.link) {
                          chipsContainer.innerHTML += `<a href="${chip.link}" target="_blank" rel="noopener" class="nicole-action-chip">${chip.text}</a>`;
                        } else if (chip.action) {
                          chipsContainer.innerHTML += `<button class="nicole-action-chip" onclick="document.getElementById('nicole-input').value='${chip.action}'; document.getElementById('nicole-send-btn').click();">${chip.text}</button>`;
                        }
                      });

                      messageWrapper.appendChild(chipsContainer);
                    }
                  }
                } else if (data.type === 'error') {
                  if (!botMessage) {
                    addMessage(data.error);
                  }
                }
              } catch (e) {
                console.error('Parse error:', e);
              }
            }
          }
        }
      } else {
        // Handle non-streaming response
        const data = await response.json();
        addMessage(data.response);
        conversationHistory.push({
          role: 'assistant',
          content: data.response
        });
      }

    } catch (error) {
      removeTyping();
      addMessage('Sorry, I\'m having trouble connecting. Please try again or email info@woodthumb.com');
      console.error('Chat error:', error);
    }

    isProcessing = false;
    sendBtn.disabled = false;
    input.focus();
  }

  // Extract booking link from message
  function extractBookingLink(message) {
    // Look for Xola or Acuity links in the message
    const xolaMatch = message.match(/https:\/\/[^\s]*xola[^\s]*/i);
    const acuityMatch = message.match(/https:\/\/woodthumb\.as\.me[^\s]*/i);

    if (acuityMatch) return acuityMatch[0];
    if (xolaMatch) return xolaMatch[0];

    return null;
  }

  // Specific event booking URLs
  const eventBookingLinks = {
    'cutting board': 'https://woodthumb.as.me/schedule/73e6f342/appointment/30929470/calendar/6567272?appointmentTypeIds[]=30929470',
    'knife rack': 'https://woodthumb.as.me/schedule/73e6f342/appointment/30929470/calendar/6567272?appointmentTypeIds[]=30929470',
    'bottle opener': 'https://woodthumb.as.me/schedule/73e6f342/appointment/30929534/calendar/6567272?appointmentTypeIds[]=30929534',
    'vase': 'https://woodthumb.as.me/schedule/73e6f342/appointment/30929534/calendar/6567272?appointmentTypeIds[]=30929534',
    'pinewood': 'https://woodthumb.as.me/schedule/73e6f342/appointment/41395938/calendar/6567272?appointmentTypeIds[]=41395938',
    'derby': 'https://woodthumb.as.me/schedule/73e6f342/appointment/41395938/calendar/6567272?appointmentTypeIds[]=41395938',
    'triangle shelf': 'https://woodthumb.as.me/schedule/73e6f342/appointment/30930450/calendar/6567272?appointmentTypeIds[]=30930450',
    'picture frame': 'https://woodthumb.as.me/schedule/73e6f342/appointment/81003629/calendar/6567272?appointmentTypeIds[]=81003629',
    'virtual': 'https://woodthumb.as.me/schedule/73e6f342/appointment/30929181/calendar/6567272?appointmentTypeIds[]=30929181'
  };

  // Detect specific event interest and return booking link
  function detectSpecificEvent(message) {
    const lowerMessage = message.toLowerCase();
    for (const [event, link] of Object.entries(eventBookingLinks)) {
      if (lowerMessage.includes(event)) {
        return link;
      }
    }
    return null;
  }

  // Detect what type of response and suggest follow-up actions
  function getFollowUpChips(message) {
    const chips = [];
    const lowerMessage = message.toLowerCase();

    // Check if it's a list of multiple events (has <ul> or lists 3+ events)
    const isEventList = message.includes('<ul>') || (message.match(/<strong>/g) || []).length >= 3;

    // If listing team events with prices (after specifying team size)
    if (isEventList && message.includes('$') && message.includes('total')) {
      chips.push({ text: 'Book Team Event', link: 'https://woodthumb.as.me/schedule/73e6f342' });
      chips.push({ text: 'Ask Question', action: 'I have a question about team events' });
      return chips;
    }

    // If discussing specific event with price (NOT a list)
    const specificEventLink = detectSpecificEvent(message);
    if (!isEventList && specificEventLink && message.includes('$')) {
      chips.push({ text: 'Book This Event', link: specificEventLink });
      chips.push({ text: 'See Other Events', action: 'What other team events do you have?' });
      return chips;
    }
    // If asking about team size
    else if (lowerMessage.includes('how many people') || lowerMessage.includes('attending')) {
      // No chips needed - waiting for user to respond with number
    }
    // If listing team events (general list without prices)
    else if (lowerMessage.includes('team') && (message.includes('Cutting Board') || message.includes('Derby') || message.includes('Bottle')) && !message.includes('$')) {
      chips.push({ text: 'Book Team Event', link: 'https://woodthumb.as.me/schedule/73e6f342' });
      chips.push({ text: 'See Prices', action: 'What are the prices for team events?' });
    }
    // If listing workshops (general list)
    else if ((message.includes('Triangle') || message.includes('Cutting Board') || message.includes('Wedge')) && !message.includes('$')) {
      chips.push({ text: 'View Schedule', link: 'https://woodthumb.com/workshops' });
      chips.push({ text: 'See Prices', action: 'What are the workshop prices?' });
    }
    // If showing prices for multiple events
    else if (message.includes('$') && (message.includes('Cutting Board') || message.includes('Derby')) && message.includes('person')) {
      chips.push({ text: 'Book Team Event', link: 'https://woodthumb.as.me/schedule/73e6f342' });
      chips.push({ text: 'Help Me Choose', action: 'Help me choose a team event' });
    }
    // General pricing info (fallback)
    else if (message.includes('$')) {
      chips.push({ text: 'Book Now', link: 'https://woodthumb.com/workshops' });
      chips.push({ text: 'Ask Question', action: 'I have a question' });
    }

    return chips;
  }

  // Escape HTML
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Auto-resize textarea
  function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
  }

  // Initialize widget
  function init() {
    createWidget();

    // Event listeners
    document.getElementById('nicole-open-btn').addEventListener('click', toggleWidget);
    document.getElementById('nicole-close-btn').addEventListener('click', toggleWidget);

    const sendBtn = document.getElementById('nicole-send-btn');
    const input = document.getElementById('nicole-input');

    sendBtn.addEventListener('click', () => {
      sendMessage(input.value);
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage(input.value);
      }
    });

    input.addEventListener('input', (e) => {
      autoResize(e.target);
    });

    // Quick reply buttons
    const quickReplyButtons = document.querySelectorAll('.nicole-quick-reply');
    quickReplyButtons.forEach(button => {
      button.addEventListener('click', () => {
        const message = button.getAttribute('data-message');
        sendMessage(message);
      });
    });
  }

  // Load when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
