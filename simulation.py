"""
simulation.py
Core workforce simulation engine.
All functions are decoupled so the WEI formula can be swapped independently.
"""
from __future__ import annotations
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Core validation constants
# ---------------------------------------------------------------------------

REQUIRED_COLS = {"ID", "Age", "Service", "Job_Family"}

# ---------------------------------------------------------------------------
# Grade structure constants (T001)
# ---------------------------------------------------------------------------

GRADE_SCORE_MAP: dict[str, int] = {
    'A1': 1, 'A2': 2, 'B1': 3, 'B2': 4, 'C1': 5, 'C2': 6, 'D': 7
}

GRADE_LABELS: list[str] = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2', 'D']

EXP_HIRE_PRESETS: dict[str, dict] = {
    'junior': {'age_mid': 31, 'age_sd': 4, 'grade': 'A2', 'grade_score': 2},
    'mid':    {'age_mid': 38, 'age_sd': 6, 'grade': 'B2', 'grade_score': 4},
    'senior': {'age_mid': 47, 'age_sd': 7, 'grade': 'C1', 'grade_score': 5},
}

MARKET_STRENGTH_PRESETS: dict[str, float] = {
    'strong':   1.00,
    'moderate': 0.70,
    'weak':     0.40,
}

EC_COHORT_DEFAULTS: dict[str, dict] = {
    'L3': {
        'programme_years': 4,
        'outturn_grade': 'A1',
        'outturn_age': 21,
        'outturn_service': 4,
    },
    'L6': {
        'programme_years': 4,
        'outturn_grade': 'B1',
        'outturn_age': 22,
        'outturn_service': 4,
    },
    'Grad': {
        'programme_years': 2,
        'outturn_grade': 'B1',
        'outturn_age': 23,
        'outturn_service': 2,
    },
}


# ---------------------------------------------------------------------------
# Load and validate
# ---------------------------------------------------------------------------

def load_workforce(path: str) -> pd.DataFrame:
    """
    Load a workforce CSV and validate required columns.

    Accepts either a 'Grade' string column (A1–D) or a numeric 'Grade_Score'
    column. If 'Grade' is present it takes precedence; 'Grade_Score' is derived
    via GRADE_SCORE_MAP. If only 'Grade_Score' is present, 'Grade' is added as
    an empty string. Neither column present raises ValueError.
    """
    df = pd.read_csv(path)
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")
    if "Grade" not in df.columns and "Grade_Score" not in df.columns:
        raise ValueError(
            "CSV must contain either a 'Grade' column (A1–D) or a 'Grade_Score' column"
        )
    df = df.copy()
    df["Age"] = df["Age"].astype(int)
    df["Service"] = df["Service"].astype(int)
    if "Grade" in df.columns:
        unknown = set(df["Grade"].dropna().unique()) - set(GRADE_SCORE_MAP.keys())
        if unknown:
            raise ValueError(f"Unknown grade values in 'Grade' column: {sorted(unknown)}")
        df["Grade_Score"] = df["Grade"].map(GRADE_SCORE_MAP).astype(float)
    else:
        df["Grade_Score"] = df["Grade_Score"].clip(1, 10).astype(float)
        df["Grade"] = ""
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
    df: pd.DataFrame, threshold_age: int, max_age: int, base_prob: float, rng: np.random.Generator
) -> pd.DataFrame:
    """
    US3: Extended Graduated Retirement Curve.
    Probability increases linearly from base_prob at threshold_age to 1.0 at max_age.
    Applies only to survivors of attrition to avoid double-counting (AS-206).
    """
    if len(df) == 0:
        return df

    p = np.zeros(len(df))
    age = df["Age"].values
    
    mask_ramp = (age >= threshold_age) & (age <= max_age)
    if max_age > threshold_age:
        p[mask_ramp] = base_prob + (1.0 - base_prob) * (age[mask_ramp] - threshold_age) / (max_age - threshold_age)
    else:
        p[mask_ramp] = 1.0
        
    p[age > max_age] = 1.0
    p = np.clip(p, 0.0, 1.0)
    
    draw = rng.random(len(df))
    keep = draw >= p
    return df[keep].copy()


