# Session Progress - December 31, 2025

## Focus: Backend Features, Reliability, and Production (Issues #14 - #20)

### Summary
Addressed a wide range of issues from frontend UX (Profiles, Dashboards) to backend features (User Accounts) and critical production infrastructure (Database Migrations, Deployment).

---

## Changes Made

### Features & Fixes
- **Issue #14 (Profiles UX):** Added success toast messages and "click-to-activate" on profile cards for better feedback.
- **Issue #15 (Journal Filters):** 
    - Improved search reliability using **ISSN-based matching** to handle NLM Catalog discrepancies.
    - Added normalization to strip trailing punctuation from journal names.
- **Issue #16 (User Account):** 
    - Implemented `GET /auth/me` endpoint.
    - Added standard User Account page (`/account`).
    - Updated Navbar to display the logged-in user's name.
- **Issue #17 (Login State):** 
    - Fixed issues where users weren't redirected away from protected routes.
    - Implemented proper cache invalidation on logout to prevent state leaks.
- **Issue #18 (Dashboard UI):** 
    - Extensive visual refactor of the Dashboard.
    - Improved typography and fixed badge text contrast issues.
- **Issue #19 (Branding):** 
    - Updated Login and Register pages to showcase the new MedBrief app icon.
- **Issue #20 (Production & DB):** 
    - **Critical Fix:** Resolved a database path ambiguity (`sqlite:///...`) that caused the backend to see an empty DB when running in WSL but a full DB when seeding in Windows.
    - **Production Fix:** Detected and fixed a schema mismatch in Production (`UndefinedColumn: full_name`) by implementing a "smart" Alembic migration that checks for column existence before adding it.

### Infrastructure & Deployment
- **Alembic Migrations:** 
    - Configured fully async Alembic migrations (`env.py`).
    - Disabled dangerous `create_all` in `main.py` to favoring controlled migrations.
- **Docker & Railway:** 
    - Updated `Dockerfile` to automatically run migrations on startup (`alembic upgrade head`).
    - created `docs/RAILWAY_DEPLOY.md` to document the deployment process and "Stamping" fix for existing databases.

---

## Commits
- `d9246d1` - fix(db): Add migration to backfill missing full_name column in production
- `f7cd7e5` - docs: Add Railway deployment guide
- `ce731d0` - chore: Cleanup debug code and scripts
- `64bfd40` - fix: Resolve SQLite path ambiguity and Journal search case-sensitivity
- `7608d02` - feat: Issue #16 - Implement user account page and navbar integration
- `669e37a` - fix: Issue #17 - Protect routes and fix login redirection state
- `ef97fd6` - fix: Issue #18 - Refactor dashboard UI layout
- `139e8b8` - fix: Issue #19 - Update Login and Register pages to use MedBrief icon
- `bbd5826` - feat: Issue #15 - Use ISSN-based matching for journal filter reliability
- `85f6ad3` - fix: Issue #14 - Profiles UX improvements (success messages, click-to-activate)

---

## Status
**Environment:** Production (Railway) is Live and Syncing.
**Next Up:** Issue #21 (User Preferences)
