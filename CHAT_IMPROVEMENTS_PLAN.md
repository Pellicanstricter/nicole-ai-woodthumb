# Chat Experience & Schedule Integration - Improvement Plan

**Making Nicole smarter with real-time workshop availability**

---

## 🎯 Goals

1. **Show Real Workshop Schedules** - Display actual upcoming workshop dates/times
2. **Improve Chat UX** - Make conversations more engaging and intuitive
3. **Add Quick Actions** - Buttons for common questions
4. **Enable Direct Booking** - Let customers book from chat (stretch goal)

---

## 📅 Part 1: Schedule Integration with Xola

### **Option A: Xola API Integration (Best)**

**What Xola API Can Provide:**
- List of all workshops (experiences)
- Available dates and times for each workshop
- Real-time seat availability
- Pricing information
- Direct booking capabilities

**Implementation Steps:**

#### **1. Get Xola API Credentials**
```
Contact Wood Thumb owner to:
- Sign up for Xola API access
- Get API key and seller ID
- Review API documentation at: https://xola.com/api
```

#### **2. Create Xola Integration Module**
```python
# api/xola_integration.py

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os

class XolaClient:
    def __init__(self):
        self.api_key = os.getenv('XOLA_API_KEY')
        self.seller_id = os.getenv('XOLA_SELLER_ID')
        self.base_url = f"https://xola.app/api/{self.seller_id}"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def get_experiences(self) -> List[Dict]:
        """Get all workshop/experience listings"""
        response = requests.get(
            f"{self.base_url}/experiences",
            headers=self.headers
        )
        return response.json().get('data', [])

    def get_availability(
        self,
        experience_id: str,
        start_date: str = None,
        end_date: str = None
    ) -> List[Dict]:
        """Get available time slots for a workshop"""
        if not start_date:
            start_date = datetime.now().strftime('%Y-%m-%d')
        if not end_date:
            end_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')

        response = requests.get(
            f"{self.base_url}/experiences/{experience_id}/availability",
            headers=self.headers,
            params={
                'from': start_date,
                'to': end_date
            }
        )
        return response.json().get('data', [])

    def get_next_available_dates(
        self,
        workshop_name: str,
        limit: int = 5
    ) -> List[Dict]:
        """Get next N available dates for a workshop"""
        experiences = self.get_experiences()

        # Find matching workshop
        experience = next(
            (exp for exp in experiences
             if workshop_name.lower() in exp['name'].lower()),
            None
        )

        if not experience:
            return []

        availability = self.get_availability(experience['id'])

        # Filter to available slots and return next N
        available_slots = [
            slot for slot in availability
            if slot['quantity'] > 0
        ]

        return available_slots[:limit]

# Initialize client
xola_client = XolaClient()
```

#### **3. Update Nicole's System Prompt**
Add schedule awareness:
```python
# In api/prompts.py

def get_system_prompt():
    # ... existing code ...

    schedule_guidance = """

When customers ask about workshop availability or schedule:
- Use the get_workshop_schedule() function to fetch real-time data
- Show next 3-5 available dates
- Include day of week, date, and time
- Mention how many spots are left if limited
- Provide direct booking link

Example response:
"The Cutting Board Workshop has these upcoming sessions:
- Saturday, Feb 15 at 10:00 AM (5 spots left)
- Sunday, Feb 16 at 2:00 PM (3 spots left)
- Saturday, Feb 22 at 10:00 AM (8 spots left)

You can book at: [direct booking link]"
"""

    return f"""...existing prompt...{schedule_guidance}"""
```

