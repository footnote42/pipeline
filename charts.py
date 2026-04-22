"""
charts.py
Plotly chart builders for the Workforce Scenario Modelling App.
Each function returns a go.Figure — keep display logic in app.py.
"""
from __future__ import annotations
import plotly.graph_objects as go
import pandas as pd

TIPPING_POINT = 0.85
ACCENT        = "#444AFF"   # blue — precision/action signal
DANGER        = "#FF5C32"   # orange — risk signals only
DANGER_WARM   = "#FFA851"   # light orange — warmth accent
NEUTRAL       = "#75808B"   # grey — supporting text/borders
PURPLE        = "#9BA0F9"   # tertiary accent

YEAR_PALETTE  = ["#444AFF", "#9BA0F9", "#FFA851", "#FF5C32", "#75808B", "#1A1A1A"]

_THEME = {
    False: {
        "bg":             "#FFFFFF",
        "surface":        "#F5F5F5",
        "grid":           "#E0E0E0",
        "text":           "#1A1A1A",
        "text_sub":       "#75808B",
        "annotation_bg":  "rgba(255,255,255,0.92)",
    },
    True: {
        "bg":             "#1A1A1A",
        "surface":        "#252525",
        "grid":           "#333333",
        "text":           "#FFFFFF",
        "text_sub":       "#75808B",
        "annotation_bg":  "rgba(26,26,26,0.92)",
    },
}


def _base_layout(title: str, dark: bool = False) -> dict:
    t = _THEME[dark]
    return dict(
        title=dict(
            text=title,
            font=dict(size=18, color=t["text"], family="Bricolage Grotesque, sans-serif"),
            x=0.02,
        ),
        paper_bgcolor=t["bg"],
        plot_bgcolor=t["bg"],
        font=dict(family="Manrope, sans-serif", color=t["text_sub"]),
        xaxis=dict(gridcolor=t["grid"], zeroline=False),
        yaxis=dict(gridcolor=t["grid"], zeroline=False),
        margin=dict(l=50, r=30, t=60, b=50),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=t["grid"], font=dict(color=t["text"])),
        hovermode="x unified",
    )


