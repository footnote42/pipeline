"""
simulation.py
Core workforce simulation engine.
All functions are decoupled so the WEI formula can be swapped independently.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

REQUIRED_COLS = {"ID", "Age", "Service", "Grade_Score", "Job_Family"}


def load_workforce(path: str) -> pd.DataFrame:
    """Load a workforce CSV and validate required columns."""
    df = pd.read_csv(path)
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")
    df = df.copy()
    df["Age"] = df["Age"].astype(int)
    df["Service"] = df["Service"].astype(int)
    df["Grade_Score"] = df["Grade_Score"].clip(1, 10).astype(float)
    return df.reset_index(drop=True)


# ---------------------------------------------------------------------------
# WEI formula — modify compute_wei_numerator to change the index definition
# ---------------------------------------------------------------------------

def compute_wei_numerator(df: pd.DataFrame) -> float:
    """Raw WEI sum: sum(Grade_Score_i * Service_i). Swap this to redefine WEI."""
    return float((df["Grade_Score"] * df["Service"]).sum())


def compute_wei(df: pd.DataFrame, baseline_numerator: float) -> float:
    """Normalised WEI relative to t=0 baseline (1.0 = as-is)."""
    if baseline_numerator == 0:
        return 0.0
    return compute_wei_numerator(df) / baseline_numerator


# ---------------------------------------------------------------------------
# Age-band helper
# ---------------------------------------------------------------------------

AGE_BAND_BINS   = [0, 25, 35, 45, 55, 65, 999]
AGE_BAND_LABELS = ["Under 25", "25-34", "35-44", "45-54", "55-64", "65+"]


def assign_age_band(age_series: pd.Series) -> pd.Series:
    return pd.cut(age_series, bins=AGE_BAND_BINS, labels=AGE_BAND_LABELS, right=False)


# ---------------------------------------------------------------------------
# Simulation steps
# ---------------------------------------------------------------------------

def _apply_attrition(df: pd.DataFrame, attrition_rate: float, rng: np.random.Generator) -> pd.DataFrame:
    """Remove employees based on flat annual attrition probability (AS-101/103)."""
    stay_mask = rng.random(len(df)) >= attrition_rate
    return df[stay_mask].copy()


def _apply_retirement_proxy(
    df: pd.DataFrame, threshold_age: int, base_prob: float, rng: np.random.Generator
) -> pd.DataFrame:
    """
    Retirement proxy (AS-201 to AS-206).
    Probability increases linearly with years over threshold, capped at 0.95.
    Applies only to survivors of attrition to avoid double-counting.
    """
    over = df["Age"] >= threshold_age
    years_over = (df["Age"] - threshold_age).clip(lower=0)
    scaled = (base_prob + years_over * 0.05).clip(upper=0.95)
    draw = rng.random(len(df))
    keep = ~over | (draw >= scaled)
    return df[keep].copy()


def _apply_inflow(df: pd.DataFrame, annual_intake: int, year: int, next_id: int):
    """Add Early Careers joiners at Age 21, Grade_Score 1 (FR-003/004)."""
    if annual_intake <= 0:
        return df, next_id
    families = df["Job_Family"].value_counts(normalize=True)
    rng_local = np.random.default_rng(year * 1000)
    new_rows = []
    for _ in range(annual_intake):
        idx = np.searchsorted(families.values.cumsum(), rng_local.random())
        idx = min(idx, len(families) - 1)
        new_rows.append({
            "ID": f"EC{year:02d}_{next_id:04d}",
            "Age": 21, "Service": 0, "Grade_Score": 1.0,
            "Job_Family": families.index[idx],
        })
        next_id += 1
    return pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True), next_id


def simulate_year(
    df: pd.DataFrame, *, attrition_rate: float, retirement_age_threshold: int,
    retirement_prob: float, annual_intake: int, year: int, next_id: int,
    rng: np.random.Generator,
):
    """Advance workforce by one year. Order: Age -> Attrition -> Retirement -> Inflow."""
    df = df.copy()
    df["Age"] += 1
    df["Service"] += 1
    df = _apply_attrition(df, attrition_rate, rng)
    df = _apply_retirement_proxy(df, retirement_age_threshold, retirement_prob, rng)
    df, next_id = _apply_inflow(df, annual_intake, year, next_id)
    return df, next_id


# ---------------------------------------------------------------------------
# Full multi-year projection
# ---------------------------------------------------------------------------

def run_projection(
    baseline_df: pd.DataFrame, *, years: int = 10,
    attrition_rate: float = 0.05, retirement_age_threshold: int = 60,
    retirement_prob: float = 0.20, annual_intake: int = 50, seed: int = 42,
) -> dict:
    """
    Project workforce over `years` years.
    Returns: wei_series, headcount, snapshots, age_bands, baseline_numerator.
    """
    rng = np.random.default_rng(seed)
    baseline_numerator = compute_wei_numerator(baseline_df)
    results = {
        "wei_series": [], "headcount": [],
        "snapshots": {}, "age_bands": {},
        "baseline_numerator": baseline_numerator,
    }
    current_df = baseline_df.copy()
    next_id = 1
    for year in range(years + 1):
        wei = compute_wei(current_df, baseline_numerator)
        results["wei_series"].append(round(wei, 4))
        results["headcount"].append(len(current_df))
        results["snapshots"][year] = current_df.copy()
        results["age_bands"][year] = (
            assign_age_band(current_df["Age"]).value_counts().sort_index()
        )
        if year < years:
            current_df, next_id = simulate_year(
                current_df, attrition_rate=attrition_rate,
                retirement_age_threshold=retirement_age_threshold,
                retirement_prob=retirement_prob, annual_intake=annual_intake,
                year=year + 1, next_id=next_id, rng=rng,
            )
    return results