def _advance_ec_pipeline(pipeline: list[float], annual_intake: int, dropout_rate: float, programme_years: int) -> tuple[list[float], int]:
    """US4: Advance pipeline, dropouts applied, pop outturn from the end."""
    reduced = [p * (1.0 - dropout_rate) for p in pipeline]
    outturn = int(round(reduced[-1])) if len(reduced) > 0 else 0
    updated_pipeline = [float(annual_intake)] + reduced[:-1]
    return updated_pipeline, outturn


def _apply_ec_outturn(df: pd.DataFrame, outturn_dict: dict[str, int], next_id: int, rng: np.random.Generator) -> tuple[pd.DataFrame, int]:
    """US4: Apply EC cohort pipeline outturn to dataframe."""
    total_outturn = sum(outturn_dict.values())
    if total_outturn == 0:
        return df, next_id
        
    families = df["Job_Family"].value_counts(normalize=True)
    new_rows = []
    
    for cohort_type, count in outturn_dict.items():
        if count <= 0:
            continue
        defaults = EC_COHORT_DEFAULTS[cohort_type]
        for _ in range(count):
            idx = np.searchsorted(families.values.cumsum(), rng.random())
            idx = min(idx, len(families) - 1)
            new_rows.append({
                "ID": f"EC_{next_id:04d}",
                "Age": defaults["outturn_age"],
                "Service": defaults["outturn_service"],
                "Grade_Score": float(GRADE_SCORE_MAP[defaults["outturn_grade"]]),
                "Grade": defaults["outturn_grade"],
                "Job_Family": families.index[idx],
            })
            next_id += 1
            
    out_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True) if new_rows else df
    return out_df, next_id


def _apply_experienced_hires(
    df: pd.DataFrame, ceiling: int | None, profile_key: str, market_key: str, rng: np.random.Generator, next_id: int
) -> tuple[pd.DataFrame, float, float, int]:
    """US2: Fill ceiling gap with experienced hires (step 6)."""
    if ceiling is None:
        return df, 0.0, 0.0, next_id
    
    gap = max(0, ceiling - len(df))
    if gap <= 0:
        return df, 0.0, 0.0, next_id
        
    hires = min(gap, int(round(gap * MARKET_STRENGTH_PRESETS[market_key])))
    demand = float(gap)
    
    if hires <= 0:
        return df, 0.0, demand, next_id
        
    preset = EXP_HIRE_PRESETS[profile_key]
    families = df["Job_Family"].value_counts(normalize=True)
    new_rows = []
    
    for _ in range(hires):
        age = int(round(rng.normal(preset['age_mid'], preset['age_sd'])))
        age = max(20, min(75, age))
        idx = np.searchsorted(families.values.cumsum(), rng.random())
        idx = min(idx, len(families) - 1)
        new_rows.append({
            "ID": f"EH_{next_id:04d}",
            "Age": age,
            "Service": max(0, age - 22),
            "Grade_Score": float(preset['grade_score']),
            "Grade": preset['grade'],
            "Job_Family": families.index[idx],
        })
        next_id += 1
        
    out_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
    return out_df, float(hires), demand, next_id


def simulate_year(
    df: pd.DataFrame, *, attrition_rate: float, retirement_age_threshold: int,
    retirement_max_age: int,
    retirement_prob: float, year: int,
    rng: np.random.Generator,
):
    """Advance workforce by one year. Order: Age -> Attrition -> Retirement -> Inflow."""
    df = df.copy()
    df["Age"] += 1
    df["Service"] += 1
    df = _apply_attrition(df, attrition_rate, rng)
    df = _apply_retirement_proxy(df, retirement_age_threshold, retirement_max_age, retirement_prob, rng)
    return df


# ---------------------------------------------------------------------------
# Full multi-year projection
# ---------------------------------------------------------------------------

