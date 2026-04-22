# Implementation Plan: Enhanced Workforce Simulation Model

**Branch**: `001-simulation-enhancements` | **Date**: 2026-04-21
**Spec**: `specs/001-simulation-enhancements/spec.md`
**Input**: Feature specification from `specs/001-simulation-enhancements/spec.md`

## Summary

Extend the simulation engine (simulation.py) with five new capabilities: headcount ceiling
management with recruiting demand output; experienced hire backfill at configurable seniority
presets; graduated retirement probability curve extending to age 75; an Early Careers cohort
pipeline tracking L3 apprentices, L6 apprentices, and graduates through their programmes with
annual dropout; and grade-aware population snapshots using the A1–D grade structure.

New Plotly charts (charts.py) surface recruiting demand and grade breakdowns. New sidebar
controls (app.py) expose all new parameters. The three-file separation-of-concerns architecture
is preserved throughout.

---

## Technical Context

**Language/Version**: Python 3.11 (Windows 11)
**Primary Dependencies**: streamlit>=1.32.0, pandas>=2.0.0, numpy>=1.26.0, plotly>=5.20.0
**Storage**: CSV files (local filesystem — `data/` directory or user upload via sidebar)
**Testing**: Manual functional testing via `streamlit run app.py`; no automated test suite in scope
**Target Platform**: Local web browser (Streamlit); designed for meeting-room presentation use
**Project Type**: Single-project Streamlit web application
**Performance Goals**: Interactive response for ~1,100 employee population; no strict latency
  requirement; all projections complete in < 5 seconds for 15-year horizon
**Constraints**: `PYTHONUTF8=1` prefix required for all CLI commands; three-file architecture
  enforced by constitution; Windows 11 host
**Scale/Scope**: ~1,100 employees; 5–15 year projections; single concurrent user

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design — see below.*

### Principle I — Separation of Concerns ✅

All new model logic (EC pipeline, experienced hire backfill, retirement curve, headcount ceiling
calculation) goes into `simulation.py`. New figure builders (recruiting demand, grade snapshot)
go into `charts.py`. New sidebar expanders and KPI display go into `app.py`. No cross-layer
imports are introduced.

### Principle II — Computational Integrity ✅ with one flagged note

**Updated simulation order per year:**
1. Age + 1, Service + 1
2. Attrition (flat rate, applied to full population)
3. Retirement proxy (age-scaled probability, applied to attrition survivors — AS-206 preserved)
4. EC cohort pipeline advancement (dropout applied; completers outturn to substantive workforce)
5. Headcount gap calculated: `gap = ceiling − current_headcount`
6. Experienced hires added: `hires = min(gap, round(gap × market_fill_rate))`
7. Recruiting demand recorded: `demand = max(0, gap − hires)`

**Flagged: Grade_Score derivation change.** The existing model takes `Grade_Score` as a raw
float from the CSV. This feature introduces a `Grade` column (A1–D) with a discrete mapping
(A1=1 … D=7) from which Grade_Score is derived. The WEI formula itself (`sum(Grade_Score ×
Service)`) is unchanged. For backward compatibility, `simulation.py` will detect which column is
present and use whichever exists; no existing CSVs break. However, any deployment using the Grade
column as primary input constitutes a change to how Grade_Score is sourced, and should be reviewed
against the constitution's MAJOR amendment criteria. **Owner sign-off is recommended before
the Grade column becomes the default input for production data.**

### Principle III — Assumption Transparency ✅

All new parameters are surfaced as sidebar controls with visible defaults. New assumptions
(experienced hire age/grade presets, market strength fill rates, EC dropout rates, retirement
curve shape) will be added to the assumptions register (`copilot-assumptions.md`). Scenario
comparison remains mandatory; no single-point-forecast output is added.

### Principle IV — Presentation Readiness ✅

New charts follow design standards (see `.impeccable.md`). Orange (`#FF5C32`) is used for
recruiting demand > 0 (a risk signal) and for WEI below the tipping point — never decoratively.
Sidebar is reorganised into labelled `st.expander` sections to prevent clutter as control count
increases.

### Principle V — Simplicity and Scope Control ✅

