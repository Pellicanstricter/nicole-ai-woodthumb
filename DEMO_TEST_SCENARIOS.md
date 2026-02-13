# Nicole Demo Test Scenarios

Test cases to verify Nicole works correctly with steinrueckn@gmail.com

## Chat Widget Test Scenarios

### Scenario 1: Basic Workshop Inquiry
**User Input:** "What workshops do you offer?"

**Expected Response:**
- Lists workshop types (cutting board, side table, spoon carving, etc.)
- Mentions beginner-friendly
- Includes booking link
- Warm, helpful tone

**Pass Criteria:**
- [ ] Response is relevant
- [ ] Includes workshop examples
- [ ] Provides booking link
- [ ] Response time < 3 seconds

---

### Scenario 2: Pricing Question
**User Input:** "How much does shop time cost?"

**Expected Response:**
- States $30-40 per hour
- Mentions membership affects pricing
- Explains what's included
- Suggests booking process

**Pass Criteria:**
- [ ] Correct pricing range
- [ ] Explains membership difference
- [ ] Helpful additional context

---

### Scenario 3: Team Event Inquiry
**User Input:** "We want to do a team building event for 12 people. What do you recommend?"

**Expected Response:**
- Acknowledges team size (12 people)
- Suggests appropriate projects
- Mentions $85-120/person range
- Offers to collect more details or connect with owner

**Pass Criteria:**
- [ ] Personalizes response to group size
- [ ] Provides pricing estimate
- [ ] Offers next steps

---

### Scenario 4: Multi-Turn Conversation
**Turn 1:** "I'm interested in woodworking"
**Expected:** Welcoming response, asks how they can help

**Turn 2:** "I've never done it before"
**Expected:** Reassures beginner-friendly, suggests workshops

**Turn 3:** "What's the easiest project to start with?"
**Expected:** Recommends specific beginner workshops

**Pass Criteria:**
- [ ] Maintains conversation context
- [ ] Each response builds on previous
- [ ] Natural conversation flow

---

### Scenario 5: Booking Assistance
**User Input:** "How do I book a cutting board workshop?"

**Expected Response:**
- Direct link to booking page
- Brief explanation of process
- Mentions what's included
- Encouraging tone

**Pass Criteria:**
- [ ] Includes booking link
- [ ] Clear instructions
- [ ] Sets expectations

---

### Scenario 6: Location/Hours
**User Input:** "Where are you located and what are your hours?"

**Expected Response:**
- Oakland, California location
- Explains hours vary by workshop schedule
- Directs to website or suggests contacting
- Mentions parking info

**Pass Criteria:**
- [ ] Correct location
- [ ] Explains variable hours
- [ ] Helpful directions

---

### Scenario 7: Custom Work Request
**User Input:** "Can you make me a custom bookshelf?"

**Expected Response:**
- Confirms custom work is available
- Explains consultation process
- Mentions timeline (2-6 weeks)
- Pricing range ($500-$3,000+)
- Offers to collect details

**Pass Criteria:**
- [ ] Confirms capability
- [ ] Sets timeline expectations
- [ ] Mentions pricing range
- [ ] Initiates intake process

---

### Scenario 8: Complex/Out of Scope
**User Input:** "Do you teach welding classes?"

**Expected Response:**
- Politely clarifies focus on woodworking
- Doesn't fabricate false offerings
- Suggests contacting owner if they have questions
- Remains helpful

**Pass Criteria:**
- [ ] Doesn't make up information
- [ ] Stays on-brand
- [ ] Offers graceful response

---

## Email Test Scenarios (API Testing)

### High Confidence Scenario (Should Auto-Send)

**From:** test@example.com
**Subject:** "Workshop Hours"
**Body:** "Hi, what are your workshop hours? Thanks"

**Expected:**
- Intent: `policy_question` or `general_info`
- Confidence: > 0.85
- Routing: `auto_send`
- Response: Clear answer about hours

**Test Command:**
```bash
curl -X POST http://localhost:8000/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "from_email": "test@example.com",
    "subject": "Workshop Hours",
    "body": "Hi, what are your workshop hours? Thanks",
    "thread_id": "test-high-conf"
  }'
```

---

### Medium Confidence Scenario (Should Draft)

**From:** corporate@business.com
**Subject:** "Team Event Inquiry"
**Body:** "We're interested in a team event for 20 people. Can you share more details about your offerings and pricing? We're flexible on dates."

**Expected:**
- Intent: `team_event_inquiry`
- Confidence: 0.60 - 0.85
- Routing: `draft`
- Response: Professional, detailed team event info

**Test Command:**
```bash
curl -X POST http://localhost:8000/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "from_email": "corporate@business.com",
    "subject": "Team Event Inquiry",
    "body": "We are interested in a team event for 20 people. Can you share more details about your offerings and pricing? We are flexible on dates.",
    "thread_id": "test-med-conf"
  }'
```

---

### Low Confidence Scenario (Should Flag)

