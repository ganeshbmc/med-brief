# Open SRMA Inspired UI Style Guide

## Design Intent
Create a calm, professional workspace that feels purpose-built for research operations. The look should communicate scientific rigor (sharp typography, balanced whites), but use rich blues and teals to hint at modern tooling. All elements lean on Bootstrap 5.3 utility classes so the style can be adopted quickly in another Flask or Vue front end.

## Color System

| Role | Token | Hex | Usage |
| --- | --- | --- | --- |
| Primary | `primary-500` | `#0D6EFD` | Buttons, key icons, links, highlighted metrics. Matches Bootstrap’s primary to stay consistent with the current project. |
| Dark Neutral | `ink-900` | `#1B2838` | Body text, nav brand, headers on white. Gives slightly softer contrast than pure black. |
| Mid Neutral | `ink-600` | `#4B5563` | Secondary text, form labels, helper copy. |
| Light Neutral | `cloud-100` | `#F8F9FA` | App background, card gutters, table rows hover. |
| Border | `cloud-300` | `#DEE2E6` | Card borders, table dividers, input outlines. |
| Accent | `teal-400` | `#20C997` | Data extraction or success callouts, icon backgrounds, badges. |
| Warning | `amber-400` | `#FFC107` | Pending reviews, “action required” banners. |
| Danger | `rose-500` | `#E55353` | Invalid inputs, destructive actions. |

**Contrast guidance:** Keep text-to-background contrast ≥ 4.5:1. When placing `primary-500` on white, use 700-weight text or uppercase buttons to maintain legibility.

## Typography
- **Base stack:** `"Inter", "Segoe UI", system-ui, -apple-system, sans-serif`. Inter is crisp and pairs well with Bootstrap spacing.
- **Scale:** Use Bootstrap display classes sparingly. Prefer `.fs-2` (32px) for page titles, `.fs-5` (20px) for section headers, `.fs-6` (16px) for body.
- **Weight mix:** Headings at `fw-semibold`, body at `fw-normal`, quiet metadata at `fw-light`. This mirrors the hierarchy in `home.html`.

## Layout & Spacing
- Max content width of 960px keeps focus on forms. Wrap long workflows in `.container` plus `py-5` sections.
- Cards remain borderless with `shadow-sm` and `rounded-3`. Introduce hover lift `transform: translateY(-4px);` for dashboards.
- Use `row gap-3` instead of nested margins to stay responsive.

## Components
- **Navbar:** `navbar navbar-expand-sm bg-body-tertiary border-bottom`. Brand left, auth actions right. Keep buttons `btn-outline-secondary` for neutral actions and `btn-primary` for conversion.
- **Buttons:** Solid primary for key actions, outline primary for secondary, `btn-link` for inline options. Add `btn-lg px-4` on hero CTAs.
- **Forms:** Bootstrap floating labels aren’t required; standard labels above controls keep clinical clarity. Ensure invalid feedback uses `.d-block` as seen in `auth_login.html`.
- **Cards:** Icon circle tinted with `primary-50` (use `rgba(13,110,253,0.1)`) and icon colored `primary-500`. Title `h5`, text `text-body-secondary`.
- **Alerts/Toasts:** Use Bootstrap alert variants but favor `alert-info` for general notifications to keep tone calm.

## Iconography
- Font Awesome 6.4 is already loaded. Stick to outlined/regular icons for utility (e.g., `fa-file-alt`, `fa-users`). Pair icon color with `primary-500` or `teal-400`.

## Interaction Details
- **Hover states:** Buttons gain 2% darker shade; cards lift; nav links show underline. Keep transitions at `0.15s ease-in-out`.
- **Focus states:** Respect Bootstrap’s default focus ring; no removal. Add `box-shadow: 0 0 0 0.2rem rgba(13,110,253,0.25);` for custom controls.
- **Empty states:** Use cloud background panel with an outline icon, short sentence (`text-muted`), and a primary button.

## Usage Checklist
1. Import Bootstrap 5.3 CSS/JS from CDN and Font Awesome 6.4.
2. Wrap every view in the shared base with navbar + container.
3. Apply the palette tokens via CSS variables or SCSS map to keep reusability.
4. Keep inline styles minimal; prefer utility classes plus a single supplemental stylesheet for hover effects.

Adhering to this guide will reproduce the open-srma feel—clean, confident, and research-ready—while remaining flexible for your new application.
