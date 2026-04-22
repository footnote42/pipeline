"""
app.py
------
Workforce Scenario Modelling App — Streamlit entry point.
Run: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import os

from simulation import load_workforce, run_projection, AGE_BAND_LABELS, REQUIRED_COLS
from charts import (
    wei_trend_chart, age_band_chart, headcount_waterfall,
    recruiting_demand_chart, grade_snapshot_chart,
)

# ---------------------------------------------------------------------------
# Page config — must be first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Workforce Scenario Modeller",
    page_icon="W",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_CSV   = os.path.join(os.path.dirname(__file__), "data", "sample_workforce.csv")
TIPPING_POINT = 0.85

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "results" not in st.session_state:
    st.session_state.results = None
if "params" not in st.session_state:
    st.session_state.params = {}

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.toggle("Dark mode", key="dark_mode")
    st.markdown("---")
    st.markdown("## Data Source")
    uploaded = st.file_uploader(
        "Upload Workforce CSV", type=["csv"],
        help=f"Required columns: {', '.join(sorted(REQUIRED_COLS))}"
    )
    use_sample = st.checkbox("Use built-in sample (~1,100 employees)", value=(uploaded is None))

    st.markdown("---")
    st.markdown("## Scenario Controls")

    with st.expander("Attrition", expanded=True):
        attrition_rate = st.slider(
            "Annual Attrition Rate (%)", min_value=1, max_value=25, value=6, step=1,
            help="Flat probability that any employee leaves in a given year (AS-101)."
        ) / 100

    with st.expander("Retirement", expanded=False):
        retirement_age = st.slider(
            "Retirement Threshold (Age)", min_value=55, max_value=68, value=60, step=1,
            help="Age at which graduation curve begins (AS-202)."
        )
        retirement_max_age = st.number_input(
            "Retirement Max Age (100% exit)", min_value=65, max_value=80, value=75, step=1
        )
        retirement_prob = st.slider(
            "Base Retirement Probability (%)", min_value=0, max_value=60, value=5, step=1,
            help="Starting annual exit probability at the threshold age (AS-203)."
        ) / 100

    with st.expander("Early Careers", expanded=False):
        l3_intake = st.number_input("L3 Apprentice Intake", min_value=0, max_value=200, value=0, step=5)
        l6_intake = st.number_input("L6 Apprentice Intake", min_value=0, max_value=200, value=0, step=5)
        grad_intake = st.number_input("Graduate Intake", min_value=0, max_value=200, value=50, step=5)
        ec_dropout = st.slider("EC Flow Dropout Rate (%)", min_value=0, max_value=50, value=10, step=1) / 100

        ec_config = {
            "L3": {"intake": l3_intake, "dropout": ec_dropout},
            "L6": {"intake": l6_intake, "dropout": ec_dropout},
            "Grad": {"intake": grad_intake, "dropout": ec_dropout},
        }

    with st.expander("Experienced Hires", expanded=False):
        exp_hire_profile = st.radio("Hire Profile Seniority", options=["junior", "mid", "senior"], index=1)
        market_strength = st.selectbox(
            "Market Strength", options=["weak", "moderate", "strong"], index=1,
            help="Recruiting market strength preset."
        )

    with st.expander("Headcount Ceiling", expanded=False):
        ceiling = st.number_input("Maximum Headcount", min_value=500, value=1100, step=10)

    with st.expander("Projection Horizon", expanded=False):
        projection_years = st.slider("Projection Horizon (Years)", 5, 20, 10)

    st.markdown("---")
    run_btn = st.button("Run Simulation", type="primary", use_container_width=True)

# ---------------------------------------------------------------------------
# Theme tokens — resolved after sidebar so dark_mode is current
# ---------------------------------------------------------------------------
dark_mode = st.session_state.dark_mode

if dark_mode:
    _bg, _surface, _border = "#1A1A1A", "#252525", "#333333"
    _text, _text_sub       = "#FFFFFF", "#8A949D"   # 5.65:1 on #1A1A1A — AA pass
else:
    _bg, _surface, _border = "#FFFFFF", "#F5F5F5", "#E0E0E0"
    _text, _text_sub       = "#1A1A1A", "#636D78"   # 5.25:1 on #FFFFFF — AA pass

_accent      = "#444AFF"
_danger      = "#FF5C32"
_accent_tint = "rgba(68,74,255,0.12)"

# ---------------------------------------------------------------------------
# Custom CSS — design system aligned, theme-aware
# ---------------------------------------------------------------------------
# Font loading — preconnect eliminates TCP handshake delay; <link> is non-blocking unlike @import
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,200..800&family=Manrope:wght@200..800&display=swap">
""", unsafe_allow_html=True)