**From:** artist@creative.com
**Subject:** "Unusual Partnership Proposal"
**Body:** "I'm an installation artist working on a piece about industrial nostalgia. I'm looking for a space to collaborate on a deconstructed furniture installation. Would you be interested in a non-traditional partnership?"

**Expected:**
- Intent: `other` or `custom_work_inquiry`
- Confidence: < 0.60
- Routing: `flag`
- Response: Polite but flagged for owner review

**Test Command:**
```bash
curl -X POST http://localhost:8000/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "from_email": "artist@creative.com",
    "subject": "Unusual Partnership Proposal",
    "body": "I am an installation artist working on a piece about industrial nostalgia. I am looking for a space to collaborate on a deconstructed furniture installation. Would you be interested in a non-traditional partnership?",
    "thread_id": "test-low-conf"
  }'
```

---

### Pricing Inquiry (High Confidence)

**From:** customer@gmail.com
**Subject:** "Shop Time Cost"
**Body:** "Hi! How much do you charge for shop time? Thanks!"

**Expected:**
- Intent: `shop_time_inquiry`
- Confidence: > 0.85
- Routing: `auto_send`
- Response: Clear pricing with details

**Test Command:**
```bash
curl -X POST http://localhost:8000/api/email \
  -H "Content-Type: application/json" \
  -d '{
    "from_email": "customer@gmail.com",
    "subject": "Shop Time Cost",
    "body": "Hi! How much do you charge for shop time? Thanks!",
    "thread_id": "test-pricing"
  }'
```

---

## Widget UX/UI Tests

### Visual Tests
- [ ] Chat button appears in bottom-right
- [ ] Button has wood thumb icon/emoji (🪵)
- [ ] Dark theme with brown accent (#8b7355)
- [ ] Widget opens smoothly (no jank)
- [ ] Header shows "Nicole" and "AI Assistant"
- [ ] Messages have proper spacing
- [ ] User messages aligned right (brown background)
- [ ] Bot messages aligned left (dark background)
- [ ] Scrollbar appears when needed
- [ ] Close button works

### Interaction Tests
- [ ] Click to open widget
- [ ] Click to close widget
- [ ] Type in input field
- [ ] Send message with button
- [ ] Send message with Enter key
- [ ] Shift+Enter creates new line
- [ ] Input auto-resizes with content
- [ ] Can't send empty messages
- [ ] Typing indicator appears while waiting
- [ ] Messages stream in real-time

### Mobile Responsive Tests
- [ ] Widget adapts to mobile screen
- [ ] Full screen on mobile
- [ ] Input stays visible (keyboard doesn't hide it)
- [ ] Scrolling works smoothly
- [ ] Touch interactions work

---

## Performance Tests

### Response Time
- [ ] Health check: < 100ms
- [ ] Simple chat query: < 3 seconds
- [ ] Complex chat query: < 5 seconds
- [ ] Email processing: < 5 seconds

### Stress Test (Optional)
Send 10 messages rapidly:
```bash
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"Test message $i\", \"stream\": false}" &
done
wait
```

Expected: All should succeed, no crashes

---

## Error Handling Tests

### Test 1: Invalid API Key
1. Set wrong API key in .env
2. Restart server
3. Try to send chat message

**Expected:** Graceful error message, not a crash

### Test 2: Network Interruption
1. Disconnect from internet
2. Try to send message

**Expected:** Timeout message, recovers when reconnected

### Test 3: Malformed Request
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{invalid json}'
```

**Expected:** 400 Bad Request with error message

---

## Success Criteria Summary

Nicole passes demo testing if:

### Functionality
✅ All API endpoints respond correctly
✅ Chat widget loads and displays properly
✅ Messages send and receive successfully
✅ Streaming works in real-time
✅ Intent classification is accurate (>80%)
✅ Confidence routing makes sense

### Quality
✅ Responses are relevant and helpful
✅ Brand voice is consistent (warm, casual, knowledgeable)
✅ No fabricated information
✅ Graceful error handling

### Performance
✅ Response time < 3 seconds for simple queries
✅ No crashes or freezes
✅ Smooth UX in widget

### Design
✅ Widget is visually appealing
✅ Theme matches Wood Thumb aesthetic
✅ Mobile responsive
✅ Accessible

---

## Recording Test Results

For each test scenario, record:
- ✅ Pass / ❌ Fail
- Response time
- Response quality (1-5 stars)
- Notes/observations

Example:
```
Scenario 1: Basic Workshop Inquiry
Status: ✅ Pass
Response Time: 2.3s
Quality: ⭐⭐⭐⭐⭐
Notes: Excellent response, included all workshop types and booking link
```

---

## Next Steps After Successful Demo

1. ✅ Update knowledge base with accurate Wood Thumb details
2. ✅ Deploy to production (Railway/Fly.io)
3. ✅ Setup Gmail integration with real email
4. ✅ Add widget to Squarespace site
5. ✅ Monitor first week of real usage
6. ✅ Adjust confidence thresholds based on feedback

---

**Ready to test!** Start with chat widget tests, then move to email API tests.
