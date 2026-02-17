# Session Progress - 2026-02-17

## Executive Summary
- Added last login tracking and surfaced it on the dashboard alongside the date range.

## Changes
- backend/app/models.py: added `last_login_at` field to `User`.
- backend/app/routers/auth.py: persisted `last_login_at` on login and exposed it via `UserOut`.
- backend/alembic/versions/c3d8e1b2a9f0_add_last_login_at.py: migration to add `last_login_at` column.
- frontend/src/utils/dateFormatter.js: added datetime formatting and days-ago helper.
- frontend/src/views/Dashboard.vue: updated subtitle copy and added last-login line.

## Verification
- `bash scripts/restart-dev.sh`

## Commits
- feat: track last login and surface it on dashboard
