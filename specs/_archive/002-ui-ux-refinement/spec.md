# Feature Specification: UI/UX Refinement — Design System Alignment

**Feature Branch**: `002-ui-ux-refinement`  
**Created**: 2026-04-22  
**Status**: Draft  
**Input**: User description: "I want to refine the UI/UX using /impeccable commands. I already have .impeccable.md"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Daylight Presentation (Priority: P1)

A people analytics lead opens the tool in a meeting room to walk a group of directors through a workforce scenario. The interface loads in light mode by default. Charts and KPI cards are clean, high-contrast, and screenshot-ready. Every visible element uses the corporate palette — black on white, with orange for risk signals and blue for interactive data. The presenter takes screenshots directly into a slide pack with no colour correction needed.

**Why this priority**: Light mode is the stated default presentation context in the design system. Currently the tool only renders dark mode, which fails entirely in well-lit meeting rooms and looks inconsistent in slide packs.

**Independent Test**: Open the app cold. Verify it renders in light mode with correct palette and typography without any action from the user.

**Acceptance Scenarios**:

1. **Given** the app loads for the first time, **When** no preference is set, **Then** the interface renders in light mode with white background, black text, and the correct corporate palette.
2. **Given** the tool is in light mode, **When** the user takes a screenshot of any chart or KPI panel, **Then** the screenshot is suitable for pasting directly into a slide deck without colour adjustments.
3. **Given** a risk condition is active (WEI below 0.85), **When** the user views the warning banner, **Then** the alert uses bright orange (#FF5C32) not red, consistent with the brand palette.

---

### User Story 2 — Theme Toggle for Personal Preference (Priority: P2)

A user working late at their desk switches the interface to dark mode. The toggle is visible in the sidebar. The switch is immediate and all charts, cards, and text update to the dark palette without a page reload. On next session the preference is not persisted — the tool returns to light mode.

**Why this priority**: The design system explicitly specifies a switchable light/dark mode. This is needed for personal comfort and accessibility but is secondary to the default presentation use case.

**Independent Test**: Can be tested in isolation by verifying the toggle control switches all visual elements between two coherent colour states.

**Acceptance Scenarios**:

1. **Given** the app is in light mode, **When** the user activates the dark mode toggle in the sidebar, **Then** all backgrounds, text, charts, and cards update to the dark palette immediately.
2. **Given** the app is in dark mode, **When** the user deactivates the toggle, **Then** the interface returns to light mode with no visual artefacts.
3. **Given** a new session begins, **When** the app loads, **Then** light mode is the default regardless of prior session state.

---

### User Story 3 — Typography Legibility at Presentation Scale (Priority: P3)

A user views the app on a projector at reduced resolution. Headings and KPI values are rendered in Bricolage Grotesque, giving the interface a distinctive, professional warmth. Body text and chart labels use Manrope, which remains legible at small sizes. The user can read all chart labels and table values without leaning towards the screen.

**Why this priority**: Typography is a brand differentiator and a legibility requirement. Inter (currently loaded) is not the specified typeface and produces a generic SaaS appearance that the design system explicitly calls out as an anti-reference.

**Independent Test**: Load the app and inspect any heading or KPI value — font should be Bricolage Grotesque. Inspect any axis label or table body — font should be Manrope.

**Acceptance Scenarios**:

1. **Given** the app loads, **When** the user views any section heading or KPI value, **Then** the text renders in Bricolage Grotesque at the correct weight.
2. **Given** the app displays a chart, **When** the user inspects axis labels and tooltips, **Then** labels render in Manrope.
3. **Given** the app is viewed on a projector at 1024×768, **When** the user reads the KPI panel, **Then** all values and delta labels are legible without zooming.

---

### User Story 4 — Correct Brand Accent in Interactive Elements (Priority: P3)

A user interacts with a data series on a chart. The primary data line is blue (#444AFF), correctly signalling precision and action per the design system. No purple (#6C63FF) appears anywhere in the interface — the brand signal is internally consistent. Orange is reserved exclusively for risk markers; blue is used for all primary interactive and data series elements.

**Why this priority**: The current accent colour is a near-purple that is not in the design system and contradicts the intended brand signal. This creates brand inconsistency visible in every chart.

**Independent Test**: Visual inspection of all charts — no purple data series should appear. Primary line and bars should be #444AFF.

**Acceptance Scenarios**:

1. **Given** the WEI trend chart displays, **When** the user views the primary WEI line, **Then** it renders in #444AFF (blue), not #6C63FF (purple).
2. **Given** any chart displays a primary data series, **When** the user views the colour, **Then** it is either #444AFF (action/primary) or #FF5C32 (risk), never an off-brand purple.
3. **Given** the interface displays interactive controls, **When** active state is visible, **Then** it uses #444AFF or #FF5C32, not any off-brand colour.

---

### Edge Cases

- What happens when the user's browser blocks Google Fonts? The layout should still function with system fallback fonts (sans-serif stack).
- What happens when dark mode is toggled mid-simulation? Chart colours should update without triggering a new projection run.
- How does the interface render on a 4K display? Typography scale should not produce oversized elements — fixed rem scale per design system.
- What happens when a KPI value is negative or very long? Card layout should not break; text should truncate or wrap gracefully.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The interface MUST render in light mode by default (white background, black text, corporate palette).
- **FR-002**: The interface MUST provide a dark mode toggle in the sidebar that switches all visual elements — charts, cards, text, backgrounds — without reloading the page.
- **FR-003**: All headings and KPI display values MUST render in Bricolage Grotesque.
- **FR-004**: All body text, chart labels, table content, and form labels MUST render in Manrope.
- **FR-005**: The primary data accent colour throughout the interface MUST be #444AFF (blue), replacing the current #6C63FF (purple).
- **FR-006**: Orange (#FF5C32) MUST be used exclusively for risk signals, tipping-point markers, and alerts — never for decorative or primary data use.
- **FR-007**: Light orange (#FFA851) MAY be used for secondary warmth accents where appropriate.
- **FR-008**: The dark mode palette MUST use design-system-aligned colours (#1A1A1A background, #FFFFFF text) rather than the current off-system dark palette (#0F172A, #1E293B).
- **FR-009**: CSS theming MUST be implemented via CSS custom properties so that theme switching is atomic — a single variable set change updates the entire interface.
- **FR-010**: All charts MUST update their colour palette to reflect the active theme (light or dark) when the toggle is activated.

### Key Entities

- **Theme state**: Light or dark. Determined at session start (default: light). Switchable via sidebar toggle. Not persisted across sessions.
- **Design token**: A CSS custom property binding a semantic role (e.g., `--color-bg`, `--color-accent`) to a hex value for the active theme. All colours in the UI must derive from tokens, not hard-coded values.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The interface loads in light mode on 100% of cold starts, with no user action required.
- **SC-002**: Theme switching completes within 300ms of toggle activation, with no chart flicker or layout shift.
- **SC-003**: 100% of text elements visible in the interface use either Bricolage Grotesque (headings/KPIs) or Manrope (body/labels), verified by browser font inspector.
- **SC-004**: Zero instances of #6C63FF (off-brand purple) appear in any rendered chart, card, or UI element.
- **SC-005**: Any chart screenshot taken in either light or dark mode is presentation-ready without post-processing colour correction.
- **SC-006**: The full interface (app + charts) uses only colours from the design system palette table in `.impeccable.md`, with no off-system hex values.

## Assumptions

- The impeccable review workflow (`/impeccable`) will be used to drive iterative refinement passes once the baseline palette and typography changes are implemented. This spec defines the target state; `/impeccable` commands guide execution quality.
- Google Fonts CDN is accessible in the deployment environment. If not, font files must be bundled locally.
- Theme state is session-scoped (Streamlit `st.session_state`). Cross-session persistence is out of scope.
- The existing tab and layout structure (3 tabs: Executive Summary, Demographics, Assumptions) is retained; this spec covers visual styling only, not information architecture changes.
- Simulation logic in `simulation.py` is out of scope — only `app.py` and `charts.py` are modified.
- Light mode is the primary delivery target; dark mode is secondary and can be delivered as a follow-on if time is constrained.
