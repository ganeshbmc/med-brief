# Session Progress 2026-01-30

## Executive Summary
- Added backend fallback to NLM Catalog for journal searches with no local matches, enabling discovery of journals not in the seeded database.
- Fixed profile editing journal selection to toggle individual search results and support adding new journals.

## Changes
- backend/app/routers/journals.py: added SearchJournalOut response model and NLM fallback logic with ISSN mapping to existing local journals.
- frontend/src/views/Profiles.vue: corrected search selection handling and added support for new journals during profile edits.
- frontend/src/services/api.js: include new journals when updating profiles.
- backend/app/routers/profiles.py: accept and persist new journals on profile update.

## Verification
- Ran `bash scripts/restart-dev.sh`.
- Tests not run.
- Manual verification not run.

## Commits
- 3292ba8 fix: fallback journal search to NLM
- fix: allow per-journal selection in profile editor
