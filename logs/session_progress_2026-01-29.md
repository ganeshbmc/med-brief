# Session Progress - 2026-01-29

## Executive Summary
- Added a global 401 handler to redirect to login and clear cached article context.
- Added a login toast for session-expired redirects.
- Merged the fix PR into agy.

## Changes
- Updated API request helper to detect session expiry, clear session-scoped article data, and force navigation to login: `frontend/src/services/api.js`.
- Added a session-expired toast on login and cleared the query flag after showing: `frontend/src/views/Login.vue`.

## Verification
- Dev servers restarted via `bash scripts/restart-dev.sh`.
- No automated tests run.

## Commits
- d524651 fix: redirect on session expiry
- 7c224f1 Merge pull request #64 from ganeshbmc/agy-issue-62-article-reload