Job-family grade constraints (vocational A1–B2; engineering B2–D) are explicitly deferred. Grade
breakdown is P3 (lowest priority). EC pipeline is additive — it replaces only the simple
`_apply_inflow` function. Headcount ceiling adds one pass at the end of the simulation year.
No new files created; three-file architecture unchanged.

**Post-Phase-1 re-check**: See bottom of plan — all gates remain green after design phase.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-simulation-enhancements/
├── plan.md              # This file
├── research.md          # Phase 0 — design decisions
├── data-model.md        # Phase 1 — entity definitions and Grade mapping
├── quickstart.md        # Phase 1 — how to run and test changes
├── contracts/
│   └── simulation-api.md  # Phase 1 — simulation.py public function contract
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 — created by /speckit-tasks
```

### Source Code (repository root)

```text
/ (project root)
├── app.py              # Modified — new sidebar expanders, new KPI metrics, new tab/chart calls
├── simulation.py       # Modified — EC pipeline, experienced hires, ceiling, retirement curve
├── charts.py           # Modified — recruiting_demand_chart(), grade_snapshot_chart()
├── requirements.txt    # Unchanged (all required packages already present)
├── data/
│   └── sample_workforce.csv   # Unchanged (Grade_Score float — backward-compatible)
└── specs/
    └── 001-simulation-enhancements/
```

**Structure Decision**: Single-project layout, files at repo root. No new directories needed in
the source tree. All changes are modifications to existing files.

---

## Phase 0: Research Decisions

*Full rationale in `research.md`. Decisions summarised here.*

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Retirement curve shape | Linear ramp: `base_prob` at threshold → 1.0 at max_age (75) | Simple to explain, monotonically increasing, no cliff-edge, two-parameter control |
| EC cohort tracking | Rolling array per cohort type (list of floats by year-in-programme) | No external state; survives session restarts; pure-function compatible |
| Experienced hire implementation | Add rows to workforce DataFrame at end of year | Consistent with existing pattern; hires age naturally in subsequent years |
| Sidebar organisation | `st.expander` sections: Attrition, Retirement, Early Careers, Experienced Hires, Scenarios | Prevents control overload; sections collapse by default |
| Grade column backward compatibility | Column detection: `Grade` → mapped score; `Grade_Score` → raw float | No breaking changes to existing CSV format |

---

## Phase 1: Design Summary

*Full details in `data-model.md` and `contracts/simulation-api.md`.*

### Key Data Model Changes

1. **Employee record**: optional `Grade` field (A1–D string); `Grade_Score` derived via
   `GRADE_SCORE_MAP` constant if Grade present; existing float Grade_Score used if Grade absent.

2. **EC cohort state**: `ec_state` dict — `{'L3': [float, ...], 'L6': [...], 'Grad': [...]}`;
   each list has length = programme_years; index 0 = newest cohort, last index = graduating.

3. **Simulation output** (extended): `run_projection` returns updated result dict with keys:
   `recruiting_demand` (list[float]), `experienced_hires_added` (list[float]),
   `ec_outturn` (dict[str, list[float]]), `grade_snapshots` (list[dict]).

4. **Parameters struct**: new named parameters passed to `run_projection`:
   `ceiling`, `exp_hire_profile` (str), `market_strength` (str: 'strong' | 'moderate' | 'weak'),
   `ec_config` (dict), `retirement_max_age` (int).

### New Chart Functions (charts.py)

- `recruiting_demand_chart(years, demand, hires)` — bar chart; orange bars for demand, blue for hires
- `grade_snapshot_chart(grade_snapshots, year)` — horizontal bar chart per grade band

---

## Post-Phase-1 Constitution Re-check

All five principles remain ✅ after design phase. No new violations introduced. The Grade_Score
sourcing note from Principle II remains open and requires owner sign-off before production use.

---

## Implementation Notes

- `_apply_inflow` in `simulation.py` is replaced by `_advance_ec_pipeline` — same internal
  naming convention (leading underscore = internal, not exported).
- `run_projection` signature extends with keyword arguments only; default values maintain
  backward compatibility for callers that don't pass new parameters.
- Sidebar expanders should default to `expanded=False` except the primary Attrition control.
- The `REQUIRED_COLS` constant should be updated: `Grade` OR `Grade_Score` must be present
  (not both required); validation error message should explain the accepted formats.
