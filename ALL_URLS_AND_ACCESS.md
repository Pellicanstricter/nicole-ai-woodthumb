# All URLs and Access Points

**Complete reference for accessing Nicole system**

---

## 🎯 Main Access URLs

### **1. Admin Dashboard (Owner Control Panel)**
```
http://localhost:8000/dashboard/admin.html
```
**What it is:** Full admin interface where owner can:
- View stats and analytics
- Edit knowledge base (workshops, pricing, policies)
- Customize AI assistant (name, greeting, personality)
- Configure booking URLs and calendar integration
- Monitor conversations
- Manage Gmail integration
- Adjust confidence thresholds

**Who uses it:** Wood Thumb owner/staff

---

### **2. Chat Widget Test Page**
```
http://localhost:8000/widget/test.html
```
**What it is:** Demo page showing the chat widget
- Circular chat button in bottom-right corner
- Click to open chat window
- Test Nicole's responses
- See customer experience

**Who uses it:** For testing before embedding on actual website

---

### **3. API Health Check**
```
http://localhost:8000/api/health
```
**What it is:** Server status endpoint
- Returns JSON with health status
- Confirms API key configured
- Shows environment (development/production)

**Response:**
```json
{
  "status": "healthy",
  "api_key_configured": true,
  "environment": "development"
}
```

---

### **4. API Root**
```
http://localhost:8000/
```
**What it is:** API information endpoint
**Response:**
```json
{
  "app": "Nicole",
  "version": "1.0.0",
  "status": "running",
  "environment": "development"
}
```

---

### **5. API Documentation (Auto-generated)**
```
http://localhost:8000/docs
```
**What it is:** FastAPI's automatic interactive API documentation
- See all available endpoints
- Test API calls directly in browser
- View request/response schemas

---

## 📂 File Locations

### **Configuration Files:**

#### **1. Environment Variables (.env)**
```
/Users/nathanielsteinrueck/nicole/.env
```
**Contains:**
- Anthropic API key
- Owner email
- Confidence thresholds
- Server port settings

**Edit to:** Change API key, thresholds, environment

---

#### **2. Dashboard Settings (JSON)**
```
/Users/nathanielsteinrueck/nicole/api/dashboard_config.json
```
**Contains:**
- AI assistant identity (name, title, intro message)
- Scheduling settings (booking URLs, platform)
- Event display preferences (featured workshops, pricing)

**Managed through:** Dashboard (Settings tab)

---

#### **3. Knowledge Base (Markdown)**
```
/Users/nathanielsteinrueck/nicole/knowledge/woodthumb.md
```
**Contains:**
- All Wood Thumb workshop information
- Pricing, descriptions, policies
- Contact information
- FAQs

**Managed through:** Dashboard (Knowledge Base tab)

---

### **Server Logs:**
```
/tmp/nicole_server.log
```
**View with:** `tail -f /tmp/nicole_server.log`

---

## 🔗 Wood Thumb Website URLs

### **Public Facing:**
```
https://woodthumb.com - Main website
https://woodthumb.com/workshops - Workshop booking page
```

### **Contact:**
```
Email: chris@woodthumb.com
Phone: (415) 295-5047
Instagram: @woodthumb
```

### **Location:**
```
968 Mission St.
San Francisco, CA 94103
(SOMA district)
```

---

## 🛠️ Development Commands

### **Start Server:**
```bash
cd /Users/nathanielsteinrueck/nicole
uvicorn api.main:app --reload
```

### **Stop Server:**
```bash
pkill -f "uvicorn api.main:app"
```

### **Check Server Status:**
```bash
curl http://localhost:8000/api/health
```

### **View Logs:**
```bash
tail -f /tmp/nicole_server.log
```

---

## 🧪 Testing URLs

### **Test Chat Endpoint:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What workshops do you offer?",
    "conversation_history": [],
    "stream": false
  }'
```

### **Test Email Endpoint:**
```bash
curl -X POST http://localhost:8000/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "from_email": "test@example.com",
    "subject": "Workshop Question",
    "body": "What workshops do you have?",
    "thread_id": "test-123"
  }'
