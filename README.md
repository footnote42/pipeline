# pipeline

Workforce scenario modelling tool for headcount projection, experience erosion analysis, and recruiting demand planning. Built as a decision-support instrument for engineering workforce planning in complex organisations.

## What it does

Pipeline models a workforce population forward year-by-year and tracks whether the organisation is gaining or losing aggregate experience and capability. The core question it answers is: **if current attrition, retirement, and intake patterns continue, when does the workforce experience profile cross a meaningful threshold — and what would it take to prevent that?**

The tool runs stochastic year-on-year simulations across a configurable horizon (up to 20 years) and produces a Weighted Experience Index (WEI) trend, headcount waterfall, age-band distribution shifts, grade structure snapshots, and recruiting demand forecasts.

Built to support a real workforce planning brief: projecting a ~1,100-person engineering sub-function using live Workday extract data, with outputs structured for restricted management-information use and senior stakeholder challenge.

## The modelling approach

### Weighted Experience Index (WEI)

The WEI is the primary output metric:

```
WEI = sum(Grade_Score_i × Service_i) / baseline_numerator
```

Where `baseline_numerator` is the same sum computed at t=0. The WEI starts at 1.0 and tracks relative to the current profile — it does not require a theoretical ideal or externally calibrated target. A WEI below 0.85 triggers a tipping-point warning: the aggregate experience stock has eroded by more than 15% from where it is today.

The WEI formula is isolated in a single function (`compute_wei_numerator` in `simulation.py`) so the index definition can be changed without touching simulation logic.

### Simulation order (per year)

Each simulated year applies steps in this sequence:

1. **Age and service increment** — all employees age by one year
2. **Attrition** — flat annual probability applied stochastically
3. **Retirement proxy** — graduated curve from a threshold age to a maximum age; applies to attrition survivors to avoid double-counting
4. **Early Careers outturn** — L3 apprentice, L6 apprentice, and Graduate cohort pipelines advance; completers join the workforce at a defined grade
5. **Experienced hires** — if a headcount ceiling is set, the gap is filled with lateral hires at a configured seniority profile, throttled by a market strength multiplier
6. **Metrics snapshot** — WEI, headcount, age-band distribution, and grade breakdown are recorded

## Inputs

A workforce CSV with these required columns:

| Column | Description |
|--------|-------------|
| `ID` | Unique employee identifier |
| `Age` | Age in years (integer) |
| `Service` | Years of service |
| `Job_Family` | Functional grouping |
| `Grade` or `Grade_Score` | Grade label (A1–D) or numeric score |

A built-in sample dataset of ~1,100 synthetic employees is included at `data/sample_workforce.csv`.

## Scenario controls

All parameters are adjustable via the sidebar at runtime:

| Control | Range | Default |
|---------|-------|---------|
| Annual attrition rate | 1–25% | 6% |
| Retirement threshold age | 55–68 | 60 |
| Retirement max age (100% exit) | 65–80 | 75 |
| L3 apprentice annual intake | 0–200 | 0 |
| L6 apprentice annual intake | 0–200 | 0 |
| Graduate annual intake | 0–200 | 50 |
| Early Careers dropout rate | 0–50% | 10% |
| Experienced hire seniority profile | junior / mid / senior | mid |
| Recruiting market strength | weak / moderate / strong | moderate |
| Headcount ceiling | 500+ | 1,100 |
| Projection horizon | 5–20 years | 10 |

## Outputs

**Executive Summary tab** — WEI trend chart with tipping-point threshold band, headcount waterfall, recruiting demand vs hires, tipping-point year and WEI value

**Demographics tab** — grade distribution snapshot, age-band grouped bar comparison across selected years, summary table with heat-map gradient

**Assumptions tab** — full assumptions register with sensitivity ratings and governance reference IDs, year-by-year scenario summary

## Running it

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app loads the sample dataset automatically. Upload a real workforce CSV via the sidebar file uploader.

## Architecture

Three-file structure with strict separation of concerns:

- `simulation.py` — pure computation, no Streamlit dependency. WEI formula lives in `compute_wei_numerator`; replace only that function to redefine the index
- `charts.py` — Plotly figure builders; each function returns a `go.Figure`
- `app.py` — Streamlit entry point; owns sidebar controls, session state, KPI metrics, and tab layout

Dependencies: `streamlit>=1.32.0`, `pandas>=2.0.0`, `numpy>=1.26.0`, `plotly>=5.20.0`

## Governance

Outputs are **Restricted Management Information** until method credibility and data credibility are confirmed by the designated owners. The assumptions register tab makes this explicit. Do not share outputs more widely without approval.

`data/EmpNumbers.csv` — real workforce extract data, not committed to this repository.
