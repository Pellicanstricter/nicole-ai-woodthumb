# Nicole Admin Dashboard - Complete Feature Guide

**Enhanced with Calendar Integration & AI Customization**

---

## 🎉 What's New

The admin dashboard now includes:
1. ✅ **Customizable AI Assistant Identity** - Change the assistant's name, title, and intro message
2. ✅ **Calendar & Scheduling Integration** - Connect booking systems (Acuity, Calendly, Google Calendar)
3. ✅ **Event Display Settings** - Control how Nicole presents workshops and events
4. ✅ **Dynamic Configuration** - All settings persist and apply immediately to chat responses

---

## 🚀 Dashboard Access

**URL:** http://localhost:8000/dashboard/admin.html

**Navigation Sections:**
- **Overview** - Dashboard stats and recent conversations
- **Analytics** - Performance metrics and question categories
- **Knowledge Base** - Edit Wood Thumb information
- **Settings** - Configure AI behavior, identity, and scheduling
- **Templates** - Customize greeting and email signatures
- **Conversations** - View chat and email history
- **Gmail Integration** - Monitor email processing status

---

## 🎨 AI Assistant Identity Customization

**Location:** Settings → AI Assistant Identity

### What You Can Customize:

1. **Assistant Name**
   - Default: "Nicole"
   - Can be changed to any name you want
   - Example: "Woody", "Alex", "Taylor"

2. **Display Title**
   - Default: "AI Assistant"
   - Examples: "Virtual Helper", "Customer Service Bot", "Workshop Guide"

3. **Introduction Message**
   - The first message customers see in the chat widget
   - Default: "Hi! I'm Nicole, Wood Thumb's AI assistant..."
   - Customize to match your brand voice

### How It Works:

When you save these settings:
- ✅ Settings are saved to `api/dashboard_config.json`
- ✅ Nicole's system prompt is regenerated with new identity
- ✅ Chat widget displays new name and greeting
- ✅ All responses use the updated identity

**Example:**
```
Change name to "Woody"
Change title to "Woodworking Guide"
Intro: "Hey there! I'm Woody, your woodworking guide at Wood Thumb..."
```

Result: Nicole becomes "Woody" with a new personality!

---

## 📅 Calendar & Scheduling Integration

**Location:** Settings → Calendar & Scheduling Integration

### Supported Platforms:
- ✅ Acuity Scheduling (default for Wood Thumb)
- ✅ Calendly
- ✅ Google Calendar
- ✅ Custom Booking Page

### What You Can Configure:

1. **Workshop Booking URL**
   - Primary link for workshop bookings
   - Example: `https://woodthumb.com/workshops`
   - Nicole will share this when customers ask about workshops

2. **Team Event Booking URL** (optional)
   - Link for team building and group events
   - Example: `https://woodthumb.com/team-events`

3. **Shop Time Booking URL** (optional)
   - Link for shop time reservations
   - Example: `https://woodthumb.com/shop-time`

4. **Show Available Times**
   - When enabled: Nicole encourages customers to check the booking link for current availability
   - When disabled: Nicole just provides the link without mentioning availability

5. **Auto-suggest Booking**
   - When enabled: Nicole proactively shares booking links when relevant
   - When disabled: Only shares links when explicitly asked

### How It Works:

When you update these settings:
- ✅ Booking URLs are injected into Nicole's system prompt
- ✅ Nicole automatically includes relevant links in responses
- ✅ Customers can click directly to book

**Example Conversation:**

```
Customer: "What workshops do you offer?"

Nicole: "Hi! We offer several beginner-friendly workshops:
- Cutting Board Workshop ($75, 2 hours)
- Side Table Workshop ($120, 3 hours)
- Spoon Carving Workshop ($85, 2.5 hours)

You can see our current schedule and book directly at:
https://woodthumb.com/workshops

Which project sounds interesting to you?"
```

---

## 🎪 Event Display Settings

**Location:** Settings → Event Display Settings

### What You Can Control:

1. **Featured Events**
   - List of workshops to highlight when customers ask
   - Enter one per line
   - Example:
     ```
     Cutting Board Workshop
     Side Table Workshop
     Spoon Carving Workshop
     ```

2. **Show Pricing**
   - When enabled: Nicole always includes pricing information
   - When disabled: Only mentions pricing when specifically asked

3. **Event Details Level**
   - **Brief**: Name and link only
   - **Moderate** (default): Name, duration, and price
   - **Detailed**: Full description with what they'll make and learn

### How It Works:

These settings control Nicole's verbosity and focus:

**Brief Mode:**
```
"We offer Cutting Board, Side Table, and Spoon Carving workshops.
Check availability at woodthumb.com/workshops"
```