#### **4. Add Function Calling to Nicole**
```python
# api/nicole.py

async def get_workshop_schedule(workshop_name: str) -> str:
    """Fetch real-time schedule for a workshop"""
    from .xola_integration import xola_client

    try:
        dates = xola_client.get_next_available_dates(workshop_name, limit=5)

        if not dates:
            return f"No upcoming dates found for {workshop_name}. Check woodthumb.com/workshops for updates."

        schedule_text = f"Upcoming {workshop_name} sessions:\n"
        for slot in dates:
            date = datetime.fromisoformat(slot['start'])
            spots = slot['quantity']
            schedule_text += f"- {date.strftime('%A, %B %d at %I:%M %p')} ({spots} spots available)\n"

        return schedule_text
    except Exception as e:
        return "Unable to fetch schedule. Please visit woodthumb.com/workshops for current availability."

# Update Nicole class to support tool use
class Nicole:
    # ... existing code ...

    TOOLS = [
        {
            "name": "get_workshop_schedule",
            "description": "Get real-time availability for a specific workshop",
            "input_schema": {
                "type": "object",
                "properties": {
                    "workshop_name": {
                        "type": "string",
                        "description": "The name of the workshop (e.g., 'Cutting Board', 'Side Table')"
                    }
                },
                "required": ["workshop_name"]
            }
        }
    ]

    async def _generate_response_sync(self, message: str, conversation_history):
        # ... existing code ...

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=messages,
            tools=self.TOOLS  # Enable tool use
        )

        # Handle tool use
        if response.stop_reason == "tool_use":
            tool_use = next(
                block for block in response.content
                if block.type == "tool_use"
            )

            if tool_use.name == "get_workshop_schedule":
                schedule = await get_workshop_schedule(
                    tool_use.input["workshop_name"]
                )

                # Continue conversation with tool result
                messages.append({
                    "role": "assistant",
                    "content": response.content
                })
                messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": schedule
                    }]
                })

                # Get final response
                final_response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1024,
                    system=system_prompt,
                    messages=messages,
                    tools=self.TOOLS
                )

                response_text = final_response.content[0].text
        else:
            response_text = response.content[0].text

        # ... rest of existing code ...
```

---

### **Option B: Manual Schedule Updates (Simpler)**

If Xola API access is not immediately available:

#### **1. Create Schedule Dashboard**
Add to admin dashboard (Settings tab):

```html
<!-- In dashboard/admin.html -->

<div class="card">
  <div class="card-header">
    <h3 class="card-title">Workshop Schedule</h3>
    <p class="card-subtitle">Manually update upcoming workshop dates</p>
  </div>

  <div class="form-group">
    <label class="form-label">Triangle Shelf - Next Dates</label>
    <textarea class="form-textarea" id="triangle-shelf-schedule" rows="3">
Saturday, Feb 15 at 10:00 AM - 5 spots
Sunday, Feb 16 at 2:00 PM - 3 spots
Saturday, Feb 22 at 10:00 AM - 8 spots</textarea>
    <div class="form-help">One date per line. Format: Day, Date at Time - Spots available</div>
  </div>

  <!-- Repeat for other workshops -->

  <button class="btn btn-primary" onclick="saveSchedules()">Update Schedules</button>
</div>
```

#### **2. Store in Config**
```json
// dashboard_config.json
{
  "schedules": {
    "triangle_shelf": [
      {
        "date": "2024-02-15",
        "time": "10:00 AM",
        "day": "Saturday",
        "spots": 5
      }
    ],
    "cutting_board": [
      {
        "date": "2024-02-16",
        "time": "2:00 PM",
        "day": "Sunday",
        "spots": 3
      }
    ]
  }
}
```

#### **3. Include in System Prompt**
```python
def get_system_prompt():
    config = load_dashboard_config()
    schedules = config.get("schedules", {})

    schedule_text = "\n\nUPCOMING WORKSHOP SCHEDULES:\n"
    for workshop, dates in schedules.items():
        schedule_text += f"\n{workshop.replace('_', ' ').title()}:\n"
        for date_info in dates[:3]:  # Show next 3 dates
            schedule_text += f"- {date_info['day']}, {date_info['date']} at {date_info['time']} ({date_info['spots']} spots)\n"

    return f"""...existing prompt...{schedule_text}"""
```

---

## 🎨 Part 2: Improve Chat UI/UX

### **Enhancement 1: Quick Reply Buttons**

Add suggested questions as clickable buttons:

