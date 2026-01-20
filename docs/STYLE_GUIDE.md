# Product UI Style Guide — Local Document Extraction Copilot

**Purpose:** Provide explicit, enforceable UI standards for a business‑grade desktop application. This guide is mandatory for all E04 UI work.

**Hydrated JDs:** UX-001 (UX Designer), UX-002 (UI Designer), UX-003 (UX/UI Designer), UX-005 (Interaction Designer), UX-006 (Visual Designer). Requirements reflect their research, accessibility, hierarchy, and interaction standards.

---

## 1) Typography
**Font tokens (use these names everywhere):**
- `--font-sans`: "Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif
- `--font-mono`: "JetBrains Mono", "SFMono-Regular", Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace

**Primary font token:** `--font-sans`
**Monospace token:** `--font-mono`

**Type scale (px):**
- Display: 32 / 40 / 700
- H1: 24 / 32 / 700
- H2: 20 / 28 / 600
- H3: 16 / 24 / 600
- Body: 14 / 20 / 400
- Caption: 12 / 16 / 400

**Rules:**
- Use sentence case for headings.
- Max 2 font weights per screen (400, 600/700).
- Line height: 1.4–1.6 for body text.

---

## 2) Color Tokens
**Color tokens (use names, not raw hex in UI specs):**
- `--color-bg`: #F8FAFC
- `--color-surface`: #FFFFFF
- `--color-border`: #E2E8F0
- `--color-text-primary`: #0F172A
- `--color-text-secondary`: #475569
- `--color-text-muted`: #94A3B8

- `--color-primary`: #1D4ED8
- `--color-primary-hover`: #1E40AF
- `--color-primary-active`: #1E3A8A
- `--color-focus`: #93C5FD

- `--color-success`: #16A34A
- `--color-warning`: #D97706
- `--color-error`: #DC2626
- `--color-info`: #0EA5E9

**Contrast:** Minimum 4.5:1 for body text, 3:1 for large text.

---

## 3) Spacing & Layout
**Base spacing unit:** 4px
**Spacing scale:** 4, 8, 12, 16, 24, 32, 40, 48

**Layout grid:**
- Desktop: 12‑column grid, 24px gutters, 24px margins
- Content max width: 1200px

**Section spacing:**
- Between sections: 24–32px
- Between form rows: 16px
- Between labels and inputs: 8px

---

## 4) Components (Explicit Specs)

### Buttons
- Height: 36px
- Padding: 0 16px
- Radius: 6px
- Primary: background `--color-primary`, text `--color-surface`
- Secondary: background `--color-surface`, border `--color-border`, text `--color-text-primary`
- Destructive: background `--color-error`, text `--color-surface`
- Disabled: background `--color-border`, text `--color-text-muted`

### Inputs
- Height: 36px
- Padding: 8px 12px
- Border: 1px solid `--color-border`
- Focus: 2px ring `--color-focus` + border `--color-primary`
- Error: border `--color-error` + helper text `--color-error`

### Cards
- Background: #FFFFFF
- Background: `--color-surface`
- Border: 1px solid `--color-border`
- Radius: 8px
- Padding: 16–24px

### Tables
- Header background: `--color-bg`
- Row height: 40px
- Border: 1px solid `--color-border`

---

## 5) Required States (All UI)
Every component must include:
- Default
- Loading
- Empty
- Error
- Success (when applicable)

---

## 6) Evidence & Trust UI
- Evidence card shows: source, page, line, snippet, confidence.
- Missing evidence displays a warning banner with remediation text.
- Confidence shown as percentage with label (e.g., 72% Confidence).

---

## 7) Accessibility
- Keyboard navigation for all actions.
- Visible focus states using `--color-focus` ring.
- No color‑only status indicators; include text or icon labels.
- Minimum target size: 36px height, 8px spacing between controls.

---

## 8) Data Formatting
- Date display: "Jan 16, 2026" (UI), ISO in backend.
- Currency: symbol + two decimals, thousands separators (e.g., $1,240.00).
- IDs: monospace only in read‑only view; avoid in primary reading flow.

---

## 9) Interaction Standards
- Animations: max 200–250ms; ease-in-out.
- No motion on critical actions (submit, delete) beyond feedback.
- Progress indicators must show when actions exceed 400ms.

---

## 10) Compliance & Review
- Every UI task evidence must include a Style Guide adherence checklist.
- Non‑compliant UI is a blocker for QC sign‑off.

---

**Owner:** PM (default PM JD)
**Applies To:** E04 and all future UI work