```

### **Get Knowledge Base:**
```bash
curl http://localhost:8000/api/dashboard/knowledge
```

---

## 📱 Access from Different Devices

### **On Same Computer:**
```
Dashboard: http://localhost:8000/dashboard/admin.html
Widget: http://localhost:8000/widget/test.html
```

### **On Local Network (Phone/Tablet):**
Find your computer's IP address:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Then use:
```
Dashboard: http://[YOUR-IP]:8000/dashboard/admin.html
Widget: http://[YOUR-IP]:8000/widget/test.html
```
Example: `http://192.168.1.100:8000/dashboard/admin.html`

---

## 🌐 Production URLs (After Deployment)

### **When Deployed to Railway/Fly.io:**
```
Dashboard: https://your-domain.com/dashboard/admin.html
Chat Widget: Embed on woodthumb.com
API: https://your-domain.com/api
Health: https://your-domain.com/api/health
```

### **Embed Widget on Actual Website:**
Add to Squarespace footer:
```html
<link rel="stylesheet" href="https://your-domain.com/widget/nicole-widget.css">
<script>
  window.NICOLE_API_URL = 'https://your-domain.com/api';
</script>
<script src="https://your-domain.com/widget/nicole-widget.js"></script>
```

---

## 🔐 Authentication

### **Current (Development):**
- ❌ No password protection
- ✅ Only accessible on localhost

### **Production (Recommended):**
- ✅ Add password to dashboard
- ✅ Restrict to Wood Thumb staff only
- ✅ Use HTTPS (SSL certificate)
- ✅ Environment variables for secrets

---

## 📊 Dashboard Sections (Navigation)

### **In the Left Sidebar:**

1. **Overview** - `/dashboard/admin.html#overview`
   - Default landing page
   - Stats, system status, recent conversations

2. **Analytics** - `/dashboard/admin.html#analytics`
   - Question categories
   - Performance metrics
   - Confidence distribution

3. **Knowledge Base** - `/dashboard/admin.html#knowledge`
   - Edit Wood Thumb information
   - Update workshops, pricing, policies

4. **Settings** - `/dashboard/admin.html#settings`
   - AI Assistant Identity
   - Calendar & Scheduling Integration
   - Event Display Settings
   - Confidence Thresholds
   - API Configuration

5. **Templates** - `/dashboard/admin.html#templates`
   - Chat widget greeting
   - Email signature
   - Brand voice guidelines

6. **Conversations** - `/dashboard/admin.html#conversations`
   - View chat and email history
   - Search and filter conversations

7. **Gmail Integration** - `/dashboard/admin.html#gmail`
   - Connection status
   - Email statistics
   - Setup instructions

---

## 🎯 Quick Reference Card

**Copy this for the owner:**

```
┌─────────────────────────────────────────────┐
│  NICOLE - WOOD THUMB AI ASSISTANT          │
├─────────────────────────────────────────────┤
│  📊 DASHBOARD                               │
│  http://localhost:8000/dashboard/admin.html│
│  (Owner control panel)                      │
├─────────────────────────────────────────────┤
│  💬 CHAT WIDGET TEST                        │
│  http://localhost:8000/widget/test.html    │
│  (Preview customer experience)              │
├─────────────────────────────────────────────┤
│  🏥 HEALTH CHECK                            │
│  http://localhost:8000/api/health          │
│  (Verify server running)                    │
├─────────────────────────────────────────────┤
│  📧 SUPPORT                                 │
│  chris@woodthumb.com                        │
│  (415) 295-5047                            │
└─────────────────────────────────────────────┘
```

---

## ✅ How to Access Everything Right Now

**Open these 3 tabs:**

**Tab 1 - Dashboard:**
```
open http://localhost:8000/dashboard/admin.html
```

**Tab 2 - Chat Widget:**
```
open http://localhost:8000/widget/test.html
```

**Tab 3 - API Docs:**
```
open http://localhost:8000/docs
```

---

**All access points documented! Share this file with the Wood Thumb owner.** 📋
