# Med-Brief Development Progress - Session Dec 28-29, 2025

## Session Summary
This session focused on completing GitHub Issues #4, #5, and #6, and fixing several bugs.

---

## Features Implemented

### 1. Issue #4: PubMed Journal Search & Custom Profile (Complete ✅)
- **PubMed Journal Search** - NLM Catalog API integration (`nlm_catalog.py`)
- **Dynamic Journal Creation** - New journals from PubMed search auto-added to DB
- **"Custom" Profile Option** - Moved to top of specialty list with distinct purple styling

### 2. Issue #5: Dashboard Caching (Complete ✅)
- **Pinia Store** - New `dashboard.js` store for session-level caching
- **Smart Fetching** - Dashboard uses cached data when available, no reload on navigation
- **Cache Invalidation** - Clears on profile/date change or manual refresh

### 3. Issue #6: Scroll Position Preservation (Complete ✅)
- **Save Scroll** - Position saved to store before navigating to article
- **Restore Scroll** - Position restored with `setTimeout(100ms)` after Dashboard renders
- **Article View** - Scrolls to top on mount
- **Vue Router scrollBehavior** - Added for browser back/forward navigation

---

## Bugs Fixed

### 1. Delete Profile Modal Not Clickable
- **Root Cause**: Modal buttons missing `type="button"` attribute
- **Fix**: Added `type="button"` and `pointer-events: auto` to modal buttons
- **File**: `frontend/src/views/Profiles.vue`

### 2. Journal Names Showing as "Journal #ID" on Profiles Page
- **Root Cause**: `loadJournalNames()` only searched hardcoded terms
- **Fix**: Use `getJournalsByIds` API to fetch actual journal info for profile journals
- **File**: `frontend/src/views/Profiles.vue`

---

## Key Files Modified

### Frontend
| File | Changes |
|------|---------|
| `stores/dashboard.js` | **NEW** - Pinia store for caching |
| `views/Dashboard.vue` | Refactored to use dashboard store |
| `views/Article.vue` | Scroll to top on mount, goBack uses router.push |
| `views/Profiles.vue` | Fixed delete modal, fixed journal names loading |
| `views/Onboarding.vue` | Custom profile styling, PubMed search integration |
| `services/api.js` | Added searchPubmedJournals, updated createProfile |
| `router/index.js` | Added scrollBehavior |

### Backend
| File | Changes |
|------|---------|
| `services/nlm_catalog.py` | **NEW** - NLM Catalog API for PubMed journal search |
| `routers/journals.py` | Added PubMed search endpoint |
| `routers/profiles.py` | Support new_journals for dynamic journal creation |

---

## Git Commits (agy branch)

1. `142dd8d` - feat: Issue #4 - PubMed journal search and Custom profile improvements
2. `0679889` - feat: Issue #5 - Dashboard caching to prevent reload on navigation  
3. `661eeff` - feat: Issue #6 - Scroll position with manual save/restore
4. `f859d74` - fix: Delete profile modal buttons not clickable
5. (pending) - fix: Journal names display on Profiles page

---

## How to Resume

1. **Start servers**:
   ```bash
   # Backend
   wsl bash -c "cd /mnt/d/Github/med-brief/backend && python3 -m uvicorn main:app --reload --port 8000"
   
   # Frontend
   wsl bash -c "cd /mnt/d/Github/med-brief/frontend && source ~/.nvm/nvm.sh && npm run dev"
   ```

2. **Branch**: All work on `agy` branch

3. **Remaining issues**: Check GitHub for open issues
