# Nicole Conversation Improvements - Complete

## Problem: Overwhelming Responses

### Before:
```
User: "What team events do you offer?"

Nicole: "For team events accommodating groups up to 64 people:
**Popular Options:** -
**Cutting Board/Magnetic Knife Rack** - $85/person, up to 64 people -
**Pinewood Racer Derby** - $95/person, up to 64 people (competitive team building) -
**Picture Frame** - $148/person, up to 18 people (smaller groups)
**Book directly:** https://woodthumb.as.me/schedule/73e6f342
For planning, email nicole@woodthumb.com with your group size and preferred dates."
```

**Issues:**
- Too much information at once
- Prices shown when not asked
- Links pasted in text (hard to click on mobile)
- Email included unnecessarily
- Bold markdown (**) showing in text
- Poor formatting

---

## Solution: Clean, Guided Conversation

### After:
```
User: "What team events do you offer?"

Nicole: "We have 6 team building options: Cutting Board, Bottle Opener,
        Pinewood Derby, Triangle Shelf, Picture Frame, Virtual Workshop.
        Which one interests you?"

[See Prices] [Book Team Event]  ← Action chips appear below
```

Then:
```
User: "How much for cutting board?"

Nicole: "Cutting Board is $85/person with $850 minimum. Takes 3 hours."

[Book Now]  ← Opens Acuity booking page
```

---

## Key Improvements

### 1. Names Only in Lists (No Prices)
**Rule:** When listing options, show NAMES ONLY

✅ **Good:** "We have 6 team options: Cutting Board, Bottle Opener, Derby..."
❌ **Bad:** "Cutting Board ($85/person), Bottle Opener ($85/person)..."

### 2. Prices Only When Asked
**Rule:** Give pricing ONLY when specifically asked

```
Q: "What workshops do you offer?"
A: "5 beginner workshops: Triangle Shelf, Cutting Board, Deco Shelf,
    Picture Frame, Wedge Table. Which one?"

Q: "How much for triangle shelf?"
A: "Triangle Shelf is $94. Takes 2 hours."
```

### 3. No Links in Text
**Rule:** Links appear as chips below message, not pasted in text

❌ **Bad:** "Book here: https://woodthumb.as.me/schedule/..."
✅ **Good:** "Cutting Board is $85/person. Ready to book?"
            [Book Now] ← chip below

### 4. No Email Unless Asked
**Rule:** Don't include contact info unless asked "how do I contact you"

❌ **Bad:** "For planning, email nicole@woodthumb.com..."
✅ **Good:** Response ends with guiding question

### 5. Guide Conversation
**Rule:** End responses with follow-up questions

Examples:
- "Which one interests you?"
- "Want to see prices?"
- "Ready to book?"
- "How many people in your group?"

---

## Action Chips System

### Types of Chips:

**1. Follow-Up Action (Blue Border)**
- Automatically sends a message
- Example: [See Prices] → sends "What are the prices?"
- Example: [Check Availability] → sends "What dates are available?"

**2. Booking Link (Solid Blue)**
- Opens booking page in new tab
- Example: [Book Now] → opens Xola/Acuity
- Example: [View Schedule] → opens workshop calendar

### When Chips Appear:

**Scenario 1: Listing Workshops**
```
Response: "We have 5 beginner workshops: Triangle, Cutting Board..."
Chips: [See Prices] [View Schedule]
```

**Scenario 2: Listing Team Events**
```
Response: "6 team options: Cutting Board, Derby, Picture Frame..."
Chips: [See Prices] [Book Team Event]
```

**Scenario 3: Gave Price**
```
Response: "Triangle Shelf is $94. Takes 2 hours."
Chips: [Book Now] → opens Xola booking page
```

**Scenario 4: Booking Link in Response**
```
Response contains Acuity/Xola URL
Chips: [Book Now] → opens that specific URL
```

---

## Code Changes

### 1. System Prompt (api/prompts.py)

**New Rules:**
```python
Response Rules - FOLLOW EXACTLY:
1. When listing workshops/events - NAMES ONLY (NO prices, NO links, NO details)
2. When asked "how much" - THEN give price + duration
3. NEVER paste URLs in response text
4. NEVER include email unless asked
5. End with guiding question
```

**Examples Added:**
```
Q: "What team events do you have?"
A: "We have 6 team options: Cutting Board, Bottle Opener, Derby,
    Triangle Shelf, Picture Frame, Virtual. Which one interests you?"

Q: "How much for cutting board?"
A: "Cutting Board is $85/person with $850 minimum. Takes 3 hours."
```

### 2. Action Chips (widget/nicole-widget.js)