**Moderate Mode:**
```
"We offer:
- Cutting Board Workshop ($75, 2 hours)
- Side Table Workshop ($120, 3 hours)
- Spoon Carving Workshop ($85, 2.5 hours)

Book at woodthumb.com/workshops"
```

**Detailed Mode:**
```
"We offer beginner-friendly workshops where you'll learn fundamental
woodworking skills and leave with a finished project:

- Cutting Board Workshop ($75, 2 hours): Learn joinery and sanding
  techniques while creating a beautiful hardwood cutting board
- Side Table Workshop ($120, 3 hours): Build a functional side table
  using basic carpentry and finishing methods
..."
```

---

## 💾 How Settings Are Stored

All dashboard configurations are saved to:
```
/Users/nathanielsteinrueck/nicole/api/dashboard_config.json
```

**Current Structure:**
```json
{
  "assistant_identity": {
    "assistant_name": "Nicole",
    "assistant_title": "AI Assistant",
    "intro_message": "Hi! I'm Nicole..."
  },
  "scheduling": {
    "platform": "acuity",
    "workshop_booking_url": "https://woodthumb.com/workshops",
    "team_booking_url": "https://woodthumb.com/team-events",
    "shop_booking_url": "https://woodthumb.com/shop-time",
    "show_available_times": true,
    "auto_suggest_booking": true
  },
  "event_display": {
    "featured_events": [
      "Cutting Board Workshop",
      "Side Table Workshop",
      "Spoon Carving Workshop"
    ],
    "show_pricing": true,
    "detail_level": "moderate"
  }
}
```

---

## 🔄 How Changes Take Effect

### Immediate Effect (No Restart Needed):
- ✅ AI Assistant Identity changes
- ✅ Scheduling URL updates
- ✅ Event display preferences
- ✅ Knowledge base edits

Nicole's system prompt is regenerated on each request, so changes apply immediately to new conversations.

### Requires Page Reload:
- Chat widget UI updates (if you change the assistant name)
- Dashboard statistics refresh

---

## 📋 Complete Settings Workflow Example

### Scenario: Wood Thumb wants to rebrand the assistant as "Woody"

**Step 1: Open Dashboard**
- Navigate to http://localhost:8000/dashboard/admin.html
- Click "Settings" in sidebar

**Step 2: Update AI Identity**
- Scroll to "AI Assistant Identity" card
- Change name from "Nicole" to "Woody"
- Change title to "Woodworking Guide"
- Update intro message:
  ```
  Hey there! I'm Woody, your woodworking guide at Wood Thumb.
  I'm here to help you find the perfect workshop or project.
  What brings you to our shop today?
  ```
- Click "Save Identity Settings"
- ✅ Confirmation: "Assistant identity saved!"

**Step 3: Update Scheduling**
- Scroll to "Calendar & Scheduling Integration"
- Verify workshop URL: `https://woodthumb.com/workshops`
- Add team event URL: `https://woodthumb.com/team-events`
- Enable "Auto-suggest Booking"
- Click "Save Scheduling Settings"
- ✅ Confirmation: "Scheduling settings saved!"

**Step 4: Configure Event Display**
- Scroll to "Event Display Settings"
- Update featured events:
  ```
  Cutting Board Workshop
  Side Table Workshop
  Spoon Carving Workshop
  Plant Stand Workshop
  ```
- Enable "Show Pricing"
- Select detail level: "Moderate"
- Click "Save Event Settings"
- ✅ Confirmation: "Event settings saved!"

**Step 5: Test the Changes**
- Open chat widget: http://localhost:8000/widget/test.html
- See new greeting from "Woody"
- Ask: "What workshops do you offer?"
- Verify:
  - ✅ Uses name "Woody"
  - ✅ Shows featured workshops
  - ✅ Includes pricing
  - ✅ Provides booking link

---

## 🧪 Testing Recommendations

### Test 1: Identity Change
```
1. Change assistant name to "Alex"
2. Update intro message
3. Save settings
4. Open widget test page
5. Verify greeting shows "Alex"
6. Ask a question - verify response uses "Alex"
```

### Test 2: Booking Link Integration
```
1. Set workshop URL to your actual Acuity link
2. Enable "Auto-suggest Booking"
3. Save settings
4. Ask: "How do I book a workshop?"
5. Verify Nicole provides correct URL
6. Ask: "What workshops do you have?"
7. Verify link is included proactively
```

### Test 3: Event Detail Levels
```
1. Set detail level to "Brief"
2. Save and ask about workshops
3. Note response length
4. Change to "Detailed"
5. Save and ask same question
6. Compare responses
```

---

## 📊 Dashboard API Endpoints

All settings are accessible via REST API:

### Assistant Identity
```bash
# Get current identity
GET /api/dashboard/settings/identity

# Update identity
PUT /api/dashboard/settings/identity
{
  "assistant_name": "Woody",
  "assistant_title": "Woodworking Guide",
  "intro_message": "Hey there! I'm Woody..."
}
```