def wei_trend_chart(
    years: list[int],
    wei_series: list[float],
    headcount: list[int],
    scenario_name: str = "Scenario",
    ceiling: int | None = None,
    dark: bool = False,
) -> go.Figure:
    """Executive Summary: WEI trend with tipping-point band and headcount secondary axis."""
    t = _THEME[dark]
    fig = go.Figure()

    # Risk zone — orange tint (danger signal, not red)
    fig.add_hrect(
        y0=0, y1=TIPPING_POINT,
        fillcolor="rgba(255,92,50,0.08)", line_width=0,
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
    fig.add_hline(
        y=1.0, line_dash="dot", line_color=NEUTRAL, line_width=1,
        annotation_text="As-Is Baseline", annotation_position="top left",
        annotation_font_color=NEUTRAL,
    )

    # WEI line — blue primary, markers switch to orange when below tipping point
    colors = [DANGER if w < TIPPING_POINT else ACCENT for w in wei_series]
    fig.add_trace(go.Scatter(
        x=years, y=wei_series, name="WEI",
        mode="lines+markers",
        line=dict(color=ACCENT, width=3),
        marker=dict(size=8, color=colors, line=dict(color=t["bg"], width=1.5)),
        hovertemplate="Year %{x}: WEI = %{y:.3f}<extra></extra>",
    ))

    # Headcount secondary axis — purple tertiary accent
    fig.add_trace(go.Scatter(
        x=years, y=headcount, name="Headcount",
        mode="lines", yaxis="y2",
        line=dict(color=PURPLE, width=1.5, dash="dot"),
        hovertemplate="Year %{x}: %{y} employees<extra></extra>",
        opacity=0.8,
    ))

    # Ceiling line — orange (risk: capacity constraint)
    if ceiling is not None:
        fig.add_hline(
            y=ceiling, yref="y2", line_dash="dash", line_color=DANGER, line_width=1.5,
            annotation_text=f"Ceiling: {ceiling}", annotation_position="top right",
            annotation_font_color=DANGER,
        )

    # First tipping-point marker annotation
    for yr, w in zip(years, wei_series):
        if w < TIPPING_POINT:
            fig.add_annotation(
                x=yr, y=w, text=f"Tipping Point<br>Year {yr}",
                showarrow=True, arrowhead=2, arrowcolor=DANGER,
                font=dict(color=DANGER, size=12),
                bgcolor=t["annotation_bg"], bordercolor=DANGER, borderwidth=1,
            )
            break

    layout = _base_layout(f"Weighted Experience Index (WEI) — {scenario_name}", dark=dark)
    layout.update(
        yaxis=dict(title="WEI (1.0 = As-Is Baseline)", range=[0, 1.3],
                   gridcolor=t["grid"], zeroline=False),
        yaxis2=dict(title="Headcount", overlaying="y", side="right",
                    showgrid=False, zeroline=False, color=PURPLE),
        xaxis=dict(title="Year", gridcolor=t["grid"], zeroline=False, tickmode="linear"),
    )
    fig.update_layout(**layout)
    return fig


def age_band_chart(age_band_data: dict, selected_years: list[int], dark: bool = False) -> go.Figure:
    """Demographics: grouped bar chart of age-band distribution across selected years."""
    band_order = ["Under 25", "25-34", "35-44", "45-54", "55-64", "65+"]
    t = _THEME[dark]

    fig = go.Figure()
    for i, yr in enumerate(selected_years):
        series = age_band_data.get(yr, pd.Series(dtype=int))
        counts = [int(series.get(b, 0)) for b in band_order]
        fig.add_trace(go.Bar(
            name=f"Year {yr}", x=band_order, y=counts,
            marker_color=YEAR_PALETTE[i % len(YEAR_PALETTE)],
            hovertemplate="%{x}: %{y} employees<extra></extra>",
        ))

    layout = _base_layout("Age-Band Distribution Over Time", dark=dark)
    layout.update(
        barmode="group",
        xaxis=dict(title="Age Band", gridcolor=t["grid"], zeroline=False),
        yaxis=dict(title="Headcount", gridcolor=t["grid"], zeroline=False),
    )
    fig.update_layout(**layout)
    return fig


def headcount_waterfall(headcount: list[int], years: list[int], dark: bool = False) -> go.Figure:
    """Net headcount change year-on-year waterfall."""
    t = _THEME[dark]
    deltas = [headcount[0]] + [headcount[i] - headcount[i - 1] for i in range(1, len(headcount))]
    measures = ["absolute"] + ["relative"] * (len(years) - 1)

    fig = go.Figure(go.Waterfall(
        x=[f"Yr {y}" for y in years], y=deltas, measure=measures,
        connector=dict(line=dict(color=t["grid"])),
        decreasing=dict(marker_color=DANGER),
        increasing=dict(marker_color=ACCENT),
        totals=dict(marker_color=NEUTRAL),
        hovertemplate="Year %{x}: %{y:+d}<extra></extra>",
    ))
    layout = _base_layout("Net Headcount Change (Waterfall)", dark=dark)
    layout.update(
        yaxis=dict(title="Headcount Delta", gridcolor=t["grid"], zeroline=True, zerolinecolor=NEUTRAL),
        xaxis=dict(gridcolor=t["grid"]),
        showlegend=False,
    )
    fig.update_layout(**layout)
    return fig


def recruiting_demand_chart(
    years: list[int],
    demand: list[float],
    hires: list[float],
    scenario_name: str = "Scenario",
    dark: bool = False,
) -> go.Figure:
    """Grouped bar chart for unfilled headcount gap and actual hires."""
    t = _THEME[dark]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Recruiting Demand", x=years, y=demand,
        marker_color=DANGER,
        hovertemplate="Year %{x}: %{y} gap<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Hires Added", x=years, y=hires,
        marker_color=ACCENT,
        hovertemplate="Year %{x}: %{y} hires<extra></extra>",
    ))

    layout = _base_layout(f"Recruiting Demand & Hires — {scenario_name}", dark=dark)
    layout.update(
        barmode="group",
        xaxis=dict(title="Year", gridcolor=t["grid"], zeroline=False, tickmode="linear"),
        yaxis=dict(title="Employees", gridcolor=t["grid"], zeroline=False),
    )
    fig.update_layout(**layout)
    return fig


def grade_snapshot_chart(grade_snapshots: list[dict], selected_year: int, dark: bool = False) -> go.Figure:
    """Demographics: horizontal bar chart for grade headcount."""
    t = _THEME[dark]
    data = grade_snapshots[selected_year]
    band_order = ["A1", "A2", "B1", "B2", "C1", "C2", "D", "Unknown"]
    y_labels = list(reversed(band_order))
    x_values = [data.get(k, 0) for k in y_labels]

    fig = go.Figure(go.Bar(
        x=x_values, y=y_labels, orientation='h',
        marker_color=ACCENT,
        hovertemplate="Grade %{y}: %{x} employees<extra></extra>",
    ))

    layout = _base_layout(f"Grade Distribution — Year {selected_year}", dark=dark)
    layout.update(
        xaxis=dict(title="Headcount", gridcolor=t["grid"], zeroline=False),
        yaxis=dict(title="Grade", gridcolor=t["grid"], zeroline=False),
    )
    fig.update_layout(**layout)
    return fig
