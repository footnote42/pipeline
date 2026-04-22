# Feature Specification: Enhanced Workforce Simulation Model

**Feature Branch**: `001-simulation-enhancements`
**Created**: 2026-04-21
**Status**: Draft
**Input**: User description: model enhancements covering experienced hire backfill, extended
retirement, Early Careers programme pipeline, grade structure, headcount ceiling, and recruiting
market modelling.

---

## User Scenarios & Testing

### User Story 1 — Headcount Ceiling and Recruiting Demand Signal (Priority: P1)

A workforce planner runs a projection and immediately sees whether natural inflow (Early Careers
outturn) is sufficient to hold the workforce at the financial headcount ceiling. Where inflow falls
short, the tool shows how many experienced hires are needed per year to close the gap.

**Why this priority**: The core question the tool must answer is "can we sustain headcount?" —
without this signal the model cannot support hiring decisions.

**Independent Test**: Given a scenario where attrition exceeds EC outturn, the simulation output
MUST show a positive recruiting demand figure (unfilled roles) each year without any experienced
hires configured. Adding experienced hires up to the ceiling MUST reduce recruiting demand to zero.

**Acceptance Scenarios**:

1. **Given** attrition of 8% per year and EC outturn of 50 joiners per year against a ceiling of
   1,100, **When** the projection runs, **Then** a "Recruiting demand" metric is shown per year,
   calculated as: (ceiling − (survivors + EC outturn)).
2. **Given** a headcount ceiling of 1,100, **When** the workforce falls below the ceiling due to
   attrition and insufficient inflow, **Then** the gap is displayed as unfilled roles — the model
   does NOT auto-fill silently; the planner controls experienced hire inputs separately.
3. **Given** experienced hire inputs are set to zero, **When** the projection runs, **Then**
   recruiting demand equals the full gap between ceiling and natural inflow.

---

### User Story 2 — Experienced Hire Backfill Scenarios (Priority: P1)

A workforce planner models the experience impact of different hiring strategies for backfilling
leavers: junior market hires (lower grade, less service), mid-career hires, or senior lateral
moves. Each strategy produces a different WEI trajectory.

**Why this priority**: Experienced hire profile is the primary lever a business has to counteract
WEI decline; without it the model cannot evaluate the most important management response.

**Independent Test**: Configuring "senior" experienced hire profile against a "junior" profile,
with the same hire count, MUST produce a measurably higher WEI at year 5. Both scenarios MUST
maintain headcount at or below the ceiling.

**Acceptance Scenarios**:

1. **Given** a configured experienced hire profile (seniority tier: junior / mid / senior,
   each with a defined age range and grade mapping), **When** the projection runs, **Then**
   experienced hires are added to the workforce each year at the specified age and grade, up to the
   number required to meet the ceiling.
2. **Given** a "moderate" recruiting market (fill rate 70%), **When** the projection runs, **Then**
   only 70% of the gap is filled by experienced hires; the remaining 30% is shown as unfilled
   demand.
3. **Given** three market strength presets (strong = 100% fill, moderate = 70%, weak = 40%),
   **When** a planner switches between them, **Then** WEI and headcount outputs change accordingly
   with the gap metric reflecting actual fills vs. demand.

---

### User Story 3 — Extended and Graduated Retirement Modelling (Priority: P2)

A workforce planner sees retirement exits spread realistically across ages from the threshold
(default 60) into the mid-70s, with probability increasing with age. There is no cliff-edge at
any single year.

**Why this priority**: The existing hard-cutoff approach misrepresents actual exit behaviour for
the oldest cohort, which affects WEI accuracy at long projection horizons.

**Independent Test**: With a population of 50 employees aged 62–72, running a 10-year projection
MUST show gradual exits across all age bands 62–75; no single year MUST account for more than 50%
of the cohort exiting via retirement.

**Acceptance Scenarios**:

1. **Given** a retirement threshold age (default 60) and a maximum modelled retirement age of 75,
   **When** a year is simulated, **Then** each employee above threshold age is subject to a
   probability of retirement that increases monotonically with age, reaching near-certainty (≥95%)
   by age 75.
2. **Given** an employee aged 71, **When** the retirement proxy is applied, **Then** the
   probability applied MUST be materially higher than for an employee aged 62.
3. **Given** retirement proxy parameters are adjustable (threshold age, maximum retirement age),
   **When** a planner adjusts the threshold or maximum age, **Then** the retirement exit pattern
   shifts accordingly across the projection horizon.

---

### User Story 4 — Early Careers Programme Pipeline (Priority: P2)

