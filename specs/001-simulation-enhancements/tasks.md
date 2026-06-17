---
description: "Task list — Enhanced Workforce Simulation Model"
---

# Tasks: Enhanced Workforce Simulation Model

**Input**: Design documents from `specs/001-simulation-enhancements/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/simulation-api.md ✅

**Tests**: No automated test suite in scope. Manual validation via `quickstart.md`.

**Organization**: Tasks are grouped by user story to enable independent implementation and
testing. All three source files live at the repo root (`app.py`, `simulation.py`, `charts.py`).

---

## Format: `[ID] [P?] [Story?] Description — file path`

- **[P]**: Can run in parallel with other [P] tasks in the same phase (different files or
  independent functions)
- **[Story]**: User story this task belongs to (US1–US5)
- Include exact function name or file path in every description

---

## Phase 1: Setup

**Purpose**: Add all new constants to `simulation.py` before any functional changes begin.
One file, no dependencies — establishes the shared vocabulary for all subsequent phases.

- [x] T001 Add constants GRADE_SCORE_MAP, GRADE_LABELS, EXP_HIRE_PRESETS, MARKET_STRENGTH_PRESETS, EC_COHORT_DEFAULTS to simulation.py (module level, after existing constants)

**Checkpoint**: All constants importable from simulation.py. Run `python -c "from simulation import GRADE_SCORE_MAP, EXP_HIRE_PRESETS"` without error.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Update the load/validate layer and run_projection signature so all user story
phases can build on a stable interface. No story work can begin until this phase is complete.

**⚠️ CRITICAL**: Phases 3–7 all modify or depend on `run_projection`; its extended signature
must exist before any user story implementation starts.

- [x] T002 Update REQUIRED_COLS and load_workforce() in simulation.py — detect Grade column (→ derive Grade_Score via GRADE_SCORE_MAP) or fall back to Grade_Score float; add Grade column as empty string when absent; raise ValueError for missing/unknown values
- [x] T003 Extend run_projection() signature in simulation.py — add keyword args: years, attrition_rate, retirement_threshold, retirement_max_age=75, retirement_base_prob=0.05, ec_config=None, ceiling=None, exp_hire_profile='mid', market_strength='moderate', seed=42; add new return dict keys recruiting_demand, experienced_hires_added, ec_outturn, grade_snapshots initialised as empty lists

**Checkpoint**: Existing app.py call `run_projection(df)` still works without changes. New
params accept defaults silently. Run `streamlit run app.py` and verify baseline still loads.

---

## Phase 3: User Story 1 — Headcount Ceiling and Recruiting Demand Signal (Priority: P1)

**Goal**: Show the annual unfilled-role gap when Early Careers outturn is insufficient to hold
headcount at the financial ceiling. Experienced hires default to zero in this phase.

**Independent Test**: Set ceiling to 1,100 and all EC intakes to zero. With attrition of 8%,
recruiting_demand KPI MUST show a positive value each year. Set ceiling=None to confirm the
metric disappears cleanly.

- [x] T004 [US1] Add headcount gap and recruiting_demand calculation to run_projection() year loop in simulation.py — after existing attrition/retirement steps: gap = max(0, ceiling − len(df)); append gap to recruiting_demand list; append 0.0 to experienced_hires_added list; skip ceiling logic if ceiling is None
- [x] T005 [P] [US1] Implement recruiting_demand_chart(years, demand, hires, scenario_name) in charts.py — grouped bar chart; orange bars for demand, blue bars for hires per year; follow palette from .impeccable.md; return go.Figure
- [x] T006 [US1] Add Headcount Ceiling sidebar expander (st.expander, collapsed by default) to app.py with a number_input for ceiling value; pass ceiling to run_projection kwargs
- [x] T007 [US1] Add Recruiting Demand KPI metric to app.py KPI row (below existing metrics); wire recruiting_demand_chart into Executive Summary tab using st.session_state.results
- [x] T007b [US1] Add ceiling reference line to headcount chart in app.py — draw a dashed horizontal line at the ceiling value on the headcount-over-time chart when ceiling is set; omit when ceiling is None

**Checkpoint**: With ceiling set and EC intake = 0, KPI shows demand > 0 each year. Chart
shows orange bars. Setting ceiling=None reverts to original behaviour with no demand metric.

---

## Phase 4: User Story 2 — Experienced Hire Backfill Scenarios (Priority: P1)

**Goal**: Fill the ceiling gap with experienced hires at a configurable seniority preset,
limited by recruiting market strength. Recruiting demand shows the residual unfilled gap.

**Independent Test**: Set ceiling=1,100, market='strong', profile='senior'. WEI at year 10
MUST be higher than the same scenario with profile='junior'. With market='weak', recruiting
demand MUST remain above zero even when senior profile is selected.

- [x] T008 [P] [US2] Implement _apply_experienced_hires(df, ceiling, profile_key, market_key, rng, next_id) in simulation.py — compute hires = min(gap, round(gap × MARKET_STRENGTH_PRESETS[market_key])); sample hire ages from truncated normal using EXP_HIRE_PRESETS[profile_key]; set Service = age − 22; append hire rows to df; return (df, hires_count, demand, next_id)
- [x] T009 [US2] Wire _apply_experienced_hires() into run_projection() year loop in simulation.py — call after EC outturn step (step 5 of simulation order in plan.md); update experienced_hires_added and recruiting_demand lists with actual values
- [x] T010 [P] [US2] Add Experienced Hires sidebar expander (st.expander, collapsed) to app.py with radio selector for profile (junior/mid/senior) and market strength (strong/moderate/weak); pass to run_projection kwargs

**Checkpoint**: Senior profile yields higher year-10 WEI than junior profile for identical
inputs. Recruiting demand bar in chart shrinks as market strength increases from weak → strong.

---

## Phase 5: User Story 3 — Extended Graduated Retirement Curve (Priority: P2)

**Goal**: Replace the hard-cutoff retirement proxy with a linear probability ramp from
retirement_base_prob at threshold age to 1.0 at retirement_max_age (default 75).

**Independent Test**: Load a CSV with 50 employees aged 62–72. Run a 10-year projection with
threshold=60, max_age=75. No single year MUST account for > 50% of the cohort exiting via
retirement. Confirm exits spread across all years.

- [x] T011 [US3] Rewrite _apply_retirement_proxy() in simulation.py — replace existing flat-probability logic with: p(age) = 0 if age < threshold; p(age) = base_prob + (1 − base_prob) × (age − threshold) / (max_age − threshold) clamped to [0,1] if threshold ≤ age ≤ max_age; p(age) = 1.0 if age > max_age; apply only to attrition survivors (AS-206 preserved)
- [x] T012 [US3] Add Retirement sidebar expander (st.expander, collapsed) to app.py with number_input for retirement_max_age (default 75) and retirement_base_prob slider (default 0.05); pass to run_projection kwargs

**Checkpoint**: With threshold=60, max_age=75 and an aged population, retirement exits are
visible in years 1–10 without a single-year spike. Adjusting max_age slider shifts the curve.

---

## Phase 6: User Story 4 — Early Careers Programme Pipeline (Priority: P2)

**Goal**: Replace the simple annual inflow with a three-cohort EC pipeline (L3, L6, Grad)
tracking participants year-by-year with dropout and outturn at programme completion.

**Independent Test**: Set L3=20, L6=10, Grad=15, all dropout=0%. Zero outturn in years 1–3.
Graduate outturn of 15 at year 2. L3 and L6 outturn at year 4. EC outturn by cohort type MUST
appear in the Assumptions tab matching these values.

- [x] T013 [P] [US4] Implement _advance_ec_pipeline(pipeline, annual_intake, dropout_rate, programme_years) in simulation.py — apply dropout, extract outturn from last slot, shift array, prepend new intake; return (updated_pipeline, outturn_count)
- [x] T014 [P] [US4] Implement _apply_ec_outturn(df, outturn_dict, next_id) in simulation.py — for each cohort type with outturn > 0, add rows to df using EC_COHORT_DEFAULTS for age, service, and grade_score; return (df, next_id)
- [x] T015 [US4] Replace _apply_inflow() calls in run_projection() year loop with _advance_ec_pipeline + _apply_ec_outturn calls in simulation.py; initialise ec_state from ec_config at start of projection; record per-cohort outturn in ec_outturn return dict key
- [x] T016 [US4] Add Early Careers sidebar expander (st.expander, collapsed) to app.py with number_input for L3/L6/Grad annual intake and slider for per-cohort dropout rate; display ec_outturn by cohort type in Assumptions tab

**Checkpoint**: With Grad=15 intake and dropout=0, ec_outturn['Grad'] shows 0,0,15,15,15...
(outturn starts at year 2). With 10% dropout, outturn ≈ 15 × 0.9^2 ≈ 12.15 at year 2.

---

## Phase 7: User Story 5 — Grade-Aware Population Snapshot (Priority: P3)

**Goal**: Add per-grade (A1–D) headcount to each simulation year's snapshot so planners can
track experience concentration by grade band.

**Independent Test**: Run a projection with a known grade mix and senior experienced hire
profile. grade_snapshots MUST show C-grade headcount increase in years where senior hires are
added. With no Grade column in CSV, all employees show in the unknown bucket or fall back to
Grade_Score-derived band — confirm no crash.

- [x] T017 [US5] Add grade_snapshots computation to run_projection() year loop in simulation.py — after each year, compute per-grade headcount from df['Grade'] column (or 'unknown' if absent); append dict to grade_snapshots list in return dict
- [x] T018 [P] [US5] Implement grade_snapshot_chart(grade_snapshots, selected_year) in charts.py — horizontal bar chart per grade (A1–D); colours from palette; return go.Figure
- [x] T019 [US5] Add grade snapshot chart and year selector to Demographics tab in app.py using st.session_state.results['grade_snapshots'] and grade_snapshot_chart()

**Checkpoint**: Demographics tab shows per-grade bars. Senior hire scenario shows C-grade
headcount increase. App runs without error when input CSV has no Grade column.

---

## Phase 8: Polish and Cross-Cutting Concerns

**Purpose**: Consistency, documentation, and validation across all delivered stories.

- [x] T019b [P] Amend constitution to v1.1.1 in .specify/memory/constitution.md — confirm Principle II 7-step simulation order and Grade/Grade_Score column wording are present; update Version line and Last Amended date if not already updated
- [x] T020 [P] Ensure sidebar expander order and collapse defaults in app.py: Attrition (expanded), Retirement (collapsed), Early Careers (collapsed), Experienced Hires (collapsed), Headcount Ceiling (collapsed), Projection Horizon (collapsed)
- [x] T021 [P] Update CLAUDE.md — simulation order section to reflect new 7-step order; Required CSV columns section to note Grade as alternative to Grade_Score
- [x] T022 [P] Add new rows to copilot-assumptions.md for: experienced hire age/grade presets, market strength fill rates, EC dropout defaults, retirement curve linear ramp, grade-to-score mapping (A1=1 … D=7)
- [x] T023 Full end-to-end manual validation per specs/001-simulation-enhancements/quickstart.md — run all 5 scenario tests and confirm expected outputs

---

## Dependencies and Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 (constants must exist before load_workforce update)
- **US1 (Phase 3)**: Depends on Phase 2 (run_projection signature must be extended)
- **US2 (Phase 4)**: Depends on Phase 3 (ceiling gap calculation must exist before hire fill)
- **US3 (Phase 5)**: Depends on Phase 2 only — independent of US1/US2
- **US4 (Phase 6)**: Depends on Phase 2 only — independent of US1/US2/US3
- **US5 (Phase 7)**: Depends on Phase 2 only — independent of other stories
- **Polish (Phase 8)**: Depends on all user story phases being complete

### User Story Cross-Dependencies

- US2 builds on US1 (requires ceiling gap from T004 before T009 can fill it)
- US3, US4, US5 are mutually independent after Phase 2

### Parallel Opportunities Within Each Phase

**Phase 3 (US1)**:
```
Parallel: T005 (charts.py)  ←── can run while T004 running (simulation.py)
Sequential: T006 → T007 (app.py, same file)
T007 depends on T004 and T005 being complete
```

**Phase 4 (US2)**:
```
Parallel: T008 (simulation.py function) + T010 (app.py)
Sequential: T008 → T009 (wire into run_projection)
```

**Phase 6 (US4)**:
```
Parallel: T013 (pipeline func) + T014 (outturn func) — both in simulation.py but independent functions
Sequential: T013, T014 → T015 → T016
```

**Phase 8 (Polish)**:
```
Parallel: T020 + T021 + T022 (all different files)
Sequential: T023 (after T020–T022 complete)
```

---

## Implementation Strategy

### MVP First (US1 + US2 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002, T003)
3. Complete Phase 3: US1 — ceiling + demand signal (T004–T007)
4. **STOP and VALIDATE**: Confirm recruiting_demand KPI appears and chart renders
5. Complete Phase 4: US2 — experienced hire fill (T008–T010)
6. **STOP and VALIDATE**: Confirm senior vs. junior WEI difference at year 10

### Incremental Delivery

- Add US3 (Graduated Retirement) → test retirement spread
- Add US4 (EC Pipeline) → test cohort-type outturn timing
- Add US5 (Grade Snapshots) → test grade breakdown in Demographics tab
- Polish phase → consistency and documentation

### Notes

- [P] tasks = different files or independent functions; no file-level dependency
- Every simulation.py change must be tested with `streamlit run app.py` to confirm no import errors
- `PYTHONUTF8=1 streamlit run app.py` required on this machine
- Commit after each phase or logical group using conventional commit messages
- Stop at each checkpoint before moving to the next phase