### Scheduling
```bash
# Get scheduling settings
GET /api/dashboard/settings/scheduling

# Update scheduling
PUT /api/dashboard/settings/scheduling
{
  "platform": "acuity",
  "workshop_booking_url": "https://...",
  "team_booking_url": "https://...",
  "shop_booking_url": "https://...",
  "show_available_times": true,
  "auto_suggest_booking": true
}
```

### Event Display
```bash
# Get event settings
GET /api/dashboard/settings/events

# Update events
PUT /api/dashboard/settings/events
{
  "featured_events": ["Workshop 1", "Workshop 2"],
  "show_pricing": true,
  "detail_level": "moderate"
}
```

---

## 🎯 Use Cases

### 1. Seasonal Workshop Focus
Change featured events based on season:
- **Spring**: Plant Stand, Garden Planter
- **Fall**: Cutting Board, Cheese Board
- **Holiday**: Gift projects, ornaments

### 2. Different Assistant Personas
Test different approaches:
- **Friendly**: "Nicole" - casual and warm
- **Professional**: "Alex" - polished and formal
- **Playful**: "Woody" - fun and engaging

### 3. Promotional Campaigns
Temporarily adjust settings:
- Highlight specific workshops with deals
- Change detail level to "Detailed" for new offerings
- Update intro message with seasonal greeting

### 4. A/B Testing
Test what works best:
- Auto-suggest booking ON vs OFF
- Brief vs Detailed event descriptions
- Different assistant names and personalities

---

## 🔐 Security & Permissions

**Who Can Access:**
- Currently: Anyone with URL access (localhost only)
- Production: Add authentication (OAuth, API keys, password)

**Recommendation for Production:**
1. Add login system
2. Restrict to Wood Thumb staff only
3. Log all configuration changes
4. Enable change rollback

---

## 📈 Future Enhancements

### Planned Features:
- [ ] **Analytics**: Track which events get asked about most
- [ ] **A/B Testing**: Split traffic between different settings
- [ ] **Schedule Sync**: Pull event calendar directly from Acuity API
- [ ] **Real-time Availability**: Show actual workshop availability
- [ ] **Multi-language**: Support for Spanish or other languages
- [ ] **Custom Workflows**: Different responses based on time/day
- [ ] **Conversation Insights**: What questions Nicole struggles with

---

## 🆘 Troubleshooting

### Problem: Changes not showing in chat widget

**Solution:**
1. Hard refresh the test page (Cmd+Shift+R)
2. Clear browser cache
3. Verify settings saved (check dashboard_config.json)
4. Check server logs: `tail -f /tmp/nicole_server.log`

### Problem: Booking links not appearing in responses

**Solution:**
1. Verify URLs saved in dashboard
2. Check "Auto-suggest Booking" is enabled
3. Ask questions that would trigger booking (e.g., "How do I book?")
4. Check system prompt in API logs

### Problem: Assistant name not changing

**Solution:**
1. Verify saved in dashboard
2. Check dashboard_config.json file
3. Restart server if needed: `pkill -f uvicorn && uvicorn api.main:app --reload`

---

## ✅ What Was Built

### New Dashboard Sections:
1. ✅ AI Assistant Identity card in Settings
2. ✅ Calendar & Scheduling Integration card in Settings
3. ✅ Event Display Settings card in Settings

### New API Endpoints:
1. ✅ `/api/dashboard/settings/identity` (GET, PUT)
2. ✅ `/api/dashboard/settings/scheduling` (GET, PUT)
3. ✅ `/api/dashboard/settings/events` (GET, PUT)

### Backend Changes:
1. ✅ Created `dashboard_config.json` for persistent storage
2. ✅ Updated `prompts.py` with dynamic `get_system_prompt()` function
3. ✅ Modified `nicole.py` to use fresh system prompt on each request
4. ✅ Added config loading/saving functions in `dashboard.py`

### Integration Points:
1. ✅ Dashboard UI → API endpoints → Config file → System prompt → Chat responses
2. ✅ Settings persist across server restarts
3. ✅ Changes apply immediately to new conversations

---

## 🎓 For Wood Thumb Owner

**What This Means:**

You can now customize Nicole's personality, booking links, and how she presents your workshops - all from the admin dashboard, without touching any code!

**Quick Wins:**
1. Update workshop schedule/URLs when they change
2. Test different assistant names to see what customers prefer
3. Adjust event detail level based on feedback
4. Enable/disable proactive booking suggestions

**No Technical Skills Needed:**
- ✅ Just fill out forms in the dashboard
- ✅ Click "Save"
- ✅ Test in the chat widget
- ✅ That's it!

---

**Dashboard is now live and ready to use! 🚀**

Access it at: http://localhost:8000/dashboard/admin.html
