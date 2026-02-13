# Where Is Everything? - Quick Reference

**Visual guide to find all parts of Nicole**

---

## 🌐 URLs - Where to Access Things

### **1. Chat Widget (Customer-Facing)**
```
http://localhost:8000/widget/test.html
```
**What you'll see:**
- A clean white page with "Nicole Widget Test" heading
- Information cards about Wood Thumb
- **LOOK HERE:** Bottom-right corner = circular chat button (black with blue icon)
- Click the button → chat window opens

**If you don't see it:**
- Scroll to the very bottom of the page
- Look in the bottom-right corner (it floats above content)
- The button is ~64px diameter, circular, black background
- Has a chat bubble icon in blue

---

### **2. Admin Dashboard (Owner-Facing)**
```
http://localhost:8000/dashboard/admin.html
```
**What you'll see:**
- Left sidebar with navigation (Overview, Analytics, Settings, etc.)
- Main content area with stats and cards
- Professional black/white/blue design matching Wood Thumb

**Key sections:**
- **Overview** = Homepage with stats
- **Settings** = Where to customize AI, scheduling, events
- **Knowledge Base** = Edit Wood Thumb info
- **Conversations** = View chat history

---

### **3. API Health Check**
```
http://localhost:8000/api/health
```
**What you'll see:**
```json
{
  "status": "healthy",
  "api_key_configured": true,
  "environment": "development"
}
```
If you see this, the server is running correctly!

---

## 🗂️ File Locations

### **Configuration Files:**

**1. API Key & Environment Variables**
```
/Users/nathanielsteinrueck/nicole/.env
```
Contains:
- ANTHROPIC_API_KEY (your Claude API key)
- OWNER_EMAIL
- Thresholds, ports, etc.

**2. Dashboard Settings (Persistent)**
```
/Users/nathanielsteinrueck/nicole/api/dashboard_config.json
```
Contains:
- Assistant identity (name, title, intro)
- Scheduling URLs (workshop, team, shop)
- Event display preferences

**3. Wood Thumb Knowledge Base**
```
/Users/nathanielsteinrueck/nicole/knowledge/woodthumb.md
```
Contains:
- Workshop information
- Pricing
- Policies
- FAQs

---

### **Code Files (Don't Need to Touch):**

```
/Users/nathanielsteinrueck/nicole/
├── api/                    (Backend server code)
│   ├── main.py            (FastAPI app entry point)
│   ├── nicole.py          (Core AI logic)
│   ├── prompts.py         (System prompts)
│   ├── dashboard.py       (Dashboard API endpoints)
│   └── dashboard_config.json (Dashboard settings storage)
│
├── widget/                (Chat widget - customer-facing)
│   ├── nicole-widget.js   (Widget JavaScript)
│   ├── nicole-widget.css  (Widget styling)
│   └── test.html          (Test page for widget)
│
├── dashboard/             (Admin dashboard - owner-facing)
│   └── admin.html         (Full dashboard interface)
│
├── gmail/                 (Gmail integration scripts)
│   ├── Code.gs            (Google Apps Script)
│   └── Config.gs          (Gmail configuration)
│
└── knowledge/             (Content storage)
    └── woodthumb.md       (Workshop info, pricing, etc.)
```

---

## 🎯 Where to Find Features

### **Chat Widget Button Location:**

```
┌─────────────────────────────────────┐
│                                     │
│  Test Page Content                  │
│                                     │
│  [Information Cards]                │
│                                     │
│                                     │
│                              ╭─────╮│
│                              │  💬  ││  ← CHAT BUTTON HERE
│                              ╰─────╯│     (Bottom-right corner)
└─────────────────────────────────────┘
      Browser window bottom-right
```

**Visual cues:**
- Black circular button
- Blue chat bubble icon inside
- Hovers above all content
- Fixed position (stays when you scroll)

**When clicked:**
```
┌─────────────────────────────────────┐
│                                     │
│                      ┌─────────────┐│
│                      │ Nicole      ││
│                      │ AI Assistant││
│                      ├─────────────┤│
│                      │             ││
│                      │ Hi! I'm...  ││  ← CHAT WINDOW
│                      │             ││
│                      │             ││
│                      ├─────────────┤│
│                      │ Type here.. ││
│                      └─────────────┘│
└─────────────────────────────────────┘
```

---

### **Dashboard Navigation:**

```
┌──────────────┬────────────────────────────┐
│              │                            │
│  Nicole      │  Dashboard Overview        │
│  Wood Thumb  │                            │
│ ─────────────┤  [Stats cards]             │
│              │                            │
│ OVERVIEW     │  [System Status]           │
│ ANALYTICS    │                            │
│ ─────────────│  [Recent Conversations]    │
│ KNOWLEDGE    │                            │
│ SETTINGS     │ ← CLICK HERE FOR AI        │
│ TEMPLATES    │    CUSTOMIZATION           │
│ ─────────────│                            │
│ CONVERSATIONS│                            │
│ GMAIL        │                            │
│              │                            │
└──────────────┴────────────────────────────┘
   Sidebar         Main content area
```

**Settings Page Sections (scroll down):**

