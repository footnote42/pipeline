# Contract: simulation.py Public API

**Branch**: `001-simulation-enhancements` | **Date**: 2026-04-21

This document defines the public interface of `simulation.py` after the enhancement.
`app.py` and `charts.py` MUST depend only on the functions and constants listed here.

---

## Constants

```python
AGE_BAND_LABELS: list[str]
# Ordered list of age band labels for use in charts
# ['Under 25', '25-34', '35-44', '45-54', '55-64', '65+']

REQUIRED_COLS: set[str]
# Minimum columns required in the input CSV (updated)
# Must contain 'ID', 'Age', 'Service', 'Job_Family'
# Plus either 'Grade' OR 'Grade_Score' (not both required)

GRADE_SCORE_MAP: dict[str, int]
# Mapping from grade string to numeric score
# {'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5, 'C2': 6, 'D': 7}

GRADE_LABELS: list[str]
# Ordered list for display: ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'D']

EXP_HIRE_PRESETS: dict[str, dict]
# Keys: 'junior', 'mid', 'senior'
# Each value: {'age_mid': int, 'age_sd': int, 'grade': str, 'grade_score': int}

MARKET_STRENGTH_PRESETS: dict[str, float]
# Keys: 'strong', 'moderate', 'weak'
# Values: fill rate floats (1.0, 0.7, 0.4)
```

---

## load_workforce(path: str | Path) → pd.DataFrame

Loads and validates a workforce CSV file.

**Parameters**:
- `path`: Absolute or relative path to the CSV file.

**Returns**: Validated DataFrame with columns `ID`, `Age`, `Service`, `Grade_Score`, `Grade`,
`Job_Family`. If input has `Grade` column, `Grade_Score` is computed from `GRADE_SCORE_MAP`. If
input has only `Grade_Score`, `Grade` column is added as empty string. Both are present on return.

**Raises**:
- `FileNotFoundError`: File not found at `path`.
- `ValueError`: Missing required columns (message lists which are missing).
- `ValueError`: Unknown grade values found in `Grade` column (message lists unknowns).

**Side effects**: None.

---

## run_projection(df: pd.DataFrame, \*\*kwargs) → dict

Runs a multi-year workforce projection simulation.

**Parameters** (all keyword; all have defaults for backward compatibility):

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `years` | int | 10 | Number of years to project |
| `attrition_rate` | float | 0.05 | Annual attrition probability (0–1) |
| `retirement_threshold` | int | 60 | Age at which retirement probability begins |
| `retirement_max_age` | int | 75 | Age at which retirement probability = 1.0 |
| `retirement_base_prob` | float | 0.05 | Retirement probability at `retirement_threshold` |
| `ec_config` | dict | all zeros | EC cohort configuration (see data-model.md) |
| `ceiling` | int \| None | None | Headcount ceiling; None disables ceiling logic |
| `exp_hire_profile` | str | 'mid' | Experienced hire seniority preset |
| `market_strength` | str | 'moderate' | Recruiting market strength preset |
| `seed` | int | 42 | RNG seed for reproducibility |

**Returns**: `dict` with the following keys:

| Key | Type | Description |
|-----|------|-------------|
| `wei_series` | list[float] | WEI per year (length = years) |
| `headcount` | list[int] | Substantive headcount per year |
| `snapshots` | list[pd.DataFrame] | Full workforce DataFrame per year |
| `age_bands` | list[dict] | Age-band counts per year |
| `recruiting_demand` | list[float] | Unfilled roles per year (0.0 if no ceiling) |
| `experienced_hires_added` | list[float] | Experienced hires added per year |
| `ec_outturn` | dict[str, list[float]] | Per-type outturn per year; keys 'L3', 'L6', 'Grad' |
| `grade_snapshots` | list[dict] | Per-grade headcount per year; keys A1–D |

**Raises**:
- `ValueError`: Ceiling below current population size.
- `ValueError`: `exp_hire_profile` not in `EXP_HIRE_PRESETS`.
- `ValueError`: `market_strength` not in `MARKET_STRENGTH_PRESETS`.
- `ValueError`: `retirement_threshold >= retirement_max_age`.

**Side effects**: None (pure computation — no Streamlit, no file I/O).

---

## compute_wei_numerator(df: pd.DataFrame) → float

Computes the raw WEI numerator for a workforce snapshot.

**Formula**: `sum(Grade_Score × Service)` across all rows.

**Parameters**: `df` — DataFrame with `Grade_Score` and `Service` columns.

**Returns**: float — raw WEI numerator. Normalised by baseline in `run_projection`.

**Note**: Swapping this function redefines the WEI. Changes require MAJOR constitution amendment.

---

## Internal Functions (NOT part of public API)

These functions are called only within `simulation.py`. `app.py` and `charts.py` MUST NOT
import or call them directly.

- `_age_service_step(df)` → df
- `_apply_attrition(df, rate, rng)` → df
- `_apply_retirement_proxy(df, threshold, base_prob, max_age, rng)` → df
- `_advance_ec_pipeline(ec_state, ec_config)` → (ec_state, outturn_dict)
- `_apply_ec_outturn(df, outturn_dict, next_id)` → (df, next_id)
- `_apply_experienced_hires(df, ceiling, profile_key, market_key, rng, next_id)` → (df, hires, demand, next_id)
- `compute_wei(df, baseline_numerator)` → float
- `assign_age_band(age_series)` → pd.Series

---

## charts.py New Functions

```python
def recruiting_demand_chart(
    years: list[int],
    demand: list[float],
    hires: list[float],
    scenario_name: str = ""
) -> go.Figure:
    ...

def grade_snapshot_chart(
    grade_snapshots: list[dict],
    selected_year: int
) -> go.Figure:
    ...
```

Both return `go.Figure` objects. Display logic stays in `app.py`.