**New Function:**
```javascript
function getFollowUpChips(message) {
  // Detects response type and suggests actions

  // If listing team events
  if (message.includes('team') && message.includes('Cutting Board')) {
    return [
      { text: 'See Prices', action: 'What are the prices?' },
      { text: 'Book Team Event', link: 'https://woodthumb.as.me/...' }
    ];
  }

  // If listing workshops
  else if (message.includes('Triangle') && !message.includes('$')) {
    return [
      { text: 'See Prices', action: 'What are the prices?' },
      { text: 'View Schedule', link: 'https://woodthumb.com/workshops' }
    ];
  }
}
```

**Chip Rendering:**
```javascript
followUpChips.forEach(chip => {
  if (chip.link) {
    // Opens URL in new tab
    html += `<a href="${chip.link}" target="_blank">${chip.text}</a>`;
  } else if (chip.action) {
    // Sends message automatically
    html += `<button onclick="sendMessage('${chip.action}')">${chip.text}</button>`;
  }
});
```

### 3. CSS Styling (widget/nicole-widget.css)

**Action Chips:**
```css
.nicole-action-chips {
  margin-top: 8px;
  display: flex;
  gap: 8px;
}

.nicole-action-chip {
  background: white;
  color: #5b9db5;  /* Wood Thumb blue */
  border: 1px solid #5b9db5;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 13px;
}

.nicole-action-chip:hover {
  background: #5b9db5;
  color: white;
}
```

**Book Now Chip:**
```css
.nicole-booking-chip a {
  background: #5b9db5;  /* Solid blue */
  color: white;
  padding: 10px 20px;
  border-radius: 20px;
}
```

---

## Example Conversations

### Conversation 1: Team Event Booking

```
User: "What team events do you have?"

Nicole: "We have 6 team building options: Cutting Board, Bottle Opener,
         Pinewood Derby, Triangle Shelf, Picture Frame, Virtual Workshop.
         Which one interests you?"

[See Prices] [Book Team Event]


User: *clicks [See Prices]*

Nicole: "Team event pricing: $85/person for most options (Cutting Board,
         Bottle Opener, Triangle, Virtual). Pinewood Derby is $95/person.
         Picture Frame is $148/person. All have $850+ minimums and require
         $200 deposit."

[Book Team Event]


User: "I want the Derby"

Nicole: "Pinewood Derby is $95/person, $1,200 minimum. 3-hour workshop
         where teams design and race wooden cars. Great for competition!
         How many people?"

[Book Now]
```

### Conversation 2: Workshop Discovery

```
User: "What workshops do you offer?"

Nicole: "We have 5 beginner workshops: Triangle Shelf, Cutting Board,
         Deco Shelf, Picture Frame, Wedge Table. Which one?"

[See Prices] [View Schedule]


User: *clicks [See Prices]*

Nicole: "Triangle Shelf and Cutting Board are $94 each. Deco Shelf is $134.
         Picture Frame and Wedge Table are $148 each. Want to book one?"

[View Schedule]


User: "How do I book triangle shelf?"

Nicole: "Triangle Shelf is $94. Takes 2 hours. Perfect for beginners!"

[Book Now]  ← Opens Xola booking page
```

---

## Benefits

### For Users:
✅ Less overwhelming - information revealed step-by-step
✅ Easy to tap chips on mobile
✅ Clear next actions
✅ Conversational and natural
✅ No need to copy/paste links

### For Business:
✅ Guides users to booking
✅ Reduces support emails
✅ Professional UX (like Intercom/Drift)
✅ Higher conversion (easier to book)
✅ Collects info step-by-step for team events

---

## Testing Results

### Test 1: Team Events
```bash
Input: "What team events do you offer?"
Output: Clean list of 6 names only
Chips: [See Prices] [Book Team Event]
✅ PASS
```

### Test 2: Workshop Pricing
```bash
Input: "What workshops do you offer?"
Output: 5 workshop names
Chips: [See Prices] [View Schedule]

Then: "How much for cutting board?"
Output: "$94. Takes 2 hours."
Chips: [Book Now]
✅ PASS
```

### Test 3: Direct Booking
```bash
Input: "I want to book shop time"
Output: "$120/hour. Book up to 5 days in advance."
Chips: [Book Now] → Acuity link
✅ PASS
```

---

## Files Modified

1. **api/prompts.py** - Strengthened conversation rules
2. **widget/nicole-widget.js** - Added action chips system
3. **widget/nicole-widget.css** - Styled action chips

---

## Summary

Nicole now has a **guided conversation approach** that:
- Lists names only (no prices unless asked)
- Uses action chips instead of links in text
- Never includes email unless asked
- Asks follow-up questions to guide users
- Provides clear next actions

This creates a **modern, professional chat experience** that's:
- Less overwhelming
- Mobile-friendly
- Conversion-optimized
- Easy to use

**Status: Ready for production** ✅