1. **Confidence Thresholds** (top)
2. **API Configuration**
3. **Widget Settings**
4. **AI Assistant Identity** ← NEW! Change name here
5. **Calendar & Scheduling Integration** ← NEW! Booking URLs
6. **Event Display Settings** ← NEW! Featured workshops

---

## 🔍 How to Test Everything Works

### **Test 1: Server Running**
```bash
curl http://localhost:8000/api/health
```
Should return: `{"status":"healthy",...}`

---

### **Test 2: Chat Widget Visible**
1. Open: http://localhost:8000/widget/test.html
2. Scroll to bottom of page
3. Look bottom-right corner for circular button
4. Button should have chat icon (looks like speech bubble)

---

### **Test 3: Chat Widget Works**
1. Click the circular button
2. Chat window should slide up
3. Should see greeting: "Hi! I'm Nicole, Wood Thumb's AI assistant..."
4. Type: "What workshops do you offer?"
5. Should get response with workshop list and booking link

---

### **Test 4: Dashboard Loads**
1. Open: http://localhost:8000/dashboard/admin.html
2. Should see sidebar on left
3. Should see "Dashboard Overview" at top
4. Should see stats cards (Total Conversations, etc.)

---

### **Test 5: Settings Can Be Changed**
1. In dashboard, click "Settings" in sidebar
2. Scroll down to "AI Assistant Identity"
3. Change name from "Nicole" to "Test"
4. Click "Save Identity Settings"
5. Should see success alert
6. Reload widget test page
7. Open chat - greeting should say "Test" now

---

## 🎨 Visual Elements to Look For

### **Chat Widget Button:**
- **Color:** Black (#000000)
- **Icon color:** Blue (#5b9db5)
- **Size:** 64px × 64px circle
- **Position:** Bottom-right, 24px from edges
- **Hover effect:** Slightly lifts up, border turns blue

### **Chat Window:**
- **Size:** 380px wide × 600px tall
- **Colors:** White background, black text, blue accents
- **Header:** Shows "Nicole" (or custom name) + "AI Assistant"
- **Messages:**
  - Bot messages: Light gray background
  - User messages: Blue background, white text

### **Dashboard:**
- **Sidebar:** White, 250px wide, black text
- **Active nav item:** Light gray background, blue left border
- **Main area:** Light gray background (#f9f9f9)
- **Cards:** White with subtle borders
- **Buttons:** Blue (#5b9db5)

---

## 📱 What You Should See Right Now

If you open these URLs now, here's what should appear:

### **Test Page (http://localhost:8000/widget/test.html):**
```
┌─────────────────────────────────────────┐
│ Nicole Widget Test                      │
│ AI Customer Service for Wood Thumb      │
│                                         │
│ ┌─────────────┐ ┌─────────────┐       │
│ │ 🪵 About    │ │ 💬 Chat     │       │
│ │ Wood Thumb  │ │ with Nicole │       │
│ └─────────────┘ └─────────────┘       │
│                                         │
│ ┌─────────────┐                        │
│ │ ⚙️ Test     │                        │
│ │ the Widget  │                        │
│ └─────────────┘                        │
│                                         │
│ [For Developers section]                │
│                                  [💬]   │← Chat button
└─────────────────────────────────────────┘
```

### **Dashboard (http://localhost:8000/dashboard/admin.html):**
```
┌────────┬─────────────────────────────────┐
│ Nicole │ Dashboard Overview              │
│ ─────  │                                 │
│        │ [247] [156] [87%] [2.3s]       │
│Overview│  Conversations Stats            │
│Analytic│                                 │
│        │ System Status                   │
│Knowledg│ ✓ Chat Widget Active            │
│Settings│ ✓ Gmail Integration Active      │
│Template│ ✓ API Server Healthy            │
│        │                                 │
│Convers.│ Recent Conversations            │
│Gmail   │ [List of recent chats]          │
└────────┴─────────────────────────────────┘
```

---

## ❓ "I Still Can't Find the Chat Widget!"

**Double-check:**

1. ✅ Server is running: `curl http://localhost:8000/api/health`
2. ✅ Page fully loaded: Wait for page to finish loading
3. ✅ Scrolled to bottom: Chat button is in bottom-right corner
4. ✅ Browser zoom normal: Not zoomed in/out too much
5. ✅ JavaScript enabled: Check browser console for errors
6. ✅ Right page: http://localhost:8000/widget/test.html (not dashboard)

**Try:**
- Open browser dev tools (F12 or Cmd+Option+I)
- Look for errors in Console tab
- Check Elements tab for `nicole-widget-button` element
- Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

---

## 📞 Quick Reference Links

**All URLs at a glance:**
```
Dashboard:      http://localhost:8000/dashboard/admin.html
Chat Widget:    http://localhost:8000/widget/test.html
Health Check:   http://localhost:8000/api/health
API Root:       http://localhost:8000/
API Docs:       http://localhost:8000/docs (FastAPI auto docs)
```

**All important files:**
```
Settings:       /Users/nathanielsteinrueck/nicole/api/dashboard_config.json
API Key:        /Users/nathanielsteinrueck/nicole/.env
Knowledge:      /Users/nathanielsteinrueck/nicole/knowledge/woodthumb.md
Server Logs:    /tmp/nicole_server.log
```

---

**Still can't find something? Check `SETUP_FOR_OWNER.md` or `DASHBOARD_FEATURES.md`**
