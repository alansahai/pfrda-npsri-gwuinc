# ❌ CALCULATION NOT WORKING - DIAGNOSED & FIXED

## What You're Seeing
✅ Form loads (good!)
✅ Slider works (good!)
❌ Click "Calculate" button → nothing happens

## Root Cause
**Backend server is NOT running**

The frontend is running (that's why you see the form), but when you click "Calculate", the frontend tries to reach the backend to do the calculations, and the request fails silently.

---

## How to Fix (3 Steps)

### Step 1: Stop Any Running Servers
Close all terminal windows with Python running (they'll have "python" or "uvicorn" in the title).

### Step 2: Start Both Servers
Open PowerShell and run:
```powershell
cd d:\PFRDA
.\START_SERVERS.ps1
```

**Wait for both messages:**
- ✅ "Application startup complete" (Backend)
- ✅ "Serving HTTP on 0.0.0.0:8080" (Frontend)

### Step 3: Test
1. Open browser: **http://localhost:8080**
2. Hard refresh: **Ctrl+Shift+R** (clears cache)
3. Click "Calculate ➤" button
4. Should see loading state, then results

---

## Verify It's Working

### Check Backend Status
```powershell
# In PowerShell, run:
.\CHECK_BACKEND.ps1
```

Should show:
```
✅ BACKEND IS RUNNING!
✅ FRONTEND IS RUNNING!
```

### Check Browser Console (F12)
After clicking "Calculate", you should see:
```
💬 Calculating projection...
📤 API Request: http://localhost:8000/api/v1/forecast/retirement {...}
✅ API Response received: {...data...}
🏆 Calculation complete!
```

If you see ❌ errors instead, look for:
- "Cannot connect to backend" → Backend not running
- "API endpoint not found" → Backend URL is wrong
- Network error → Backend on wrong port

---

## What Was Fixed in Code

### Fixed File: `app.js`

**1. Language Initialization Error**
- **Before**: Tried to find non-existent `h3` elements in KPI cards → crashed
- **After**: Correctly finds `.kpi-label` divs → no crash

**2. Calculation Error Logging**
- **Before**: `console.error('Calculation error:', error)` → vague message
- **After**: Detailed logging showing exact API URL, request payload, response
- **Benefit**: Can now see exactly what went wrong

**3. Better Error Messages**
- **Before**: Generic "Failed to calculate"
- **After**: Tells you if backend isn't running, network issue, timeout, etc.

### Fixed File: `styles.css`

**1. Removed Duplicate CSS Rules**
- Duplicate `* { margin: 0; ... }` at EOF was causing conflicts

**2. Fixed Panel Visibility**
- Ensured `pointer-events: auto` on all form controls
- Forms now stay interactive when switching steps

### Created Files

**START_SERVERS.bat** & **START_SERVERS.ps1**
- Starts both servers correctly
- Uses `python -m http.server 8080 --directory .` (was incorrectly `index.html`)

**CHECK_BACKEND.ps1**
- Quickly verify both servers are running
- Shows API URLs and status

---

## Complete Step-by-Step: Fresh Start

If you're still having issues, do this exactly:

### Terminal 1: Start Backend
```powershell
cd d:\PFRDA\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**WAIT for**: `Application startup complete`

### Terminal 2: Start Frontend  
```powershell
cd d:\PFRDA\frontend
python -m http.server 8080 --directory .
```

**WAIT for**: `Serving HTTP on 0.0.0.0:8080`

### Browser
1. Open: `http://localhost:8080`
2. Hard refresh: `Ctrl+Shift+R`
3. Fill form:
   - Current Age: 30
   - Retirement Age: 60
   - Monthly Contribution: (use slider, default 10,000)
   - Risk Profile: Moderate
4. Click "Calculate ➤"
5. **Should see loading**, then chart + KPI values

---

## Expected Behavior

### Loading State
- Button becomes disabled
- Button text changes
- Loader appears briefly

### Results Display
- Chart appears with three lines (p10, p50, p90)
- KPI cards animate with values
- Page scrolls to show results
- Step indicator advances (1→2→3)

### Troubleshooting If Still Broken

| Issue | Check |
|-------|-------|
| Nothing happens when I click | Is backend running in Terminal 1? |
| Error appears after click | Check Backend endpoint (should be `/api/v1/forecast/retirement`) |
| Form not interactive | Hard refresh: `Ctrl+Shift+R` |
| Can't start servers | Python not installed? Run `python --version` |
| Port already in use | Close other Python windows, wait 10 seconds, retry |

---

## URL Reference
- Frontend: `http://localhost:8080`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`

---

## Dashboard Calculation Flow

```
1. User fills form
   ↓
2. User clicks "Calculate"  
   ↓
3. Frontend disables button, shows loader
   ↓
4. Frontend POSTs to backend:
   POST http://localhost:8000/api/v1/forecast/retirement
   with: age, retirement_age, contribution, risk_profile
   ↓
5. **If backend not running**: ERROR (network fail, timeout, etc)
   **If backend running**: Returns corpus + pension data
   ↓
6. Frontend receives response
   ↓
7. Frontend updates:
   - KPI cards (animate numbers)
   - Chart (draw percentile lines)
   - Step indicator (advance to 3)
```

**If step 4 fails** (backend not running), everything stops there.

---

**Key Point**: Make sure BOTH servers are running:
1. ✅ Backend on port 8000 (shows "Application startup complete")
2. ✅ Frontend on port 8080 (shows "Serving HTTP on 0.0.0.0:8080")

Then reload the browser and try clicking "Calculate" again.
