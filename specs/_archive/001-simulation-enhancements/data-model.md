# Data Model: Enhanced Workforce Simulation Model

**Branch**: `001-simulation-enhancements` | **Date**: 2026-04-21

---

## Constants (simulation.py)

```python
GRADE_SCORE_MAP = {'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5, 'C2': 6, 'D': 7}

GRADE_LABELS = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'D']

EC_COHORT_DEFAULTS = {
    'L3': {
        'programme_years': 4,
        'outturn_grade': 'A1',        # Grade_Score = 1
        'outturn_age': 21,
        'outturn_service': 4,
    },
    'L6': {
        'programme_years': 4,
        'outturn_grade': 'B1',        # Grade_Score = 3
        'outturn_age': 22,
        'outturn_service': 4,
    },
    'Grad': {
        'programme_years': 2,
        'outturn_grade': 'B1',        # Grade_Score = 3
        'outturn_age': 23,
        'outturn_service': 2,
    },
}

EXP_HIRE_PRESETS = {
    'junior': {'age_mid': 31, 'age_sd': 4, 'grade': 'A2', 'grade_score': 2},
    'mid':    {'age_mid': 38, 'age_sd': 6, 'grade': 'B2', 'grade_score': 4},
    'senior': {'age_mid': 47, 'age_sd': 7, 'grade': 'C1', 'grade_score': 5},
}

MARKET_STRENGTH_PRESETS = {
    'strong':   1.00,
    'moderate': 0.70,
    'weak':     0.40,
}

RETIREMENT_MAX_AGE_DEFAULT = 75
```

---

## Core Data Structures

### Workforce DataFrame (simulation.py)

Passed between simulation steps as a pandas DataFrame. All columns are present at all times.

| Column | Type | Source | Notes |
|--------|------|--------|-------|
| `ID` | str | CSV / generated | Unique employee ID; new hires receive generated IDs |
| `Age` | float | CSV / updated | Incremented by 1 each simulation year |
| `Service` | float | CSV / updated | Incremented by 1 each simulation year |
| `Grade_Score` | float | Derived or CSV | Derived from `Grade` via `GRADE_SCORE_MAP`; or raw float from CSV |
| `Grade` | str | CSV / assigned | Optional column — A1, A2, B1, B2, C1, C2, D; added for new hires |
| `Job_Family` | str | CSV / assigned | Job family string |

**Column detection logic** (in `load_workforce`):
- `Grade` present → compute `Grade_Score` from `GRADE_SCORE_MAP`; unknown grades raise `ValueError`
- `Grade` absent, `Grade_Score` present → use raw float; `Grade` column added as empty string
- Neither present → raise `ValueError`

---

### EC Cohort State

Tracked in `run_projection` as a local dict. Not stored in the workforce DataFrame.

```python
ec_state: dict[str, list[float]]
# Keys: 'L3', 'L6', 'Grad'
# Values: list of length == programme_years for that cohort type
# Index 0: most recently enrolled (year 1 of programme)
# Last index: graduating cohort (year programme_years of programme)
# Initial value: [0.0, 0.0, ...] (empty pipeline at t=0)
```

Example after 2 years with L3 intake=20:
```python
{'L3': [20.0, 20.0, 0.0, 0.0], 'L6': [0.0, 0.0, 0.0, 0.0], 'Grad': [0.0, 0.0]}
```

---

### Simulation Parameters (run_projection arguments)

Extended keyword arguments added to `run_projection`. All have defaults for backward
compatibility with existing callers.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `years` | int | 10 | Projection horizon |
| `attrition_rate` | float | 0.05 | Annual flat attrition rate (0–1) |
| `retirement_threshold` | int | 60 | Age above which retirement probability begins |
| `retirement_max_age` | int | 75 | Age at which retirement probability reaches 1.0 |
| `retirement_base_prob` | float | 0.05 | Probability at threshold age |
| `annual_intake` | int | 0 | Legacy EC intake (deprecated; use `ec_config`) |
| `ec_config` | dict | see below | EC cohort configuration dict |
| `ceiling` | int | None | Headcount ceiling; None disables ceiling logic |
| `exp_hire_profile` | str | 'mid' | Experienced hire preset: 'junior', 'mid', 'senior' |
| `market_strength` | str | 'moderate' | Recruiting market: 'strong', 'moderate', 'weak' |
| `seed` | int | 42 | RNG seed for reproducibility |

**`ec_config` default structure**:
```python
{
    'L3':   {'intake': 0, 'dropout_rate': 0.0},
    'L6':   {'intake': 0, 'dropout_rate': 0.0},
    'Grad': {'intake': 0, 'dropout_rate': 0.0},
}
```

---

### Simulation Output (run_projection return dict)

Extended return value. Existing keys are preserved; new keys are additive.

| Key | Type | Description |
|-----|------|-------------|
| `wei_series` | list[float] | WEI per year (existing) |
| `headcount` | list[int] | Substantive workforce headcount per year (existing) |
| `snapshots` | list[DataFrame] | Full workforce DataFrame per year (existing) |
| `age_bands` | list[dict] | Age-band breakdown per year (existing) |
| `recruiting_demand` | list[float] | Unfilled roles per year (new) |
| `experienced_hires_added` | list[float] | Experienced hires added per year (new) |
| `ec_outturn` | dict[str, list[float]] | Per-cohort-type outturn per year (new) |
| `grade_snapshots` | list[dict] | Per-grade headcount per year (new) |

**`grade_snapshots` entry format**:
```python
{'A1': 45, 'A2': 120, 'B1': 310, 'B2': 280, 'C1': 180, 'C2': 90, 'D': 15}
```

---

## Entity Relationships

```
run_projection(df, **params)
    │
    ├── reads: df (Workforce DataFrame — each employee row)
    ├── reads: ec_config → manages: ec_state (EC Cohort State)
    ├── reads: ceiling, exp_hire_profile, market_strength
    │
    ├── per-year calls:
    │   ├── _age_service_step(df) → df
    │   ├── _apply_attrition(df, rate, rng) → df
    │   ├── _apply_retirement_proxy(df, threshold, base_prob, max_age, rng) → df
    │   ├── _advance_ec_pipeline(ec_state, ec_config) → (ec_state, outturn_rows_dict)
    │   ├── _apply_ec_outturn(df, outturn_rows_dict) → df
    │   ├── _apply_experienced_hires(df, ceiling, profile, market_strength, rng) → (df, hires_added, demand)
    │   └── compute_wei(df, baseline) → float
    │
    └── returns: result dict (all output keys above)
```

---

## Validation Rules

- `ceiling` MUST be ≥ 1 if provided; MUST NOT be less than current population (raises
  `ValueError` with message: "Headcount ceiling ({n}) is below current population ({m})")
- `retirement_threshold` MUST be < `retirement_max_age`
- `dropout_rate` for any EC cohort MUST be in [0, 1)
- `market_strength` string MUST be a key in `MARKET_STRENGTH_PRESETS`
- `exp_hire_profile` string MUST be a key in `EXP_HIRE_PRESETS`
- Grade values in `Grade` column MUST be keys in `GRADE_SCORE_MAP`

---

## Migration Notes

Existing `data/sample_workforce.csv` has `Grade_Score` as a float column. No changes to this
file are needed. The app continues to work as before; the `Grade` column is optional.

To upgrade a CSV to the grade-aware format: add a `Grade` column with values from
`{A1, A2, B1, B2, C1, C2, D}` and remove or leave the `Grade_Score` column (it will be
overwritten if `Grade` is present).