```javascript
// In widget/nicole-widget.js

function addQuickReplies() {
    const quickReplies = [
        "What workshops do you offer?",
        "Show me available dates",
        "How much do workshops cost?",
        "Tell me about team events"
    ];

    const container = document.createElement('div');
    container.className = 'nicole-quick-replies';
    container.innerHTML = quickReplies.map(text =>
        `<button class="nicole-quick-reply-btn" onclick="sendQuickReply('${text}')">${text}</button>`
    ).join('');

    document.getElementById('nicole-messages').appendChild(container);
}

function sendQuickReply(text) {
    document.getElementById('nicole-input').value = text;
    document.getElementById('nicole-send-btn').click();

    // Hide quick replies after use
    document.querySelector('.nicole-quick-replies').remove();
}

// Add CSS for quick replies
```

```css
/* In widget/nicole-widget.css */

.nicole-quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0;
  padding: 0 12px;
}

.nicole-quick-reply-btn {
  background: var(--primary);
  border: 1px solid var(--accent);
  color: var(--accent);
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

.nicole-quick-reply-btn:hover {
  background: var(--accent);
  color: white;
}
```

---

### **Enhancement 2: Workshop Cards in Chat**

Show workshops as interactive cards instead of text:

```javascript
function addWorkshopCard(workshop) {
    const card = document.createElement('div');
    card.className = 'nicole-workshop-card';
    card.innerHTML = `
        <div class="workshop-card-image" style="background: ${workshop.color}"></div>
        <div class="workshop-card-content">
            <h4>${workshop.name}</h4>
            <p class="workshop-price">${workshop.price}</p>
            <p class="workshop-description">${workshop.description}</p>
            ${workshop.nextDate ? `
                <p class="workshop-next-date">
                    <strong>Next available:</strong> ${workshop.nextDate}
                </p>
            ` : ''}
            <a href="${workshop.bookingUrl}" target="_blank" class="workshop-book-btn">
                Book Now
            </a>
        </div>
    `;

    return card;
}
```

```css
.nicole-workshop-card {
  background: var(--primary);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  margin: 12px 0;
  max-width: 300px;
}

.workshop-card-image {
  height: 120px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.workshop-card-content {
  padding: 16px;
}

.workshop-card-content h4 {
  font-size: 1.1rem;
  margin-bottom: 8px;
  color: var(--text);
}

.workshop-price {
  color: var(--accent);
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 8px;
}

.workshop-description {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-bottom: 12px;
}

.workshop-next-date {
  font-size: 0.85rem;
  padding: 8px;
  background: var(--bg-light);
  border-radius: 4px;
  margin-bottom: 12px;
}

.workshop-book-btn {
  display: inline-block;
  background: var(--accent);
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.workshop-book-btn:hover {
  background: #4a8ca3;
  transform: translateY(-1px);
}
```

---

### **Enhancement 3: Better Typing Indicator**

Replace dots with more engaging animation:

```javascript
function showTyping() {
    const typingDiv = document.createElement('div');
    typingDiv.id = 'nicole-typing-indicator';
    typingDiv.className = 'nicole-message';
    typingDiv.innerHTML = `
        <div class="nicole-message-avatar">N</div>
        <div class="nicole-message-content">
            <div class="nicole-typing-enhanced">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <span class="typing-text">Nicole is typing...</span>
        </div>
    `;
    messagesContainer.appendChild(typingDiv);
}
```

```css
.nicole-typing-enhanced {
  display: flex;
  gap: 6px;
  padding: 12px 0;
}

.nicole-typing-enhanced span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--accent);
  animation: bounce 1.4s infinite ease-in-out;
}

.nicole-typing-enhanced span:nth-child(1) {
  animation-delay: -0.32s;
}

.nicole-typing-enhanced span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.typing-text {
  font-size: 0.85rem;
  color: var(--text-muted);
  font-style: italic;
}
```

---

### **Enhancement 4: Message Reactions**

Let customers rate responses:

```javascript
function addMessageReactions(messageDiv) {
    const reactions = document.createElement('div');
    reactions.className = 'message-reactions';
    reactions.innerHTML = `
        <button class="reaction-btn" data-reaction="helpful" title="Helpful">
            👍
        </button>
        <button class="reaction-btn" data-reaction="not-helpful" title="Not helpful">
            👎
        </button>
    `;

    reactions.querySelectorAll('.reaction-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const reaction = btn.dataset.reaction;
            sendFeedback(reaction, messageDiv.dataset.messageId);
            btn.classList.add('selected');
            btn.disabled = true;
        });
    });

    messageDiv.appendChild(reactions);
}
```

---

### **Enhancement 5: Schedule Calendar View**

Show available dates in a mini calendar:

```javascript
function showScheduleCalendar(workshopDates) {
    const calendar = document.createElement('div');
    calendar.className = 'nicole-schedule-calendar';

    const today = new Date();
    const daysToShow = 30;

    let calendarHTML = '<div class="calendar-header">Next 30 Days</div>';
    calendarHTML += '<div class="calendar-grid">';

    for (let i = 0; i < daysToShow; i++) {
        const date = new Date(today);
        date.setDate(today.getDate() + i);

        const hasWorkshop = workshopDates.some(wd =>
            new Date(wd.date).toDateString() === date.toDateString()
        );

        calendarHTML += `
            <div class="calendar-day ${hasWorkshop ? 'has-workshop' : ''}">
                <div class="day-number">${date.getDate()}</div>
                <div class="day-name">${date.toLocaleDateString('en-US', {weekday: 'short'})}</div>
                ${hasWorkshop ? '<div class="workshop-dot"></div>' : ''}
            </div>
        `;
    }

    calendarHTML += '</div>';
    calendar.innerHTML = calendarHTML;

    return calendar;
}
```

---

## 📊 Part 3: Analytics & Improvements

### **Track Common Questions**
```python
# api/analytics.py

from collections import Counter
from datetime import datetime

class ConversationAnalytics:
    def __init__(self):
        self.questions = Counter()
        self.intent_counts = Counter()
        self.failed_questions = []

    def log_question(self, message: str, intent: str, confidence: float):
        self.questions[message.lower()] += 1
        self.intent_counts[intent] += 1

        if confidence < 0.6:
            self.failed_questions.append({
                'message': message,
                'intent': intent,
                'confidence': confidence,
                'timestamp': datetime.now()
            })

    def get_top_questions(self, limit: int = 10):
        return self.questions.most_common(limit)

    def get_questions_needing_improvement(self):
        return self.failed_questions[-20:]  # Last 20 failed
```

---

## 🎯 Implementation Priority

### **Phase 1: Quick Wins (This Week)**
1. ✅ Add quick reply buttons
2. ✅ Improve typing indicator
3. ✅ Add message timestamps
4. ✅ Manual schedule update in dashboard

### **Phase 2: Enhanced Experience (Next Week)**
1. ✅ Workshop cards in chat
2. ✅ Message reactions/feedback
3. ✅ Schedule calendar view
4. ✅ Conversation analytics

### **Phase 3: Full Integration (Week 3-4)**
1. ✅ Xola API integration
2. ✅ Real-time availability
3. ✅ Direct booking from chat
4. ✅ Automated schedule sync

---

## 💰 Cost Considerations

**Xola API:**
- Usually included with Xola subscription
- Check with Wood Thumb's current plan
- May require upgrade for API access

**Additional Claude API Usage:**
- Tool use adds ~$0.001 per request
- Minimal impact on monthly costs
- Still way cheaper than Intercom ($79-128/month)

---

## 🚀 Next Steps

1. **Research Xola API**
   - Contact Wood Thumb owner
   - Get API credentials
   - Review API documentation

2. **Start with Manual Schedules**
   - Add schedule editor to dashboard
   - Owner can update weekly
   - Include in Nicole's knowledge

3. **Implement Quick Wins**
   - Add quick reply buttons
   - Improve typing indicators
   - Better message styling

4. **Test & Iterate**
   - Get owner feedback
   - Track which features customers use most
   - Continuously improve

---

**Want me to start implementing any of these improvements?** Let me know which enhancements you'd like to see first!