A workforce planner configures three cohort types — L3 apprentice, L6 apprentice, graduate —
each with its own annual intake, programme length, dropout rate, and outturn grade/job family.
The tool shows how much of the annual inflow to the substantive workforce comes from each cohort.

**Why this priority**: EC outturn is the primary natural inflow; modelling it as a single
undifferentiated stream misrepresents the timing (4 vs 2 year programmes) and grade profile of
joiners.

**Independent Test**: Configuring L3 intake of 20, L6 intake of 15, graduate intake of 25, with
dropout rates of 10%, 5%, 5% respectively, MUST produce correct per-cohort outturn at years 2
(graduates) and 4 (apprentices). WEI impact of graduate outturn (higher starting grade) MUST be
measurably higher than L3 outturn for the same intake count.

**Acceptance Scenarios**:

1. **Given** L3 apprentice cohort (4-year programme, outturn at A1), **When** Year 4 is
   reached, **Then** survivors (intake minus dropouts) join the substantive workforce at A1
   grade and age ~21.
2. **Given** L6 apprentice cohort (4-year programme, outturn at B1), **When** Year 4 is
   reached, **Then** survivors join at B1 grade and are distinguished from L3 outturn in
   summary outputs.
3. **Given** graduate cohort (2-year programme, outturn at B1), **When** Year 2 is reached,
   **Then** survivors join at B1 grade.
4. **Given** a dropout rate of 10% per year for a cohort, **When** the programme runs, **Then**
   10% of active participants are removed each year (compounding); they do not contribute to
   outturn headcount.
5. **Given** any EC cohort dropout, **When** the headcount calculation runs, **Then** dropouts
   are removed from the in-programme population only and do NOT count toward the substantive
   workforce or recruiting demand.

---

### User Story 5 — Grade-Aware Population Snapshot (Priority: P3)

A workforce planner can see a workforce breakdown by grade band (A1, A2, B1, B2, C1, C2, D) in
snapshot outputs, so experience concentration at each level is visible.

**Why this priority**: Grade-level visibility enables early detection of "missing middle" effects
where experience loss is concentrated at specific levels. Lower priority because the core WEI
signal already captures aggregate experience; grade breakdown is supporting context.

**Independent Test**: A projection run with known grade composition at t=0 MUST produce per-grade
headcount snapshots at each year that correctly reflect outturn (joining at A1–B2) and attrition
(distributed across all grades).

**Acceptance Scenarios**:

1. **Given** a workforce with employees across all grade bands, **When** a year is projected,
   **Then** the snapshot output includes a per-grade headcount breakdown.
2. **Given** experienced hire profile set to "senior" (C1–C2), **When** hires are added,
   **Then** the grade snapshot shows an increase in C-grade headcount.

---

### Edge Cases

- What happens if EC intake is set to zero for all cohort types? The model MUST show full
  recruiting demand equal to total annual exits.
- What happens if the headcount ceiling is set below the current population? The model MUST flag
  this as a misconfiguration and prevent the projection from running.
- What if dropout rate is set to 100%? No outturn from that cohort; recruiting demand increases
  accordingly.
- What if retirement threshold is set above 75 (max modelled age)? The retirement curve MUST
  deactivate gracefully and produce zero retirement exits.
- What if experienced hire count would push headcount above ceiling? The model MUST cap hires at
  the ceiling; surplus demand is shown as zero.

---

## Requirements

### Functional Requirements

- **FR-001**: The simulation MUST support a configurable headcount ceiling parameter representing
  the financial headcount cap for the P&A sub-function.
- **FR-002**: Each simulation year MUST calculate and output a "recruiting demand" figure: the
  number of additional experienced hires required to bring headcount to the ceiling after natural
  inflow and Early Careers outturn.
- **FR-003**: The simulation MUST support an experienced hire backfill parameter with three
  seniority presets (junior, mid, senior), each defining an age range and grade band for incoming
  hires.
- **FR-004**: Experienced hire volume MUST be determined by recruiting market strength (strong =
  full gap filled; moderate = 70% of gap filled; weak = 40% of gap filled), configurable as a
  scenario parameter.
- **FR-005**: Experienced hires MUST be added to the workforce after attrition and EC outturn in
  the simulation step order, and MUST NOT push headcount above the ceiling.
- **FR-006**: Retirement probability MUST be modelled as a graduated function of age, beginning
  above a configurable threshold age and increasing monotonically to near-certainty (≥95%) by
  age 75. There MUST be no hard single-age cutoff.
- **FR-007**: Retirement exits MUST remain mutually exclusive with attrition exits in the same
  simulation year (no double-counting; consistent with AS-206).