def run_projection(
    df: pd.DataFrame, *,
    years: int = 10,
    attrition_rate: float = 0.05,
    retirement_threshold: int = 60,
    retirement_max_age: int = 75,
    retirement_base_prob: float = 0.05,
    ec_config: dict | None = None,
    ceiling: int | None = None,
    exp_hire_profile: str = 'mid',
    market_strength: str = 'moderate',
    seed: int = 42,
    # Legacy parameter aliases — accepted for backward compatibility with existing callers
    retirement_age_threshold: int | None = None,
    retirement_prob: float | None = None,
    annual_intake: int = 0,
) -> dict:
    """
    Project workforce over `years` years.

    Returns a dict with keys:
      wei_series, headcount, snapshots, age_bands, baseline_numerator,
      recruiting_demand, experienced_hires_added, ec_outturn, grade_snapshots.

    New keys (recruiting_demand, experienced_hires_added, ec_outturn, grade_snapshots)
    are populated in later phases (US1–US5). They are initialised here so callers
    can safely access them without KeyError.
    """
    # Resolve legacy aliases so existing app.py callers continue to work
    if retirement_age_threshold is not None:
        retirement_threshold = retirement_age_threshold
    if retirement_prob is not None:
        retirement_base_prob = retirement_prob

    rng = np.random.default_rng(seed)
    baseline_numerator = compute_wei_numerator(df)
    if ec_config is None:
        ec_config = {
            "L3": {"intake": 0, "dropout": 0.0},
            "L6": {"intake": 0, "dropout": 0.0},
            "Grad": {"intake": annual_intake, "dropout": 0.0},
        }

    ec_state = {
        'L3': [0.0] * EC_COHORT_DEFAULTS['L3']['programme_years'],
        'L6': [0.0] * EC_COHORT_DEFAULTS['L6']['programme_years'],
        'Grad': [0.0] * EC_COHORT_DEFAULTS['Grad']['programme_years'],
    }

    results: dict = {
        "wei_series": [],
        "headcount": [],
        "snapshots": {},
        "age_bands": {},
        "baseline_numerator": baseline_numerator,
        "recruiting_demand": [],
        "experienced_hires_added": [],
        "ec_outturn": {"L3": [], "L6": [], "Grad": []},
        "grade_snapshots": [],
    }
    current_df = df.copy()
    next_id = 1
    for year in range(years + 1):
        wei = compute_wei(current_df, baseline_numerator)
        results["wei_series"].append(round(wei, 4))
        results["headcount"].append(len(current_df))
        results["snapshots"][year] = current_df.copy()
        results["age_bands"][year] = (
            assign_age_band(current_df["Age"]).value_counts().sort_index()
        )
        
        if "Grade" in current_df.columns:
            grade_counts = current_df["Grade"].value_counts().to_dict()
        else:
            grade_counts = {}
            
        grade_snap = {g: int(grade_counts.get(g, 0)) for g in GRADE_LABELS}
        unknown_str_count = sum(v for k, v in grade_counts.items() if k not in GRADE_LABELS)
        grade_snap["Unknown"] = int(unknown_str_count)
        
        results["grade_snapshots"].append(grade_snap)

        if year < years:
            current_df = simulate_year(
                current_df,
                attrition_rate=attrition_rate,
                retirement_age_threshold=retirement_threshold,
                retirement_max_age=retirement_max_age,
                retirement_prob=retirement_base_prob,
                year=year + 1,
                rng=rng,
            )
            
            # Step 4: Early Careers Outturn
            outturn_dict = {}
            for ctype in ["L3", "L6", "Grad"]:
                intake = ec_config[ctype]["intake"]
                dropout = ec_config[ctype]["dropout"]
                prog_years = EC_COHORT_DEFAULTS[ctype]["programme_years"]
                updated_pipeline, outturn = _advance_ec_pipeline(
                    ec_state[ctype], intake, dropout, prog_years
                )
                ec_state[ctype] = updated_pipeline
                outturn_dict[ctype] = outturn
                results["ec_outturn"][ctype].append(outturn)
                
            current_df, next_id = _apply_ec_outturn(current_df, outturn_dict, next_id, rng)
            current_df, hires, demand, next_id = _apply_experienced_hires(
                current_df, ceiling, exp_hire_profile, market_strength, rng, next_id
            )
            if ceiling is not None:
                results["recruiting_demand"].append(demand)
                results["experienced_hires_added"].append(hires)
    return results