st.markdown(f"""
<style>

/* ── Streamlit theme variable overrides ── */
:root {{
    --primary-color: {_accent};
    --background-color: {_bg};
    --secondary-background-color: {_surface};
    --text-color: {_text};
}}

/* ── Base ── */
html, body, [class*="css"] {{
    font-family: 'Manrope', sans-serif;
    color: {_text};
}}
h1, h2, h3, h4, h5, h6 {{
    font-family: 'Bricolage Grotesque', sans-serif;
    color: {_text} !important;
}}
p {{ color: {_text}; }}

.stApp {{ background: {_bg}; color: {_text}; }}

/* Main block — catches most body text Streamlit renders */
[data-testid="stMainBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {{
    color: {_text};
}}
[data-testid="stMainBlockContainer"] p,
[data-testid="stMainBlockContainer"] span,
[data-testid="stMainBlockContainer"] li,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span {{
    color: {_text} !important;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {_surface};
    border-right: 1px solid {_border};
}}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] button,
[data-testid="stSidebar"] a {{ color: {_text} !important; }}
[data-testid="stSidebar"] .stMarkdown h2 {{
    font-family: 'Bricolage Grotesque', sans-serif;
    font-weight: 600; font-size: 1rem;
    border-bottom: 1px solid {_border}; padding-bottom: 0.5rem;
}}

/* ── Widget labels & captions ── */
label, [data-testid="stWidgetLabel"] p {{ color: {_text} !important; }}
[data-testid="stCaptionContainer"] p {{ color: {_text_sub} !important; }}

/* ── File uploader ── */
[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploadDropzone"] {{
    background: {_bg} !important;
    border: 2px dashed {_border} !important;
}}
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploadDropzone"] p,
[data-testid="stFileUploadDropzone"] span,
[data-testid="stFileUploadDropzone"] small,
[data-testid="stFileUploadDropzone"] button {{ color: {_text} !important; }}
[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small {{
    color: {_text_sub} !important;
}}

/* ── Expanders ── */
[data-testid="stExpander"] {{
    border: 1px solid {_border} !important;
    border-radius: 8px;
    background: {_surface} !important;
}}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
[data-testid="stExpanderToggleIcon"] {{ color: {_text} !important; }}
[data-testid="stExpander"] > div {{ background: {_surface} !important; }}

/* ── Inputs & number fields ── */
input, textarea {{
    color: {_text} !important;
    background: {_bg} !important;
    border-color: {_border} !important;
}}

/* ── Selectbox ── */
[data-testid="stSelectbox"] p,
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] label {{ color: {_text} !important; }}
[data-testid="stSelectbox"] [data-baseweb="select"] > div {{
    background: {_bg} !important;
    border-color: {_border} !important;
}}
/* Dropdown list */
[data-baseweb="popover"] [role="listbox"],
[data-baseweb="popover"] [role="option"] {{
    background: {_surface} !important;
    color: {_text} !important;
}}
[data-baseweb="popover"] [aria-selected="true"] {{
    background: {_accent_tint} !important;
    color: {_accent} !important;
}}

/* ── Multiselect ── */
[data-testid="stMultiSelect"] p,
[data-testid="stMultiSelect"] span,
[data-testid="stMultiSelect"] label,
[data-testid="stMultiSelect"] input {{ color: {_text} !important; }}
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {{
    background: {_bg} !important;
    border-color: {_border} !important;
}}
[data-baseweb="tag"] {{
    background: {_accent_tint} !important;
}}
[data-baseweb="tag"] span {{ color: {_text} !important; }}

/* ── Radio ── */
[data-testid="stRadio"] p,
[data-testid="stRadio"] span,
[data-testid="stRadio"] label,
[data-testid="stRadio"] div {{ color: {_text} !important; }}

/* ── Slider ── */
[data-testid="stSlider"] p, [data-testid="stSlider"] span {{ color: {_text} !important; }}

/* ── Toggle ── */
[data-testid="stToggle"] p {{ color: {_text} !important; }}

/* ── Metric cards ── */
[data-testid="metric-container"] {{
    background: {_surface};
    border: 1px solid {_border};
    border-radius: 12px;
    padding: 1rem 1.25rem;
}}
[data-testid="stMetricValue"] {{
    color: {_text} !important;
    font-size: 1.6rem; font-weight: 700;
    font-family: 'Bricolage Grotesque', sans-serif;
}}
[data-testid="stMetricDelta"] {{ font-size: 0.85rem; }}
[data-testid="stMetricLabel"] p {{ color: {_text_sub} !important; font-size: 0.85rem; }}

/* ── Tabs ── */
[data-testid="stTabs"] button {{
    color: {_text_sub}; font-weight: 500;
    border-bottom: 2px solid transparent;
    font-family: 'Manrope', sans-serif;
}}
[data-testid="stTabs"] button[aria-selected="true"] {{
    color: {_accent} !important; border-bottom: 2px solid {_accent};
}}
/* Tab content area */
[data-testid="stTabsContent"] p,
[data-testid="stTabsContent"] span,
[data-testid="stTabsContent"] h1,
[data-testid="stTabsContent"] h2,
[data-testid="stTabsContent"] h3,
[data-testid="stTabsContent"] h4,
[data-testid="stTabsContent"] li {{ color: {_text}; }}

/* ── Streamlit native alerts (st.info etc.) ── */
[data-testid="stAlert"] p {{ color: {_text} !important; }}

/* ── Custom components ── */
.tipping-warning {{
    background: rgba(255,92,50,0.10);
    border: 1px solid {_danger};
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: {_danger} !important;
    font-weight: 500;
    margin-bottom: 1.25rem;
    max-width: 80ch;
}}
.tipping-warning * {{ color: {_danger} !important; }}
.info-card {{
    background: {_surface};
    border: 1px solid {_border};
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin: 1rem 0;
    max-width: 80ch;
}}
.info-card * {{ color: {_text}; }}

/* ── Dataframe ── */
[data-testid="stDataFrameContainer"] {{ border-radius: 12px; overflow: hidden; }}

/* ── Spacing utility ── */
.spacer {{ height: 1rem; }}

/* ── Screen-reader only utility ── */
.sr-only {{
    position: absolute; width: 1px; height: 1px;
    padding: 0; margin: -1px; overflow: hidden;
    clip: rect(0,0,0,0); white-space: nowrap; border: 0;
}}

/* ── Responsive KPI row ── */
@media (max-width: 900px) {{
    [data-testid="stMetricValue"] {{ font-size: 1.1rem !important; }}
    [data-testid="stMetricLabel"] p {{ font-size: 0.75rem !important; }}
    [data-testid="stMetricDelta"] {{ font-size: 0.75rem !important; }}
}}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
@st.cache_data
def get_baseline(path: str) -> pd.DataFrame:
    return load_workforce(path)


def load_data():
    if uploaded is not None:
        import io
        return load_workforce(io.StringIO(uploaded.read().decode("utf-8")))
    if use_sample and os.path.exists(DEFAULT_CSV):
        return get_baseline(DEFAULT_CSV)
    return None


baseline_df = load_data()

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(f"""
<div style="padding: 1.5rem 0 1rem 0;">
    <h1 style="font-family:'Bricolage Grotesque',sans-serif; color:{_text}; font-size:2rem; font-weight:700; margin:0;">
        Workforce Scenario Modeller
    </h1>
    <p style="font-family:'Manrope',sans-serif; color:{_text_sub}; margin:0.25rem 0 0 0; font-size:0.95rem;">
        Year-on-year projection of workforce age, experience, and capability risk
    </p>
</div>
""", unsafe_allow_html=True)

if baseline_df is None:
    st.info("Upload a workforce CSV or enable the sample dataset to begin.")
    st.stop()

# ---------------------------------------------------------------------------
# Simulation — auto-run on first load or param change
# ---------------------------------------------------------------------------
current_params = dict(
    attrition_rate=attrition_rate, retirement_age_threshold=retirement_age,
    retirement_max_age=retirement_max_age,
    retirement_prob=retirement_prob,
    ec_config=ec_config,
    years=projection_years,
    ceiling=ceiling,
    exp_hire_profile=exp_hire_profile,
    market_strength=market_strength,
)

if run_btn or st.session_state.results is None or st.session_state.params != current_params:
    with st.spinner("Running projection..."):
        st.session_state.results = run_projection(baseline_df, **current_params)
    st.session_state.params = current_params

results     = st.session_state.results
years_axis  = list(range(projection_years + 1))
wei_series  = results["wei_series"]
headcount   = results["headcount"]

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
final_wei  = wei_series[-1]
trough_yr  = next((y for y, w in enumerate(wei_series) if w < TIPPING_POINT), None)

kpi_row1 = st.columns(3)
kpi_row2 = st.columns(2)
with kpi_row1[0]:
    st.metric("Baseline Headcount", f"{len(baseline_df):,}")
with kpi_row1[1]:
    st.metric(f"Year {projection_years} WEI", f"{final_wei:.3f}",
              delta=f"{final_wei - 1.0:+.3f} vs baseline",
              delta_color="inverse")
with kpi_row1[2]:
    st.metric(f"Year {projection_years} Headcount", f"{headcount[-1]:,}",
              delta=f"{headcount[-1] - headcount[0]:+,}")
with kpi_row2[0]:
    if trough_yr is not None:
        st.metric("Tipping Point (WEI < 0.85)", f"Year {trough_yr}", delta="Risk identified", delta_color="inverse")
    else:
        st.metric("Tipping Point (WEI < 0.85)", "Not reached", delta="Within safe range", delta_color="normal")
with kpi_row2[1]:
    if results.get("recruiting_demand"):
        total_demand = sum(results["recruiting_demand"])
        total_hires  = sum(results["experienced_hires_added"])
        st.metric("Total Recruiting Demand", f"{int(total_demand):,}", delta=f"{int(total_hires):,} hired")
    else:
        st.metric("Total Recruiting Demand", "N/A", delta="No ceiling")

st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

# Tipping-point warning banner
if trough_yr is not None:
    st.markdown(
        f"""<div class="tipping-warning" role="alert" aria-live="polite">
        <span aria-hidden="true">&#9888;</span><span class="sr-only">Warning:</span>
        WEI drops below 0.85 at <strong>Year {trough_yr}</strong>
        (WEI = {wei_series[trough_yr]:.3f}).
        Sustained experience erosion is likely without targeted intervention.
        </div>""",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Executive Summary", "Demographics", "Assumptions"])

# ---- Tab 1: Executive Summary -----------------------------------------------
with tab1:
    annual_intake  = l3_intake + l6_intake + grad_intake
    scenario_label = (
        f"Attrition {attrition_rate:.0%} | Retirement threshold {retirement_age} | Intake {annual_intake}/yr"
    )
    fig_wei = wei_trend_chart(
        years_axis, wei_series, headcount, scenario_label,
        ceiling=current_params["ceiling"], dark=dark_mode,
    )
    st.plotly_chart(fig_wei, use_container_width=True)
    if trough_yr is not None:
        st.caption(
            f"WEI declines from 1.00 to {final_wei:.3f} over {projection_years} years. "
            f"The tipping point (WEI < 0.85) is first reached at Year {trough_yr} "
            f"(WEI = {wei_series[trough_yr]:.3f}). Headcount ends at {headcount[-1]:,}."
        )
    else:
        st.caption(
            f"WEI moves from 1.00 to {final_wei:.3f} over {projection_years} years, "
            f"remaining above the 0.85 tipping-point threshold throughout. "
            f"Headcount ends at {headcount[-1]:,}."
        )

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
    st.plotly_chart(headcount_waterfall(headcount, years_axis, dark=dark_mode), use_container_width=True)
    _net = headcount[-1] - headcount[0]
    st.caption(
        f"Net headcount {'increases' if _net >= 0 else 'decreases'} from "
        f"{headcount[0]:,} to {headcount[-1]:,} over {projection_years} years "
        f"(net {'+' if _net >= 0 else ''}{_net:,})."
    )

    if results.get("recruiting_demand"):
        fig_demand = recruiting_demand_chart(
            years_axis[1:],
            results["recruiting_demand"],
            results["experienced_hires_added"],
            scenario_label,
            dark=dark_mode,
        )
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
        st.plotly_chart(fig_demand, use_container_width=True)
        _total_demand = sum(results["recruiting_demand"])
        _total_hires  = sum(results["experienced_hires_added"])
        st.caption(
            f"Cumulative recruiting demand over {projection_years} years: {int(_total_demand):,} roles. "
            f"{int(_total_hires):,} hires added; {int(_total_demand - _total_hires):,} unfilled gap."
        )

# ---- Tab 2: Demographics ----------------------------------------------------
with tab2:
    max_yr = projection_years

    st.markdown("#### Grade Distribution")
    st.caption("Headcount overview per grade for a specific year.")
    selected_grade_year = st.slider(
        "Select Year for Grade Snapshot", min_value=0, max_value=max_yr, value=max_yr, step=1
    )

    if results.get("grade_snapshots"):
        fig_grades = grade_snapshot_chart(results["grade_snapshots"], selected_grade_year, dark=dark_mode)
        st.plotly_chart(fig_grades, use_container_width=True)
        _gdata = results["grade_snapshots"][selected_grade_year]
        _top_grade = max(_gdata, key=_gdata.get) if _gdata else "—"
        _total_graded = sum(_gdata.values())
        st.caption(
            f"Year {selected_grade_year}: {_total_graded:,} employees across all grades. "
            f"Largest group: Grade {_top_grade} ({_gdata.get(_top_grade, 0):,} employees)."
        )

    st.markdown("---")
    st.markdown("#### Age-Band Distribution")
    st.caption("Select which years to display in the comparison view.")

    default_years   = sorted(set([0, max_yr // 2, max_yr]))
    selected_display = st.multiselect(
        "Years to compare",
        options=list(range(max_yr + 1)),
        default=default_years,
        format_func=lambda y: f"Year {y}" + (" (Baseline)" if y == 0 else ""),
    )

    if selected_display:
        fig_bands = age_band_chart(results["age_bands"], selected_display, dark=dark_mode)
        st.plotly_chart(fig_bands, use_container_width=True)
        _yr_labels = " vs ".join(
            f"Year {y}" + (" (Baseline)" if y == 0 else "") for y in sorted(selected_display)
        )
        _band_totals = {
            y: int(results["age_bands"][y].sum()) for y in selected_display
            if y in results["age_bands"]
        }
        _totals_str = "; ".join(f"Year {y}: {t:,}" for y, t in sorted(_band_totals.items()))
        st.caption(f"Age-band comparison — {_yr_labels}. Total headcount: {_totals_str}.")
    else:
        st.info("Select at least one year above.")

    st.markdown("#### Age-Band Summary Table")
    band_rows = {}
    for yr in range(max_yr + 1):
        series = results["age_bands"][yr]
        band_rows[f"Year {yr}"] = {b: int(series.get(b, 0)) for b in AGE_BAND_LABELS}
    band_df = pd.DataFrame(band_rows).T
    band_df["Total"] = band_df.sum(axis=1)
    st.dataframe(band_df.style.bar(color="rgba(68,74,255,0.35)", axis=1), use_container_width=True)

# ---- Tab 3: Assumptions -----------------------------------------------------
with tab3:
    st.markdown("#### Active Scenario Variables")
    st.caption(
        "All levers and their current values. See your Assumptions Register (AR-001) "
        "for full governance context (AS-101 to AS-603)."
    )

    assumptions = pd.DataFrame([
        {
            "Parameter": "Annual Attrition Rate",
            "Value": f"{attrition_rate:.1%}",
            "Range available": "1% – 25%",
            "Register ref": "AS-101 / AS-103",
            "Owner": "Requester / Customer Owner",
            "Sensitivity": "H",
        },
        {
            "Parameter": "Retirement Age Threshold",
            "Value": str(retirement_age),
            "Range available": "55 – 68",
            "Register ref": "AS-202",
            "Owner": "Requester / Customer Owner",
            "Sensitivity": "H",
        },
        {
            "Parameter": "Base Retirement Probability",
            "Value": f"{retirement_prob:.0%}",
            "Range available": "5% – 60%",
            "Register ref": "AS-203",
            "Owner": "Requester / Customer Owner",
            "Sensitivity": "H",
        },
        {
            "Parameter": "Early Careers Intake Configuration",
            "Value": f"L3: {l3_intake}, L6: {l6_intake}, Grad: {grad_intake}",
            "Range available": "0 – 200 per tier",
            "Register ref": "AS-406 / AS-403",
            "Owner": "Requester / Customer Owner",
            "Sensitivity": "H",
        },
        {
            "Parameter": "Projection Horizon (Years)",
            "Value": str(projection_years),
            "Range available": "3 – 15",
            "Register ref": "AS-404",
            "Owner": "Requester / Customer Owner",
            "Sensitivity": "M",
        },
        {
            "Parameter": "WEI Formula",
            "Value": "sum(Grade_Score × Service) normalised to t=0",
            "Range available": "Reference-profile (active)",
            "Register ref": "AS-301 / AS-302",
            "Owner": "Engineering Director Owner",
            "Sensitivity": "H",
        },
        {
            "Parameter": "WEI Tipping-Point Threshold",
            "Value": "0.85 (15% decline vs as-is)",
            "Range available": "User-configurable in code",
            "Register ref": "AS-307",
            "Owner": "Engineering Director Owner",
            "Sensitivity": "H",
        },
        {
            "Parameter": "Retirement / Attrition double-counting",
            "Value": "Mutually exclusive (attrition first, retirement on survivors)",
            "Range available": "Fixed design rule",
            "Register ref": "AS-206",
            "Owner": "Requester / Customer Owner",
            "Sensitivity": "H",
        },
        {
            "Parameter": "Early Careers Joiner Profile",
            "Value": "Age 21, Grade_Score 1, proportional job-family distribution",
            "Range available": "Fixed design rule",
            "Register ref": "AS-403 / FR-003",
            "Owner": "Requester / Customer Owner",
            "Sensitivity": "M",
        },
        {
            "Parameter": "Baseline Population",
            "Value": f"{len(baseline_df):,} employees",
            "Range available": "Loaded from CSV",
            "Register ref": "AS-001 / AS-002",
            "Owner": "Requester / Customer Owner",
            "Sensitivity": "H",
        },
    ])

    st.dataframe(assumptions, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div class="info-card">
        <strong style="color:{_text};">Method note (AS-302 / AS-507)</strong><br>
        <span style="font-size:0.9rem;">
        This model uses the reference-profile WEI method: all projected states are compared against
        the current &ldquo;as-is&rdquo; workforce (WEI = 1.0). Claims made from this output are
        scenario-based and proportionate to the evidence. No causal predictions are intended.
        Wider sharing requires method credibility + data credibility sign-off (GOV-004).
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Scenario Summary")
    summary_df = pd.DataFrame({
        "Year":       [f"Year {y}" for y in years_axis],
        "WEI":        wei_series,
        "Headcount":  headcount,
        "WEI Status": ["Below tipping point" if w < TIPPING_POINT else "Within safe range" for w in wei_series],
    })
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.markdown("#### Early Careers Outturn Pipeline")
    if results.get("ec_outturn"):
        ec_df = pd.DataFrame(results["ec_outturn"])
        ec_df.index = [f"Year {y}" for y in range(1, len(ec_df) + 1)]
        st.dataframe(ec_df.T, use_container_width=True)
