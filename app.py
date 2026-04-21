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
from charts import wei_trend_chart, age_band_chart, headcount_waterfall

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Workforce Scenario Modeller",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS — dark premium theme
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Main background */
.stApp { background: #0F172A; color: #CBD5E1; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #1E293B;
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] .stMarkdown h2 {
    color: #F1F5F9; font-weight: 600; font-size: 1rem;
    border-bottom: 1px solid #334155; padding-bottom: 0.5rem;
}

/* Metric cards */
[data-testid="metric-container"] {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1rem 1.25rem;
}
[data-testid="stMetricValue"] { color: #F1F5F9; font-size: 1.6rem; font-weight: 700; }
[data-testid="stMetricDelta"] { font-size: 0.85rem; }

/* Tabs */
[data-testid="stTabs"] button {
    color: #94A3B8; font-weight: 500;
    border-bottom: 2px solid transparent;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #6C63FF; border-bottom: 2px solid #6C63FF;
}

/* Warning banner */
.tipping-warning {
    background: linear-gradient(135deg, rgba(255,75,110,0.15), rgba(255,75,110,0.05));
    border: 1px solid #FF4B6E;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #FDA4AF;
    font-weight: 500;
    margin-bottom: 1.25rem;
}

/* Info card */
.info-card {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
}

/* Table styling */
[data-testid="stDataFrameContainer"] { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helper: find the default CSV
# ---------------------------------------------------------------------------
DEFAULT_CSV = os.path.join(os.path.dirname(__file__), "data", "sample_workforce.csv")
TIPPING_POINT = 0.85


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## Data Source")
    uploaded = st.file_uploader(
        "Upload Workforce CSV", type=["csv"],
        help=f"Required columns: {', '.join(sorted(REQUIRED_COLS))}"
    )
    use_sample = st.checkbox("Use built-in sample (~1,100 employees)", value=(uploaded is None))

    st.markdown("---")
    st.markdown("## Scenario Controls")

    attrition_rate = st.slider(
        "Annual Attrition Rate (%)", min_value=1, max_value=25, value=6, step=1,
        help="Flat probability that any employee leaves in a given year (AS-101)."
    ) / 100

    retirement_age = st.slider(
        "Retirement Proxy Threshold (Age)", min_value=55, max_value=68, value=60, step=1,
        help="Age above which an increasing retirement probability applies (AS-202)."
    )

    retirement_prob = st.slider(
        "Base Retirement Probability (%)", min_value=5, max_value=60, value=20, step=5,
        help="Starting annual exit probability at the threshold age — scales up year-on-year (AS-203)."
    ) / 100

    annual_intake = st.slider(
        "Early Careers Annual Intake", min_value=0, max_value=200, value=50, step=5,
        help="Number of joiners added each year at Age 21, Grade_Score 1 (FR-003/004)."
    )

    projection_years = st.slider(
        "Projection Horizon (Years)", min_value=3, max_value=15, value=10, step=1
    )

    st.markdown("---")
    run_btn = st.button("Run Simulation", type="primary", use_container_width=True)


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
st.markdown("""
<div style="padding: 1.5rem 0 1rem 0;">
    <h1 style="color:#F1F5F9; font-size:2rem; font-weight:700; margin:0;">
        Workforce Scenario Modeller
    </h1>
    <p style="color:#64748B; margin:0.25rem 0 0 0; font-size:0.95rem;">
        Year-on-year projection of workforce age, experience, and capability risk
    </p>
</div>
""", unsafe_allow_html=True)

if baseline_df is None:
    st.info("Upload a workforce CSV or enable the sample dataset to begin.")
    st.stop()

# ---------------------------------------------------------------------------
# Session state for results
# ---------------------------------------------------------------------------
if "results" not in st.session_state:
    st.session_state.results = None
if "params" not in st.session_state:
    st.session_state.params = {}

current_params = dict(
    attrition_rate=attrition_rate, retirement_age_threshold=retirement_age,
    retirement_prob=retirement_prob, annual_intake=annual_intake,
    years=projection_years,
)

# Auto-run on first load or when params change
if run_btn or st.session_state.results is None or st.session_state.params != current_params:
    with st.spinner("Running projection..."):
        st.session_state.results = run_projection(
            baseline_df, **current_params
        )
    st.session_state.params = current_params

results = st.session_state.results
years_axis = list(range(projection_years + 1))
wei_series = results["wei_series"]
headcount  = results["headcount"]

# ---------------------------------------------------------------------------
# KPI row
# ---------------------------------------------------------------------------
final_wei   = wei_series[-1]
peak_wf     = max(headcount)
trough_yr   = next((y for y, w in enumerate(wei_series) if w < TIPPING_POINT), None)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Baseline Headcount",  f"{len(baseline_df):,}")
with col2:
    st.metric(f"Year {projection_years} WEI", f"{final_wei:.3f}",
              delta=f"{final_wei - 1.0:+.3f} vs baseline",
              delta_color="inverse")
with col3:
    st.metric(f"Year {projection_years} Headcount", f"{headcount[-1]:,}",
              delta=f"{headcount[-1] - headcount[0]:+,}")
with col4:
    if trough_yr is not None:
        st.metric("Tipping Point (WEI < 0.85)", f"Year {trough_yr}", delta="Risk identified", delta_color="inverse")
    else:
        st.metric("Tipping Point (WEI < 0.85)", "Not reached", delta="Within safe range", delta_color="normal")

st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

# Tipping-point warning banner
if trough_yr is not None:
    st.markdown(
        f"""<div class="tipping-warning">
        &#9888; WEI drops below 0.85 at <strong>Year {trough_yr}</strong>
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
    scenario_label = (
        f"Attrition {attrition_rate:.0%} | Retirement threshold {retirement_age} | Intake {annual_intake}/yr"
    )
    fig_wei = wei_trend_chart(years_axis, wei_series, headcount, scenario_label)
    st.plotly_chart(fig_wei, use_container_width=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
    st.plotly_chart(headcount_waterfall(headcount, years_axis), use_container_width=True)

# ---- Tab 2: Demographics ----------------------------------------------------
with tab2:
    st.markdown("#### Age-Band Distribution")
    st.caption("Select which years to display in the comparison view.")

    max_yr = projection_years
    default_years = sorted(set([0, max_yr // 2, max_yr]))
    selected_display = st.multiselect(
        "Years to compare",
        options=list(range(max_yr + 1)),
        default=default_years,
        format_func=lambda y: f"Year {y}" + (" (Baseline)" if y == 0 else ""),
    )

    if selected_display:
        fig_bands = age_band_chart(results["age_bands"], selected_display)
        st.plotly_chart(fig_bands, use_container_width=True)
    else:
        st.info("Select at least one year above.")

    # Age-band table
    st.markdown("#### Age-Band Summary Table")
    band_rows = {}
    for yr in range(max_yr + 1):
        series = results["age_bands"][yr]
        band_rows[f"Year {yr}"] = {b: int(series.get(b, 0)) for b in AGE_BAND_LABELS}
    band_df = pd.DataFrame(band_rows).T
    band_df["Total"] = band_df.sum(axis=1)
    st.dataframe(band_df.style.background_gradient(cmap="Blues", axis=1), use_container_width=True)

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
            "Parameter": "Early Careers Annual Intake",
            "Value": str(annual_intake),
            "Range available": "0 – 200",
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

    st.markdown("""
    <div class="info-card" style="margin-top:1rem;">
        <strong style="color:#F1F5F9;">Method note (AS-302 / AS-507)</strong><br>
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
        "Year": [f"Year {y}" for y in years_axis],
        "WEI": wei_series,
        "Headcount": headcount,
        "WEI Status": ["Below tipping point" if w < TIPPING_POINT else "Within safe range" for w in wei_series],
    })
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
