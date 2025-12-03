# Frontend Test Checklist

## ✅ Server Status
- **URL**: http://localhost:3000/
- **Status**: Running
- **Compilation**: Successful (25s)
- **Webpack**: No errors

## 📁 File Structure Verified
```
docusaurus-book/src/
├── components/
│   └── Chatbot/
│       ├── index.tsx ✅
│       └── styles.module.css ✅
├── services/
│   ├── chat_api.ts ✅
│   ├── conversation_api.ts ✅
│   └── search_api.ts ✅
└── theme/
    └── Root.tsx ✅ (import fixed)
```

## 🔍 What to Check in Browser

### 1. Open the Site
1. Open http://localhost:3000/ in your browser
2. Wait for page to load completely

### 2. Look for Chatbot Button
**Location**: Bottom-right corner
**Appearance**:
- Purple circular button
- 60px x 60px
- Contains 💬 emoji
- Gradient background (purple to pink)

### 3. Test Interaction
1. **Click** the purple button
2. **Expected**: Chat window opens
3. **Window should show**:
   - Header: "AI Assistant"
   - Close button (×)
   - Welcome message
   - Input textarea
   - Send button

### 4. Send a Test Message
1. Type: "What is Physical AI?"
2. Click "Send"
3. **Expected**:
   - Your message appears (right side, purple)
   - Loading indicator shows (3 dots)
   - Bot response appears (left side, white)
   - Response comes within 3 seconds

## 🐛 Troubleshooting

### If you don't see the button:

#### Check 1: Hard Refresh
- **Windows**: `Ctrl + Shift + R`
- **Mac**: `Cmd + Shift + R`
- This clears cache

#### Check 2: Console Errors
1. Press `F12` to open DevTools
2. Click "Console" tab
3. Look for red errors
4. Common issues:
   - Module not found
   - Failed to fetch
   - CORS error

#### Check 3: Check if Root.tsx is loading
1. In Console, type: `document.querySelector('.chatbotToggle')`
2. Press Enter
3. **Should return**: `<button class="chatbotToggle">...</button>`
4. **If null**: Chatbot not rendering

#### Check 4: Clear .docusaurus cache
```bash
cd docusaurus-book
rm -rf .docusaurus
npm start
```

### If button shows but doesn't work:

#### Check 1: Backend running?
- Open http://127.0.0.1:8000/health
- Should return: `{"status":"healthy"}`
- If not, start backend

#### Check 2: CORS error?
- Check console for:
  ```
  Access to fetch at 'http://127.0.0.1:8000' has been blocked by CORS policy
  ```
- **Fix**: Verify `backend/src/main.py` has `http://localhost:3000` in CORS origins

#### Check 3: Network tab
1. Press F12
2. Click "Network" tab
3. Send a message
4. Look for `/api/chat` request
5. Check status code:
   - 200 = OK
   - 404 = Endpoint not found
   - 500 = Server error
   - Failed = Backend not running

## 📱 Mobile Testing

### Desktop View (1920x1080)
- Button: Bottom-right, 60px
- Window: 400px wide, floating

### Tablet View (768px)
1. Press F12
2. Click "Toggle Device Toolbar" (phone icon)
3. Select "iPad"
4. Check chatbot adapts to smaller screen

### Mobile View (375px)
1. In Device Toolbar
2. Select "iPhone SE"
3. **Expected**:
   - Button stays bottom-right
   - Window opens full-screen
   - No rounded corners on mobile

## ✅ Success Criteria

You'll know it's working when:

- [ ] Purple button visible bottom-right
- [ ] Button has hover effect (grows slightly)
- [ ] Clicking opens chat window
- [ ] Window shows welcome message
- [ ] Can type in input field
- [ ] Send button is clickable
- [ ] Test message gets response
- [ ] Response shows within 3 seconds
- [ ] Can close window with × button
- [ ] Mobile view works (full-screen)

## 🎯 Quick Visual Test

**Look for this in bottom-right corner:**

```
┌─────────┐
│    💬   │  ← Purple gradient button
└─────────┘
```

**After clicking:**

```
┌──────────────────────────────┐
│ AI Assistant            ×    │
├──────────────────────────────┤
│ Welcome! Ask me anything     │
│ about the Physical AI        │
│ textbook.                    │
│                              │
│ (Backend server required     │
│  for live responses)         │
├──────────────────────────────┤
│ [                         ]  │
│ [  Type your question...  ]  │
│ [                         ]  │
│                              │
│                      [Send]  │
└──────────────────────────────┘
```

## 🔄 If Still Not Working

Try this nuclear option:

```bash
# Kill all Node processes
taskkill /F /IM node.exe

# Clean everything
cd docusaurus-book
rm -rf node_modules .docusaurus build
npm install
npm start
```

Then refresh browser.

---

**Current Status**: Frontend compiled successfully with no errors! ✅
