"""
charts.py
Plotly chart builders for the Workforce Scenario Modelling App.
Each function returns a go.Figure — keep display logic in app.py.
"""
from __future__ import annotations
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

TIPPING_POINT = 0.85
ACCENT   = "#6C63FF"
DANGER   = "#FF4B6E"
NEUTRAL  = "#94A3B8"
BG       = "#0F172A"
SURFACE  = "#1E293B"
GRID     = "#334155"


def _base_layout(title: str) -> dict:
    return dict(
        title=dict(text=title, font=dict(size=18, color="#F1F5F9"), x=0.02),
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family="Inter, sans-serif", color="#CBD5E1"),
        xaxis=dict(gridcolor=GRID, zeroline=False),
        yaxis=dict(gridcolor=GRID, zeroline=False),
        margin=dict(l=50, r=30, t=60, b=50),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID),
        hovermode="x unified",
    )


def wei_trend_chart(
    years: list[int],
    wei_series: list[float],
    headcount: list[int],
    scenario_name: str = "Scenario",
    ceiling: int | None = None,
) -> go.Figure:
    """Executive Summary: WEI trend with tipping-point band and headcount secondary axis."""
    fig = go.Figure()

    # Tipping-point shaded zone
    fig.add_hrect(
        y0=0, y1=TIPPING_POINT,
        fillcolor="rgba(255,75,110,0.08)", line_width=0,
        annotation_text="Risk Zone (WEI < 0.85)",
        annotation_position="bottom right",
        annotation_font_color=DANGER,
    )

    # Tipping-point reference line
    fig.add_hline(
        y=TIPPING_POINT, line_dash="dash", line_color=DANGER, line_width=1.5,
        annotation_text="Tipping Point 0.85", annotation_position="top right",
        annotation_font_color=DANGER,
    )

    # Baseline reference
    fig.add_hline(y=1.0, line_dash="dot", line_color=NEUTRAL, line_width=1,
                  annotation_text="As-Is Baseline", annotation_position="top left",
                  annotation_font_color=NEUTRAL)

    # WEI line
    colors = [DANGER if w < TIPPING_POINT else ACCENT for w in wei_series]
    fig.add_trace(go.Scatter(
        x=years, y=wei_series, name="WEI",
        mode="lines+markers",
        line=dict(color=ACCENT, width=3),
        marker=dict(size=8, color=colors, line=dict(color=BG, width=1.5)),
        hovertemplate="Year %{x}: WEI = %{y:.3f}<extra></extra>",
    ))

    # Headcount on secondary axis
    fig.add_trace(go.Scatter(
        x=years, y=headcount, name="Headcount",
        mode="lines", yaxis="y2",
        line=dict(color="#38BDF8", width=1.5, dash="dot"),
        hovertemplate="Year %{x}: %{y} employees<extra></extra>",
        opacity=0.7,
    ))

    # Optional Headcount Ceiling reference line
    if ceiling is not None:
        fig.add_hline(
            y=ceiling, yref="y2", line_dash="dash", line_color="#FF5C32", line_width=1.5,
            annotation_text=f"Ceiling: {ceiling}", annotation_position="top right",
            annotation_font_color="#FF5C32",
        )

    # Tipping-point marker
    for yr, w in zip(years, wei_series):
        if w < TIPPING_POINT:
            fig.add_annotation(
                x=yr, y=w, text=f"Tipping Point<br>Year {yr}",
                showarrow=True, arrowhead=2, arrowcolor=DANGER,
                font=dict(color=DANGER, size=12),
                bgcolor="rgba(15,23,42,0.85)", bordercolor=DANGER, borderwidth=1,
            )
            break

    layout = _base_layout(f"Weighted Experience Index (WEI) — {scenario_name}")
    layout.update(
        yaxis=dict(title="WEI (1.0 = As-Is Baseline)", range=[0, 1.3],
                   gridcolor=GRID, zeroline=False),
        yaxis2=dict(title="Headcount", overlaying="y", side="right",
                    showgrid=False, zeroline=False, color="#38BDF8"),
        xaxis=dict(title="Year", gridcolor=GRID, zeroline=False, tickmode="linear"),
    )
    fig.update_layout(**layout)
    return fig


