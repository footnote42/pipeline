# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
streamlit run app.py
```

The app loads `data/sample_workforce.csv` by default (~1,100 synthetic employees). Users can also upload their own CSV via the sidebar.

## Architecture

Three-file structure with strict separation of concerns:

- **`simulation.py`** — pure computation, no Streamlit. Exports `load_workforce`, `run_projection`, `AGE_BAND_LABELS`, `REQUIRED_COLS`. The WEI formula lives in `compute_wei_numerator`; swap only that function to redefine the index.
- **`charts.py`** — Plotly figure builders. Each function returns a `go.Figure`; display logic stays in `app.py`. Theme constants (`BG`, `SURFACE`, `GRID`, etc.) are defined at module level.
- **`app.py`** — Streamlit entry point. Owns sidebar controls, session state (`st.session_state.results`), KPI metrics, and tab layout. Auto-reruns the projection whenever any parameter changes.

## Key Domain Concepts

- **WEI (Weighted Experience Index):** `sum(Grade_Score × Service)` normalised to 1.0 at baseline. The tipping-point threshold is 0.85 (15% decline). Defined in `simulation.py:compute_wei_numerator`.
- **Simulation order per year:** Age+1 → Attrition → Retirement proxy → EC cohort pipeline advancement + outturn → Headcount gap calculation → Experienced hires fill (market-strength limited) → Metrics recorded (WEI, headcount, age bands, grade snapshot).
- **Required CSV columns:** `ID`, `Age`, `Service`, `Job_Family`, and either `Grade` or `Grade_Score`.

## Design

Design context is in `.impeccable.md`. Key points:
- **Palette:** Black `#1A1A1A` / White `#FFFFFF` (prime), Bright Orange `#FF5C32` / Blue `#444AFF` (secondary), Purple `#9BA0F9` / Grey `#75808B` (tertiary)
- **Fonts:** Bricolage Grotesque (headings/KPIs) + Manrope (body/labels)
- **Theme:** Light default, dark mode toggle
- Orange is reserved for risk signals and alerts — never decorative
- All CLI commands require `PYTHONUTF8=1` prefix on this machine to avoid Windows encoding crashes

## Dependencies

```
streamlit>=1.32.0
pandas>=2.0.0
numpy>=1.26.0
plotly>=5.20.0
```

Install: `pip install -r requirements.txt` (venv at `.venv/`).

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan at
`specs/001-simulation-enhancements/plan.md`
<!-- SPECKIT END -->
