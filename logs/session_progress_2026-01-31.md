# Session Progress 2026-01-31

## Executive Summary
- Rebuilt the frontend visual system around an editorial, warm-neutral palette with terracotta accents and new typography tokens.
- Refactored the main dashboard flow into a premium news-style experience with refined navigation, filters, and article cards.
- Strengthened accessibility with skip-link navigation, focus-visible styling, and reduced-motion handling.
- Extended the new visual language to article reading and auth/onboarding experiences with refined layouts and inputs.
- Aligned dashboard and preferences naming, unified export button styling, and fixed preference changes to persist.
- Updated the landing page to an editorial pre-login experience with refreshed feature cards.
- Consolidated dashboard profile stats into a single row with a streamlined default indicator.
- Cleaned the profile switcher label styling, removed count badge, and broadened preference default range options.
- Updated dashboard profile truncation and refined the abstracts-only filter control.
- Removed the abstract badge from dashboard article cards.
- Kept the abstracts-only label and count on a single line.
- Aligned PDF styling with print-safe serif/sans typography and terracotta link accents.

## Changes
- frontend/src/assets/theme.css: new design tokens, typography, button/input/card styles, and accessibility refinements.
- frontend/src/assets/main.css: added layout utilities, summary tiles, toolbar patterns, and updated article card helpers.
- frontend/src/App.vue: redesigned top navigation with updated IA and accessibility updates.
- frontend/src/views/Dashboard.vue: restructured the dashboard masthead, filters, and article card layout.
- frontend/src/views/Article.vue: refreshed article layout with editorial header, metadata chips, and updated abstract section.
- frontend/src/views/Login.vue: redesigned auth layout with new card shell and input styling.
- frontend/src/views/Register.vue: aligned registration layout with updated auth patterns.
- frontend/src/views/ForgotPassword.vue: updated reset request view to new auth shell.
- frontend/src/views/ResetPassword.vue: refined reset form inputs and success messaging.
- frontend/src/views/Onboarding.vue: updated onboarding layout and input styling to match new system.
- frontend/src/views/Account.vue: refreshed account cards to match the editorial visual system.
- frontend/src/views/Preferences.vue: renamed and redesigned preferences layout; fixed edit flow and save behavior.
- frontend/src/views/Home.vue: redesigned pre-login landing page hero and feature cards.
- frontend/src/views/Dashboard.vue: consolidated profile summary row and added default/profile count indicators.
- backend/app/routers/preferences.py: expanded allowed default date ranges to include daily.
- frontend/src/views/Dashboard.vue: clamped profile label to two lines and restyled the abstracts-only toggle.
- frontend/src/assets/main.css: added clamp and toggle utility styles.
- frontend/src/views/Dashboard.vue: removed abstract badge from article cards.
- frontend/src/assets/main.css: prevented abstracts-only label wrapping.
- backend/app/services/pdf_generator.py: tightened margins and refreshed typography/colors for PDF output.

## Verification
- Ran `bash scripts/restart-dev.sh`.
- Tests not run.
- Manual verification not run.

## Commits
- Update theme tokens and UI utilities
- Update navigation and dashboard layout
- Chore: update session log
- Update shared auth and article utilities
- Refresh article detail layout
- Refresh auth and onboarding layouts