def age_band_chart(age_band_data: dict, selected_years: list[int]) -> go.Figure:
    """Demographics: grouped bar chart of age-band distribution across selected years."""
    band_order = ["Under 25", "25-34", "35-44", "45-54", "55-64", "65+"]
    palette = px.colors.sequential.Plasma_r
    colors = [palette[i * (len(palette) // max(len(selected_years), 1))] for i in range(len(selected_years))]

    fig = go.Figure()
    for i, yr in enumerate(selected_years):
        series = age_band_data.get(yr, pd.Series(dtype=int))
        counts = [int(series.get(b, 0)) for b in band_order]
        fig.add_trace(go.Bar(
            name=f"Year {yr}", x=band_order, y=counts,
            marker_color=colors[i % len(colors)],
            hovertemplate="%{x}: %{y} employees<extra></extra>",
        ))

    layout = _base_layout("Age-Band Distribution Over Time")
    layout.update(
        barmode="group",
        xaxis=dict(title="Age Band", gridcolor=GRID, zeroline=False),
        yaxis=dict(title="Headcount", gridcolor=GRID, zeroline=False),
    )
    fig.update_layout(**layout)
    return fig


def headcount_waterfall(headcount: list[int], years: list[int]) -> go.Figure:
    """Small waterfall showing net headcount change year-on-year."""
    deltas = [headcount[0]] + [headcount[i] - headcount[i - 1] for i in range(1, len(headcount))]
    measures = ["absolute"] + ["relative"] * (len(years) - 1)
    colors_bar = [ACCENT if d >= 0 else DANGER for d in deltas]

    fig = go.Figure(go.Waterfall(
        x=[f"Yr {y}" for y in years], y=deltas, measure=measures,
        connector=dict(line=dict(color=GRID)),
        decreasing=dict(marker_color=DANGER),
        increasing=dict(marker_color=ACCENT),
        totals=dict(marker_color=NEUTRAL),
        hovertemplate="Year %{x}: %{y:+d}<extra></extra>",
    ))
    layout = _base_layout("Net Headcount Change (Waterfall)")
    layout.update(
        yaxis=dict(title="Headcount Delta", gridcolor=GRID, zeroline=True, zerolinecolor=NEUTRAL),
        xaxis=dict(gridcolor=GRID),
        showlegend=False,
    )
    fig.update_layout(**layout)
    return fig


def recruiting_demand_chart(
    years: list[int],
    demand: list[float],
    hires: list[float],
    scenario_name: str = "Scenario",
) -> go.Figure:
    """Grouped bar chart for unfilled headcount gap and actual hires."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Recruiting Demand", x=years, y=demand,
        marker_color="#FF5C32",
        hovertemplate="Year %{x}: %{y} gap<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Hires Added", x=years, y=hires,
        marker_color="#38BDF8",
        hovertemplate="Year %{x}: %{y} hires<extra></extra>",
    ))

    layout = _base_layout(f"Recruiting Demand & Hires — {scenario_name}")
    layout.update(
        barmode="group",
        xaxis=dict(title="Year", gridcolor=GRID, zeroline=False, tickmode="linear"),
        yaxis=dict(title="Employees", gridcolor=GRID, zeroline=False),
    )
    fig.update_layout(**layout)
    return fig


def grade_snapshot_chart(grade_snapshots: list[dict], selected_year: int) -> go.Figure:
    """Demographics: horizontal bar chart for grade headcount."""
    data = grade_snapshots[selected_year]
    band_order = ["A1", "A2", "B1", "B2", "C1", "C2", "D", "Unknown"]
    y_labels = list(reversed(band_order))
    x_values = [data.get(k, 0) for k in y_labels]

    fig = go.Figure(go.Bar(
        x=x_values, y=y_labels, orientation='h',
        marker_color=ACCENT,
        hovertemplate="Grade %{y}: %{x} employees<extra></extra>",
    ))
    
    layout = _base_layout(f"Grade Distribution — Year {selected_year}")
    layout.update(
        xaxis=dict(title="Headcount", gridcolor=GRID, zeroline=False),
        yaxis=dict(title="Grade", gridcolor=GRID, zeroline=False),
    )
    fig.update_layout(**layout)
    return fig
