# MedBrief UI Style Guide

## Design Intent
A warm, modern reading experience that feels like a premium news app. The design keeps users engaged with comfortable reading aesthetics—warm neutrals reduce eye strain while terracotta accents draw attention to actions without being aggressive.

---

## Color System

| Role | Token | Hex | Usage |
|------|-------|-----|-------|
| **Primary** | `terracotta-500` | `#E07A5F` | Buttons, active nav, key icons |
| **Primary Hover** | `terracotta-600` | `#C65D45` | Button/link hover states |
| **Accent** | `amber-500` | `#F59E0B` | Badges, highlights, "new" indicators |
| **Dark Text** | `warm-900` | `#292524` | Headlines, nav brand |
| **Body Text** | `warm-700` | `#44403C` | Article body, readable contrast |
| **Muted Text** | `warm-500` | `#78716C` | Metadata, dates, secondary info |
| **Background** | `cream-50` | `#FFFBF5` | Main app background |
| **Card BG** | `white` | `#FFFFFF` | Article cards |
| **Border** | `warm-200` | `#E7E5E4` | Card borders, dividers |
| **Success** | `sage-500` | `#65A30D` | Completed states |
| **Danger** | `rose-500` | `#E55353` | Delete actions, errors |

**Contrast guidance:** Keep text-to-background contrast ≥ 4.5:1.

---

## Typography

- **Font Stack:** `"Inter", "Segoe UI", system-ui, -apple-system, sans-serif`
- **Scale:** `.fs-2` (32px) for page titles, `.fs-5` (20px) for section headers, `.fs-6` (16px) for body
- **Weight Hierarchy:**
  - Headings: `fw-semibold`, warm-900
  - Body: `fw-normal`, warm-700
  - Metadata: `fw-light`, warm-500

---

## Layout & Spacing

- Max content width: **960px** (`.container`)
- Cards: borderless with `shadow-sm`, `rounded-3`
- Hover effect: `transform: translateY(-4px)` with `0.15s ease-in-out` transition
- Spacing: Use `gap-3` for consistent gutters

---

## Components

### Navbar
- White background with border-bottom
- Brand: Terracotta icon + warm-900 text
- Nav links: warm-700, hover terracotta-500

### Buttons
- **Primary:** Terracotta background, white text
- **Secondary:** Outline terracotta
- **Danger:** Rose-500 background
- Add `btn-lg px-4` on hero CTAs

### Cards
- White background on cream
- `shadow-sm` + `rounded-3`
- Hover: slight lift effect
- Title: `fw-semibold`, warm-900
- Metadata: warm-500

### Forms
- Standard labels above controls
- Border: warm-200
- Focus: terracotta ring

### Alerts
- Use Bootstrap alert variants
- Favor `alert-info` for neutral tone

---

## Iconography

**Library:** Lucide (`lucide-vue-next`)

| Context | Icon |
|---------|------|
| Brand/Logo | `BookOpen` |
| Search | `Search` |
| Refresh | `RefreshCw` |
| Dashboard | `LayoutDashboard` |
| Profiles | `Users` |
| Export | `Download` |
| Article | `FileText` |
| Logout | `LogOut` |
| Calendar | `Calendar` |
| Journal | `Newspaper` |
| External Link | `ExternalLink` |

**Style:** Stroke icons, 20-24px size, colored with terracotta-500 or warm-500.

---

## Interaction Details

- **Hover:** Buttons darken 10%; cards lift; links show underline
- **Transitions:** `0.15s ease-in-out`
- **Focus:** Preserved Bootstrap focus ring with terracotta tint
- **Empty states:** Cream panel with outline icon, muted text, primary button

---

## Usage Checklist

1. Import Inter font from Google Fonts
2. Import Bootstrap 5.3 CSS/JS
3. Install `lucide-vue-next` for icons
4. Apply palette via CSS variables in `theme.css`
5. Use utility classes; avoid inline styles
