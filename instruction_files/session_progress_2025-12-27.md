# Med-Brief Development Progress - Session Dec 27, 2025

## Session Summary
This session focused on enhancing the Dashboard UI and adding article management features.

---

## Features Implemented

### 1. PubMed Article Fetching Improvements
- **Increased article limit** from 100 to 500
- **Batched fetching** - Articles fetched in batches of 100 to avoid HTTP 414 "URI Too Long" error
- **Sort by publication date** - Added `sort=pub_date` to PubMed query for newest articles first
- **Full abstract parsing** - Now joins ALL AbstractText elements (structured abstracts with Background, Methods, Results, Conclusions)
- **DOI extraction** - Properly extracted from ELocationID field

### 2. Dashboard Date Range Selector
- **From/To date pickers** instead of just preset days
- **Quick select dropdown** (Last 7/14/30 days + Custom) - auto-updates date pickers
- **Days limit extended** to 90 days
- **Dynamic header** shows selected date range

### 3. Article Detail Page (`/article/:pmid`)
- **PubMed-like layout** with centered abstract
- **Shows**: title, authors, journal, date, DOI (clickable)
- **Links**: View on PubMed, Full Text (DOI), PubMed Format
- **Export buttons**: TXT, RIS, NBIB for single article
- **Navigation**: Back to Dashboard, Previous/Next Article buttons
- **Route watcher** fixes for prev/next navigation

### 4. Article Export Functionality
- **Bulk export** from Dashboard - all visible articles
- **Export dropdown** - consolidated TXT/RIS/NBIB into single "Export" button
- **Single article export** from detail page
- **RIS/NBIB formats** include DOI field

### 5. Article Multi-Select (PARTIALLY WORKING)
- **Selection mode toggle** button in filter bar
- **Checkbox overlay** on cards when in selection mode
- **Visual feedback** - blue border on selected cards
- **"Export Selected" dropdown** when articles selected
- **Type fix** - converts pmid to String for consistent comparison

---

## Known Issues / TODO

### High Priority
1. **Selection mode still not updating** - The count shows (0) even after clicking cards
   - Debug: Check browser console for "Selected articles:" log
   - May need further debugging of reactivity with string array

### Medium Priority
2. Consider adding "Select All" / "Deselect All" buttons
3. Persist selection across page refresh (localStorage)

---

## Key Files Modified

### Frontend
- `frontend/src/views/Dashboard.vue` - Main dashboard with filters, selection, export
- `frontend/src/views/Article.vue` - Article detail page (NEW)
- `frontend/src/services/api.js` - Added date range params to generateBrief
- `frontend/src/router/index.js` - Added /article/:pmid route

### Backend
- `backend/app/services/pubmed.py` - Batched fetching, full abstract, DOI extraction
- `backend/app/routers/briefs.py` - Added from_date/to_date params, DOI to model

---

## How to Resume

1. **Start servers**:
   ```bash
   cd frontend && npm run dev
   cd backend && uvicorn main:app --reload --port 8000
   ```

2. **Debug selection issue**:
   - Open browser dev tools (F12 → Console)
   - Go to Dashboard, click "☐ Select"
   - Click an article card
   - Check console for "Selected articles:" output
   - If empty array or not logging, investigate reactivity

3. **Files to focus on**:
   - `/frontend/src/views/Dashboard.vue` lines 446-461 (`handleCardClick` function)
   - Check if `selectedArticles` ref is reactive properly

---

## Database
- SQLite database at `backend/medbrief.db`
- Contains users, profiles, journals tables
- Test user credentials would be whatever was registered during testing