- **FR-008**: The simulation MUST model three Early Careers cohort types independently: L3
  apprentice (4-year programme, A1 outturn), L6 apprentice (4-year programme, B1 outturn),
  graduate (2-year programme, B1 outturn).
- **FR-009**: Each EC cohort type MUST support a configurable annual intake count and annual
  dropout rate. Dropouts are removed from the in-programme population each year and do not
  contribute to substantive workforce headcount.
- **FR-010**: EC programme participants MUST NOT appear in the substantive workforce headcount or
  WEI calculation until they complete their programme and survive dropout.
- **FR-011**: The data model MUST support the grade structure A1, A2, B1, B2, C1, C2, D at the
  employee level. Simulation outputs MUST include per-grade headcount in annual snapshots.
- **FR-012**: All new simulation parameters (headcount ceiling, experienced hire profile, market
  strength, EC cohort intakes and dropout rates, retirement curve) MUST be adjustable via the
  existing sidebar controls without modifying the underlying data file.
- **FR-013**: The simulation summary output MUST include: WEI trend, headcount vs. ceiling trend,
  recruiting demand per year, EC outturn by cohort type per year.

### Key Entities

- **Workforce Member** (updated): ID, Age, Service, Grade (A1/A2/B1/B2/C1/C2/D), Job_Family.
  Grade_Score is derived from Grade mapping for WEI computation.
- **EC Cohort Programme**: Type (L3 / L6 / Graduate), Programme length (years), Annual intake,
  Annual dropout rate, Outturn grade band, Participants by programme year.
- **Simulation Parameters** (extended): Headcount ceiling, Attrition rate, Retirement threshold
  age, Retirement curve steepness, EC cohort intakes and dropout rates, Experienced hire profile
  (seniority tier), Recruiting market strength, Projection horizon.
- **Simulation Output** (extended): Year, Headcount, WEI, Headcount ceiling gap (recruiting
  demand), Experienced hires added, EC outturn by type, Per-grade headcount snapshot.

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: A planner can identify the annual recruiting demand in headcount units for any
  scenario within one projection run, without manual calculation.
- **SC-002**: Switching between strong, moderate, and weak recruiting market presets produces
  measurably different WEI outcomes at year 10 (at least 5% WEI spread between strong and weak
  for a representative scenario).
- **SC-003**: Retirement exits are distributed across multiple age bands above threshold; no
  single projection year removes more than 50% of the oldest cohort via retirement alone.
- **SC-004**: EC outturn from graduate cohort (higher starting grade) produces a higher WEI
  contribution per joiner than L3 outturn for equivalent intake counts — verifiable by comparing
  WEI at year 5 with matching inputs.
- **SC-005**: All new parameters are accessible and adjustable from the sidebar; no data file
  changes are required to run any of the new scenarios.
- **SC-006**: Per-grade headcount snapshots are present in simulation output and correctly reflect
  the configured experienced hire seniority tier.

---

## Assumptions

- **Experienced hire profile**: Hires are modelled at the cohort level using a seniority preset,
  not matched one-for-one to individual leavers. Junior preset: age_mid 31 (sd 4), grade A2.
  Mid preset: age_mid 38 (sd 6), grade B2. Senior preset: age_mid 47 (sd 7), grade C1. These
  defaults are configurable and will be documented in the assumptions register.
- **Headcount ceiling behaviour**: The ceiling is a hard cap; experienced hires auto-fill up to
  the ceiling based on market strength, but the planner sets market strength as a scenario input.
  The model does not auto-optimise hires — it shows consequences of configured market assumptions.
- **Grade-to-Grade_Score mapping**: A1=1, A2=2, B1=3, B2=4, C1=5, C2=6, D=7. This mapping
  drives WEI; it is a sensible default and can be revised via constitution amendment.
- **Job-family grade constraints** (A1–B2 for vocational; B2–D for engineering) are noted as a
  future modelling refinement. They are out of scope for this iteration and will not be enforced
  in the simulation logic.
- **EC participants and headcount ceiling**: In-programme EC participants are NOT counted against
  the headcount ceiling. Only substantive employees count.
- **Dropout timing**: Dropouts are removed at the end of each programme year, after the year
  begins. They are not replaced mid-year.
- **Design refresh** (user point 7): UI/visual design improvements via Impeccable skills are
  treated as a concurrent but separate workstream. This spec covers functional simulation
  behaviour only; visual design changes will be addressed via a separate `/impeccable` session.
- **Existing CSV format**: The current `sample_workforce.csv` uses `Grade_Score` as a float.
  This enhancement requires a `Grade` column (A1–D). A migration path for existing CSV files
  (inferring grade from Grade_Score) will be handled during implementation.

