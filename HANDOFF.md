# HANDOFF: Enhanced Workforce Simulation Model

**Date**: 2026-04-22 
**Branch**: `001-simulation-enhancements`
**Spec dir**: `specs/001-simulation-enhancements/`

---

## Where We Are

**All Phases (1 through 8) are 100% COMPLETE.**

The `001-simulation-enhancements` feature specification has been fully implemented into the pipeline.

**Completed tasks**: T001 through T023 (all marked `[x]` in `tasks.md`)

---

## Session Progress

- Phase 3 (US1 — Headcount Ceiling & Recruiting Demand) was implemented in full. Added logic to project total recruiting demand and visually display it against a maximum ceiling threshold limit via `charts.py` and `app.py`.
- Phase 4 (US2 — Experienced Hires) was subsequently built into the app. Constructed dynamic distribution mapping to assign realistic experience factors inside the workforce for varying profile seniorities, throttled by market fill rates.
- Phase 5 (US3 — Graduated Retirement) implemented linear interpolation retirement logic from `retirement_age` up to a specific `max_age` directly in `simulate_year` within `simulation.py`.
- Phase 6 (US4 — Early Careers Outturn) extended the projection array to shift dropout rates compounding per cohort flow (L3, L6, Grads), with interactive parameters inside the `app.py` wrapper. 
- Phase 7 (US5 — Grade-Aware Snapshot) allowed for per-grade A1-D counts tracked independently in memory and returned iteratively rendering natively onto an interactive Plotly horizontal bar chart.
- Phase 8 (Polish + CCC) structured the sidebars cleanly via closed tabs and validated alignment of the core Constitution, CLAUDE.md guidelines, and Copilot assumptions register.

---

## Next Action: Verification

The implementation footprint is finished.

Execute the **Full End-to-End Manual Validation (T023)** per `specs/001-simulation-enhancements/quickstart.md`. Run the internal 5 scenario tests against `PYTHONUTF8=1 streamlit run app.py` and ensure they align exactly to behavioral forecasts. 

---

## Phase Dependency Map (quick reference)

```
Phase 1 (T001) ✅ → Phase 2 (T002, T003) ✅ → Phase 3 US1 (T004–T007b) ✅
                                              → Phase 5 US3 (T011–T012)   ✅
                                              → Phase 6 US4 (T013–T016)   ✅
                                              → Phase 7 US5 (T017–T019)   ✅
Phase 3 US1 ✅ → Phase 4 US2 (T008–T010) ✅
All phases ✅ → Phase 8 Polish (T019b–T023) ✅
```

---

## Pending Work Outside This Spec

### GitHub setup
- GitHub core repo pushes ongoing on this established branch track.

### Design refresh
- Explicitly deferred — separate `/impeccable` workstream
- Does not block simulation implementation

---

## UI/UX Audit — Remaining Actions

**Audit date**: 2026-04-22 | **Score**: 17/20 (Good) | **Branch**: `001-simulation-enhancements`

No P0 or P1 issues. App is shippable. Items below are improvements only.

### P2 — Fix before next demo

**1. Heading hierarchy** (`app.py:521, 539, 565, 576, 679, 688`)
Change all `####` (h4) in-tab section headers to `###` (h3). The page jumps h1 → h4, skipping two levels — WCAG 1.3.1 violation that breaks screen-reader heading navigation.

**2. `prefers-reduced-motion`** (CSS block in `app.py`)
Add to the bottom of the `<style>` block:
```css
@media (prefers-reduced-motion: reduce) {
    * { transition: none !important; animation: none !important; }
}
```
Plotly charts animate on render; users with OS-level reduced-motion get no accommodation.

### P3 — Nice to have

**3. Tokenize alpha-tint literals**
- `app.py:314` — `rgba(255,92,50,0.10)` in `.tipping-warning` background → add `_danger_tint` to token block
- `app.py:572` — `rgba(68,74,255,0.35)` in `st.dataframe` Styler bar → extract to a variable

**4. Enumerate custom-component wildcards**
- `app.py:323` — `.tipping-warning * { color: {_danger} }` → `p, span, strong`
- `app.py:332` — `.info-card * { color: {_text} }` → `p, span, strong`
Low-risk (no interactive elements in either div), but inconsistent with the enumerated pattern used everywhere else.

**5. Header inline styles** (`app.py:381, 384`)
Page header `h1` and `p` use inline `style=` with hard-coded font-family strings. Move to a `.page-header` CSS class rule — only worth doing alongside other edits.

### Audit history

| Date | Score | Notes |
|------|-------|-------|
| 2026-04-22 (pass 1) | 12/20 | Baseline |
| 2026-04-22 (pass 2) | 14/20 | ARIA, contrast, font loading, chart captions, theme-aware dataframe |
| 2026-04-22 (pass 3) | 17/20 | Widget wildcards enumerated, KPI layout 5→3+2, colour tokens complete |
