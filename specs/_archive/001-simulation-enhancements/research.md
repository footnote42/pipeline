# Research: Enhanced Workforce Simulation Model

**Branch**: `001-simulation-enhancements` | **Date**: 2026-04-21
**Derived from**: Phase 0 of `plan.md`

---

## 1. Retirement Curve Design

**Decision**: Linear probability ramp from `base_prob` at `threshold_age` to `1.0` at
`max_retirement_age` (default 75). Clamped to [0, 1].

**Formula**:
```
p(age) = 0                           if age < threshold_age
p(age) = base_prob + (1 - base_prob)
         × (age - threshold_age)
         / (max_retirement_age - threshold_age)   if threshold_age ≤ age ≤ max_retirement_age
p(age) = 1.0                         if age > max_retirement_age
```

**Rationale**: Stakeholders can understand "probability increases from X% at 60, reaching
certainty at 75" without statistical training. The linear shape is not the most realistic
(empirically a sigmoid fits better) but matches the explainability requirement of the model
(proportionate claims per AS-507). Two configurable parameters (threshold, max_age) are
sufficient for all modelled scenarios.

**Alternatives considered**:
- *Logistic (sigmoid)*: More realistic shape, but introduces a steepness parameter that is
  difficult to explain to non-technical owners. Rejected for this iteration.
- *Piecewise linear (two segments)*: Allows a slow-start, fast-finish shape. Additional
  complexity not justified for first proof-of-concept. Noted as future option.
- *Hard cutoff*: Existing approach — rejected as it concentrates exits in one year and
  misrepresents actual behaviour at long horizons.

**Mutually exclusive with attrition (AS-206)**: The retirement check is applied only to
attrition survivors, identical to the current implementation. No double-counting.

---

## 2. EC Cohort Pipeline Tracking

**Decision**: Per-cohort-type rolling array (`list[float]`) of length `programme_years`.
Index 0 holds the most recently enrolled cohort; the last index holds the graduating cohort.

**Algorithm per simulation year**:
```python
def _advance_ec_pipeline(pipeline, annual_intake, dropout_rate, programme_years):
    # 1. Apply annual dropout to each year-in-programme
    pipeline = [count * (1 - dropout_rate) for count in pipeline]
    # 2. Outturn: graduating cohort completes programme
    outturn = pipeline[-1] if len(pipeline) == programme_years else 0.0
    # 3. Advance: shift older cohorts toward graduation
    pipeline = pipeline[:-1]   # remove graduating cohort
    # 4. Enrol new intake at front
    pipeline = [float(annual_intake)] + pipeline
    return pipeline, outturn
```

Initial state: all pipeline slots = 0.0 (empty; fills over first `programme_years` years).

**Rationale**: Pure-function approach — no external state or class required. Compatible with
the existing stateless simulation design. Dropout compounds correctly (each year's survivors
face the same rate). Outturn in years 1 and 2 (before pipeline fills) is zero, which correctly
reflects that no cohort has yet completed the programme.

**Three cohort types**:

| Type | Programme years | Default outturn grade | Age at outturn |
|------|-----------------|-----------------------|----------------|
| L3 apprentice | 4 | A1 (Grade_Score 1) | ~21 |
| L6 apprentice | 4 | B1 (Grade_Score 3) | ~21–23 |
| Graduate | 2 | B1 (Grade_Score 3) | ~23–24 |

Starting age and starting service at outturn are fixed per cohort type and set as constants.
Outturn grade is configurable (sidebar) with the above as defaults.

**EC participants not in substantive headcount**: Pipeline counts are tracked separately from
the main workforce DataFrame. Participants do not appear in WEI, age band, or headcount metrics
until they outturn and are added as new rows.

---

## 3. Experienced Hire Backfill

**Decision**: Three seniority presets, each defining a (age_mid, age_sd, grade) distribution.
Hires are sampled with age drawn from a truncated normal centred on `age_mid` with `age_sd`,
grade fixed to preset grade.

**Presets**:

| Preset | Label | Age range (approx) | Grade |
|--------|-------|-------------------|-------|
| junior | "Junior market hire" | 27–35 | A2 (score 2) |
| mid | "Mid-career hire" | 32–45 | B2 (score 4) |
| senior | "Senior lateral move" | 40–55 | C1 (score 5) |

**Service at hire**: Set to `age − 22` as a default approximation (assumes professional
working life from age 22). This gives reasonable Grade_Score × Service contribution without
requiring a separate service assumption.

**Volume**: `hires_added = min(gap, round(gap × market_strength_fill_rate))` where gap is the
shortfall between ceiling and (post-attrition/retirement + EC outturn) headcount.

**Market strength presets**:

| Label | Fill rate |
|-------|-----------|
| Strong | 1.00 (100% of gap filled) |
| Moderate | 0.70 |
| Weak | 0.40 |

**Rationale**: Presets avoid requiring owners to specify individual hire characteristics.
Age range is realistic for each seniority level (junior = recent graduates / early movers;
mid = established professionals; senior = experienced leaders). Service approximation is
transparent and documented in assumptions register.

**Alternatives considered**:
- *Match leaver profile*: Would require tracking individual leaver characteristics to mirror
  in the hire. Adds complexity without clarity; leavers are sampled stochastically so the
  "mirror" would be noisy. Rejected.
- *Fully configurable age/grade sliders*: Too many parameters for a presentation-ready sidebar.
  Rejected for first iteration.

---

## 4. Headcount Ceiling Algorithm

**Decision**: Closed-loop ceiling with market-strength-limited fill. Per-year order:

```
1. age + 1, service + 1
2. attrition exits
3. retirement exits (on attrition survivors)
4. ec_outturn → add rows to workforce DataFrame
5. gap = ceiling − len(workforce)
6. hires = min(max(gap, 0), round(gap × market_fill_rate))
7. add `hires` rows at experienced hire preset profile
8. recruiting_demand = max(0, gap − hires)
9. compute WEI, headcount, age bands, grade snapshot
```

If `gap ≤ 0` (workforce at or above ceiling), steps 5–8 produce zero hires and zero demand.
If ceiling is set below initial headcount, `load_workforce` raises a `ValueError` with a
descriptive message.

**Rationale**: Closed-loop is consistent with the user's stated intent ("maintain the headcount
at the ceiling"). Market strength determines how much of the gap can realistically be filled.
The residual gap is the actionable output: it tells the planner how many roles remain unfilled
under the configured market assumption.

---

## 5. Sidebar Organisation

**Decision**: Group new parameters into `st.expander` sections. Attrition section remains
visible by default; all new sections start collapsed.

**Proposed sidebar layout**:

```
[Attrition]  (expanded by default)
  Annual attrition rate

[Retirement]  (collapsed)
  Threshold age
  Maximum retirement age

[Early Careers]  (collapsed)
  L3 intake / dropout rate
  L6 intake / dropout rate
  Graduate intake / dropout rate

[Experienced Hires]  (collapsed)
  Seniority profile (junior / mid / senior)
  Recruiting market (strong / moderate / weak)

[Headcount Ceiling]  (collapsed)
  Ceiling (number)

[Projection]  (collapsed)
  Projection horizon (years)
```

**Rationale**: Expanders keep the default view uncluttered for quick scenario runs. Power users
can expand relevant sections. Section naming is plain English, appropriate for non-technical
users.

---

## 6. Grade Column and Backward Compatibility

**Decision**: `load_workforce` detects column presence in this order:
1. If `Grade` column present: derive `Grade_Score` via `GRADE_SCORE_MAP` constant
2. If only `Grade_Score` present: use raw float (existing behaviour)
3. If neither present: raise `ValueError` listing required alternatives

`GRADE_SCORE_MAP`: `{'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5, 'C2': 6, 'D': 7}`

**Rationale**: Existing `data/sample_workforce.csv` uses `Grade_Score` float. No change needed
to use the app after this enhancement. New CSVs with a `Grade` column (A1–D strings) use the
discrete mapping. The two approaches coexist cleanly. Documented in assumptions register as
default Grade_Score mapping.
