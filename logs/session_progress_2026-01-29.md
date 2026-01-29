# Session Progress - 2026-01-29

## Executive Summary
- Added a global 401 handler to redirect to login and clear cached article context.
- Added a login toast for session-expired redirects.
- Restarted dev servers to apply frontend changes.

## Changes
- Updated API request helper to detect session expiry, clear session-scoped article data, and force navigation to login: `frontend/src/services/api.js`.
- Added a session-expired toast on login and cleared the query flag after showing: `frontend/src/views/Login.vue`.

## Verification
- Dev servers restarted via `bash scripts/restart-dev.sh`.
- No automated tests run.

## Commits
- No commits created.
