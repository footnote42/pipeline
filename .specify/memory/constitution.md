<!--
SYNC IMPACT REPORT
Version change: [TEMPLATE] → 1.0.0
Modified principles: All (initial population from template placeholders)
Added sections: Core Principles (I–V), Data & Classification, Development Standards, Governance
Removed sections: N/A — template placeholders replaced
Templates requiring updates:
  ✅ .specify/templates/plan-template.md — Constitution Check section is generic; principle names now available for concrete gates
  ✅ .specify/templates/spec-template.md — no structural changes required
  ✅ .specify/templates/tasks-template.md — no structural changes required
Follow-up TODOs:
  - TODO(RATIFICATION_DATE): No prior ratification event on record; using initial adoption date 2026-04-21
-->

# Pipline Constitution

## Core Principles

### I. Separation of Concerns

Computation, visualisation, and presentation MUST remain strictly separated across three files:

- `simulation.py` MUST contain all projection and WEI logic. No Streamlit imports are permitted here.
- `charts.py` MUST contain only Plotly figure builders that return `go.Figure`. No display or state logic.
- `app.py` MUST be the sole Streamlit entry point. It owns sidebar controls, session state, KPI metrics,
  and tab layout.

No file may import from a higher layer (e.g., `charts.py` MUST NOT import from `app.py`). Expanding
beyond three files requires a recorded justification in the relevant implementation plan.

### II. Computational Integrity

The simulation MUST execute in this exact order each year:
Age+1 → Attrition → Retirement proxy → EC cohort pipeline advancement + outturn →
Headcount gap calculation → Experienced hires fill (market-strength limited) →
Metrics recorded (WEI, headcount, age bands, grade snapshot).

Deviation from this order requires explicit governance approval and an assumptions-register update.

- Retirement proxy exits MUST NOT double-count attrition exits in the same simulation year (AS-206).
- The WEI formula is authoritative. Any change to `compute_wei_numerator` constitutes a MAJOR amendment.
- WEI normalisation baseline MUST remain at 1.0 (current reference profile) unless formally re-ratified.
- The tipping-point threshold (default 0.85 — a 15% decline) MUST be surfaced as a configurable or
  documented assumption, never hardcoded silently.

### III. Assumption Transparency

All model decisions affecting projections MUST be documented in the assumptions register
(`copilot-assumptions.md` or its successor). Claims in any output MUST remain proportionate to the
scenario-based nature of the model; causal claims are prohibited unless separately evidenced (AS-507).

- Attrition, retirement proxy, WEI weightings, and Early Careers intake are owner-controlled assumptions.
  The tool MUST surface these to the user rather than embedding silent defaults.
- Scenario comparison is mandatory for all outputs. Point-forecasts MUST NOT be presented as predictions.

### IV. Presentation Readiness

Every chart and data panel MUST be screenshot-worthy at the time it is rendered. Design rules in
`.impeccable.md` are binding:

- Orange (`#FF5C32`, `#FFA851`) is reserved for risk signals, tipping points, and alerts. It MUST NOT
  be used decoratively.
- Blue (`#444AFF`) is the precision/action signal for interactive elements and primary data series.
- Typography: Bricolage Grotesque for display/headings/KPIs; Manrope for body/labels/data.
- Light mode is the default. Dark mode MUST be available via toggle.
- Crowded layouts and prototype-style elements are prohibited in the delivered interface.

### V. Simplicity and Scope Control

The tool MUST remain bounded to the P&A sub-function (~1,100 employees). Free-form modelling beyond
the agreed preset scenarios is explicitly out of scope for v1.

- YAGNI applies: do not build generalisation or extension points not required by the current scope.
- The minimum accepted output is a decision-support pack. Additional artefacts are desirable but cannot
  gate delivery.
- The three-file architecture MUST NOT be expanded without explicit justification recorded in a plan.

## Data & Classification

All workforce data originates from Workday AP reports. The following rules apply without exception:

- Outputs are classified as **Restricted Management Information** until both method credibility and data
  credibility are confirmed by the designated owners (GOV-003, GOV-004).
- Baseline workforce definition, attrition assumption, and Early Careers intake assumption are owned by
  the Requester / Customer Owner (DEP-006 – DEP-008).
- Capability-risk interpretation and wider-sharing approval are owned by the Engineering Director
  (DEP-009 – DEP-010).
- Initial outputs MUST be stored in the access-controlled P&A Business Operations library (GOV-002).
- Required CSV columns (`ID`, `Age`, `Service`, `Job_Family`, and either `Grade` or `Grade_Score`)
  MUST be validated on load; the app MUST surface a clear error for any missing field.

## Development Standards

- All CLI commands on this machine MUST be prefixed with `PYTHONUTF8=1` to prevent Windows encoding
  crashes (applies to any script invoked from the project).
- No direct commits to `main`. Conventional commit messages (`feat:`, `fix:`, `chore:`, `docs:`, etc.)
  are required.
- Push and PR creation MUST be confirmed with the user before execution.
- The app is run with `streamlit run app.py`; the venv is at `.venv/`.
- Dependencies are pinned in `requirements.txt`. Dependency additions require a recorded rationale.

## Governance

This constitution supersedes all other practices for this project. Amendment rules:

- **MAJOR** (v2.0.0+): Removing or redefining a Core Principle, changing the WEI formula, or changing
  the authoritative data source. Requires sign-off from both the Requester / Customer Owner and the
  Engineering Director.
- **MINOR** (v1.1.0+): Adding a new principle or section, or materially expanding guidance. Requires
  acknowledgement from one designated owner.
- **PATCH** (v1.0.1+): Wording clarifications, typo fixes, non-semantic refinements. No sign-off
  required.

All implementation plans MUST include a Constitution Check gate (referencing principles I–V by name)
before Phase 0 research. The check MUST be re-run after Phase 1 design.

Compliance review is expected at each project milestone and before any wider-sharing event.

**Version**: 1.1.1 | **Ratified**: 2026-04-21 | **Last Amended**: 2026-04-21
