# Quickstart: Enhanced Workforce Simulation Model

**Branch**: `001-simulation-enhancements` | **Date**: 2026-04-21

---

## Running the App

```bash
PYTHONUTF8=1 streamlit run app.py
```

The app loads `data/sample_workforce.csv` by default. Upload a custom CSV via the sidebar.

---

## Testing New Features

### 1. Headcount Ceiling and Recruiting Demand

1. Run the app.
2. Open the **Headcount Ceiling** expander in the sidebar.
3. Set ceiling to a value slightly below current headcount (e.g., 1,050).
   → Expect: `ValueError` message shown in the app ("Ceiling below current population").
4. Set ceiling to 1,100 (equal to population).
5. Open the **Experienced Hires** expander and set market strength to "weak".
6. Run projection.
   → Expect: "Recruiting demand" metric shows a positive value each year where EC outturn
   cannot replace attrition losses. Headcount chart shows gap between ceiling and actual.

### 2. Experienced Hire Profiles

1. Set ceiling to 1,100, market strength to "strong".
2. Compare "junior" vs. "senior" hire profiles across a 10-year projection.
   → Expect: Senior profile produces higher WEI at year 10. Both maintain headcount at ceiling.

3. Keep profile as "senior". Switch market strength from "strong" to "weak".
   → Expect: WEI at year 10 is at least 5% lower under weak market than under strong market
   (SC-002). Recruiting demand metric rises as fewer hires fill the gap.

### 3. Early Careers Pipeline

1. Open the **Early Careers** expander.
2. Set L3 intake = 20, L6 intake = 10, Graduate intake = 15.
3. Set all dropout rates to 0%.
4. Run a 10-year projection.
   → Expect: Zero EC outturn in years 1–3 (pipeline filling). First outturn at year 2 from
   Graduate cohort. First outturn at year 4 from both apprentice cohorts.

5. Set L3 dropout to 20%.
   → Expect: ~65% of the original L3 cohort outurns at year 4 (0.8^4 ≈ 0.41 would be
   correct for fully compounding; but it's 0.8 per year over 4 years = 0.41 × intake).
   Verify EC outturn by cohort type in the output metrics.

### 4. Graduated Retirement

1. Open the **Retirement** expander.
2. Set threshold age = 60, max retirement age = 75.
3. Run a 20-year projection against a population with employees aged 55–70.
   → Expect: Retirement exits spread across years; no single year has a mass exit of the
   oldest cohort. Oldest employees (age 74+) exit with near-100% probability.

### 5. Backward Compatibility

1. Upload `data/sample_workforce.csv` (uses float `Grade_Score`, no `Grade` column).
   → Expect: App runs without error; all existing features work as before.

---

## Accepted CSV Formats

**Format A — existing (Grade_Score float)**:
```
ID,Age,Service,Grade_Score,Job_Family
EMP001,46,23,9.0,Engineering
```

**Format B — new (Grade string)**:
```
ID,Age,Service,Grade,Job_Family
EMP001,46,23,C2,Engineering
```

Both formats are accepted. If both columns are present, `Grade` takes precedence.

---

## Key Metrics to Check

After a projection run:

| Metric | Location | What to verify |
|--------|----------|----------------|
| WEI trend | Executive Summary tab | Senior hires → higher WEI than junior hires |
| Recruiting demand | KPI row | Positive when market is weak / EC outturn low |
| Headcount vs. ceiling | Demographics tab | Headcount line should not exceed ceiling |
| EC outturn by type | Assumptions tab | Outturn appears at correct year (2 for Grad, 4 for L3/L6) |
| Grade snapshot | Demographics tab | Grade distribution shifts per hire profile |
