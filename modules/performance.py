"""
performance.py
Core performance classification logic for Capacity Connect.
All classification decisions are made here and reused across the application.
"""

import pandas as pd
import streamlit as st
from modules.data_manager import load_employees, load_appraisals, get_latest_appraisal


# ──────────────────────────────────────────────────────────────────────────────
# Classification constants
# ──────────────────────────────────────────────────────────────────────────────

CATEGORY_TOP_NOTCH = "Top Notch"
CATEGORY_MEDIOCRE = "Mediocre"
CATEGORY_BELOW_AVERAGE = "Below Average"
CATEGORY_NOT_APPRAISED = "Not Appraised"

CATEGORY_THRESHOLDS = {
    CATEGORY_TOP_NOTCH: (80, 100),
    CATEGORY_MEDIOCRE: (50, 79),
    CATEGORY_BELOW_AVERAGE: (0, 49),
}

# Clean visual indicators (no emoji clutter)
CATEGORY_BADGES = {
    CATEGORY_TOP_NOTCH: "●",
    CATEGORY_MEDIOCRE: "●",
    CATEGORY_BELOW_AVERAGE: "●",
    CATEGORY_NOT_APPRAISED: "○",
}

CATEGORY_COLORS = {
    CATEGORY_TOP_NOTCH: "#059669",      # Emerald
    CATEGORY_MEDIOCRE: "#d97706",       # Amber
    CATEGORY_BELOW_AVERAGE: "#dc2626",   # Rose/Red
    CATEGORY_NOT_APPRAISED: "#64748b",   # Slate
}


# ──────────────────────────────────────────────────────────────────────────────
# Core classification function
# ──────────────────────────────────────────────────────────────────────────────

def classify_performance(score) -> str:
    """
    Classify an employee's performance based on their appraisal score.

    Args:
        score: Numeric performance score (0–100) or None / NaN.

    Returns:
        One of: 'Top Notch', 'Mediocre', 'Below Average', or 'Not Appraised'.
    """
    if score is None or (isinstance(score, float) and pd.isna(score)):
        return CATEGORY_NOT_APPRAISED

    try:
        score = float(score)
    except (ValueError, TypeError):
        return CATEGORY_NOT_APPRAISED

    if not (0 <= score <= 100):
        raise ValueError(f"Score must be between 0 and 100. Got: {score}")

    if score >= 80:
        return CATEGORY_TOP_NOTCH
    elif score >= 50:
        return CATEGORY_MEDIOCRE
    else:
        return CATEGORY_BELOW_AVERAGE


def validate_score(score) -> tuple:
    """
    Validate that a score is a number between 0 and 100.

    Returns:
        (is_valid: bool, error_message: str)
    """
    try:
        score = float(score)
    except (ValueError, TypeError):
        return False, "Score must be a valid number."

    if score < 0 or score > 100:
        return False, "Score must be between 0 and 100."

    return True, ""


# ──────────────────────────────────────────────────────────────────────────────
# Enriched employee data (employees + latest appraisal + category)
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=None, show_spinner=False)
def get_enriched_employees() -> pd.DataFrame:
    """
    Return all employees with their latest appraisal score and performance category.

    Columns added:
        - latest_score
        - latest_appraisal_date
        - latest_remarks
        - performance_category
    """
    employees = load_employees()
    appraisals = load_appraisals()

    if appraisals.empty:
        employees["latest_score"] = None
        employees["latest_appraisal_date"] = None
        employees["latest_remarks"] = None
        employees["performance_category"] = CATEGORY_NOT_APPRAISED
        return employees

    # Get the latest appraisal per employee (sort by date then keep last)
    appraisals_sorted = appraisals.sort_values("appraisal_date", ascending=False)
    latest = appraisals_sorted.drop_duplicates(subset="employee_id", keep="first")

    latest = latest[["employee_id", "performance_score", "appraisal_date", "remarks"]].rename(
        columns={
            "performance_score": "latest_score",
            "appraisal_date": "latest_appraisal_date",
            "remarks": "latest_remarks",
        }
    )

    enriched = employees.merge(latest, on="employee_id", how="left")
    enriched["performance_category"] = enriched["latest_score"].apply(classify_performance)

    return enriched


# ──────────────────────────────────────────────────────────────────────────────
# Dashboard statistics
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=None, show_spinner=False)
def get_dashboard_stats() -> dict:
    """
    Compute summary statistics for the dashboard.

    Returns a dict with keys:
        total_employees, avg_score, top_notch, mediocre,
        below_average, not_appraised, category_counts, dept_stats
    """
    enriched = get_enriched_employees()

    total = len(enriched)
    appraised = enriched[enriched["performance_category"] != CATEGORY_NOT_APPRAISED]
    avg_score = round(appraised["latest_score"].mean(), 2) if not appraised.empty else 0.0

    category_counts = enriched["performance_category"].value_counts().to_dict()

    top_notch = category_counts.get(CATEGORY_TOP_NOTCH, 0)
    mediocre = category_counts.get(CATEGORY_MEDIOCRE, 0)
    below_average = category_counts.get(CATEGORY_BELOW_AVERAGE, 0)
    not_appraised = category_counts.get(CATEGORY_NOT_APPRAISED, 0)

    # Department-wise average score
    dept_stats = (
        appraised.groupby("department")["latest_score"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "avg_score", "count": "employee_count"})
        .round(2)
        .reset_index()
    )

    return {
        "total_employees": total,
        "avg_score": avg_score,
        "top_notch": top_notch,
        "mediocre": mediocre,
        "below_average": below_average,
        "not_appraised": not_appraised,
        "category_counts": category_counts,
        "dept_stats": dept_stats,
        "enriched_df": enriched,
    }


def get_category_badge(category: str) -> str:
    """Return an emoji badge for the given category."""
    return CATEGORY_BADGES.get(category, "❓")


def get_category_color(category: str) -> str:
    """Return the hex color for the given category."""
    return CATEGORY_COLORS.get(category, "#95a5a6")
