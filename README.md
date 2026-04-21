# Pipline — Workforce Experience Scenario Model

A Streamlit app for projecting workforce age and experience profiles over time, using the
Weighted Experience Index (WEI) as the primary tipping-point measure.

Built for business operations managers and people analytics leads in the P&A sub-function.

---

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app loads `data/sample_workforce.csv` (~1,100 synthetic employees) by default.
Upload your own CSV via the sidebar.

---

## Architecture

| File | Role |
|------|------|
| `simulation.py` | Pure computation — projection logic, WEI formula, no Streamlit |
| `charts.py` | Plotly figure builders — each function returns `go.Figure` |
| `app.py` | Streamlit entry point — sidebar, session state, KPI metrics, tab layout |

---

## CSV Format

Your workforce file must include these columns:

| Column | Type | Description |
|--------|------|-------------|
| `ID` | string | Unique employee identifier |
| `Age` | integer | Current age in years |
| `Service` | float | Years of service |
| `Grade_Score` | float | Experience/seniority score |
| `Job_Family` | string | Job family grouping |

---

## Parameters

Adjusted via the sidebar at runtime:

| Parameter | Description |
|-----------|-------------|
| Annual attrition rate | Flat probability of leaving each year |
| Retirement threshold age | Age above which retirement proxy applies |
| Annual Early Careers intake | Joiners per year at Age 21, Grade_Score 1 |
| Projection horizon | Years to project forward |

---

## Weighted Experience Index (WEI)

WEI = `sum(Grade_Score × Service)` for the projected workforce, normalised to 1.0 at baseline.

A WEI below **0.85** (15% decline) is the tipping-point threshold and triggers a risk warning.

To redefine the index, swap `compute_wei_numerator` in `simulation.py`.

---

## Data Classification

Outputs are **Restricted Management Information** until method credibility and data credibility
are confirmed by the designated owners. Do not share outputs more widely without approval.
See `copilot-assumptions.md` for the full assumptions register.
