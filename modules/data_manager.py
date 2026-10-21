"""
data_manager.py
Handles all CSV read/write operations for Capacity Connect.
Uses st.cache_data for read operations to dramatically speed up the app.
"""

import pandas as pd
import os
import streamlit as st

# Base directory for data files (relative to project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

EMPLOYEES_FILE  = os.path.join(DATA_DIR, "employees.csv")
APPRAISALS_FILE = os.path.join(DATA_DIR, "appraisals.csv")
FEEDBACK_FILE   = os.path.join(DATA_DIR, "feedback.csv")


# ──────────────────────────────────────────────────────────────────────────────
# Cached loaders — TTL of 0 means "cache until explicitly cleared"
# ──────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=None, show_spinner=False)
def load_employees() -> pd.DataFrame:
    """Load all employees from the CSV file (cached)."""
    try:
        df = pd.read_csv(EMPLOYEES_FILE)
        df["employee_id"]  = df["employee_id"].astype(str).str.strip()
        df["joining_date"] = pd.to_datetime(df["joining_date"], errors="coerce")
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["employee_id","name","department","designation","email","joining_date"])
    except Exception as e:
        st.warning(f"Could not load employees: {e}")
        return pd.DataFrame(columns=["employee_id","name","department","designation","email","joining_date"])


@st.cache_data(ttl=None, show_spinner=False)
def load_appraisals() -> pd.DataFrame:
    """Load all appraisals from the CSV file (cached)."""
    try:
        df = pd.read_csv(APPRAISALS_FILE)
        df["employee_id"]      = df["employee_id"].astype(str).str.strip()
        df["appraisal_date"]   = pd.to_datetime(df["appraisal_date"], errors="coerce")
        df["performance_score"]= pd.to_numeric(df["performance_score"], errors="coerce")
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["appraisal_id","employee_id","appraisal_date","performance_score","remarks"])
    except Exception as e:
        st.warning(f"Could not load appraisals: {e}")
        return pd.DataFrame(columns=["appraisal_id","employee_id","appraisal_date","performance_score","remarks"])


@st.cache_data(ttl=None, show_spinner=False)
def load_feedback() -> pd.DataFrame:
    """Load all feedback from the CSV file (cached)."""
    try:
        df = pd.read_csv(FEEDBACK_FILE)
        df["employee_id"]   = df["employee_id"].astype(str).str.strip()
        df["feedback_date"] = pd.to_datetime(df["feedback_date"], errors="coerce")
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=["feedback_id","employee_id","feedback_type","comments","feedback_date"])
    except Exception as e:
        st.warning(f"Could not load feedback: {e}")
        return pd.DataFrame(columns=["feedback_id","employee_id","feedback_type","comments","feedback_date"])


def _bust_cache():
    """Invalidate all data caches after a write operation."""
    load_employees.clear()
    load_appraisals.clear()
    load_feedback.clear()
    # Also clear enriched/stats caches defined in performance.py
    try:
        from modules.performance import get_enriched_employees, get_dashboard_stats
        get_enriched_employees.clear()
        get_dashboard_stats.clear()
    except Exception:
        pass


# ──────────────────────────────────────────────────────────────────────────────
# Write operations
# ──────────────────────────────────────────────────────────────────────────────

def save_appraisal(employee_id: str, appraisal_date: str,
                   performance_score: float, remarks: str) -> tuple:
    """Append a new appraisal record. Returns (success, message)."""
    try:
        df = load_appraisals()
        if df.empty:
            new_id = "A001"
        else:
            nums = []
            for aid in df["appraisal_id"].astype(str):
                try:
                    nums.append(int(aid.replace("A","").strip()))
                except ValueError:
                    pass
            new_id = f"A{str(max(nums)+1 if nums else 1).zfill(3)}"

        new_row = pd.DataFrame([{
            "appraisal_id":    new_id,
            "employee_id":     employee_id,
            "appraisal_date":  appraisal_date,
            "performance_score": performance_score,
            "remarks":         remarks,
        }])
        new_row.to_csv(APPRAISALS_FILE, mode="a", header=False, index=False)
        _bust_cache()
        return True, f"Appraisal {new_id} saved successfully for employee {employee_id}."
    except Exception as e:
        return False, f"Error saving appraisal: {e}"


def save_feedback(employee_id: str, feedback_type: str,
                  comments: str, feedback_date: str) -> tuple:
    """Append a new feedback record. Returns (success, message)."""
    try:
        df = load_feedback()
        if df.empty:
            new_id = "F001"
        else:
            nums = []
            for fid in df["feedback_id"].astype(str):
                try:
                    nums.append(int(fid.replace("F","").strip()))
                except ValueError:
                    pass
            new_id = f"F{str(max(nums)+1 if nums else 1).zfill(3)}"

        new_row = pd.DataFrame([{
            "feedback_id":   new_id,
            "employee_id":   employee_id,
            "feedback_type": feedback_type,
            "comments":      comments,
            "feedback_date": feedback_date,
        }])
        new_row.to_csv(FEEDBACK_FILE, mode="a", header=False, index=False)
        _bust_cache()
        return True, f"Feedback {new_id} saved successfully for employee {employee_id}."
    except Exception as e:
        return False, f"Error saving feedback: {e}"


# ──────────────────────────────────────────────────────────────────────────────
# Convenience accessors (use cached loaders internally)
# ──────────────────────────────────────────────────────────────────────────────

def get_employee_by_id(employee_id: str) -> pd.Series:
    df = load_employees()
    match = df[df["employee_id"] == employee_id.strip()]
    return match.iloc[0] if not match.empty else None


def get_latest_appraisal(employee_id: str) -> pd.Series:
    df = load_appraisals()
    emp = df[df["employee_id"] == employee_id.strip()].copy()
    if emp.empty:
        return None
    return emp.sort_values("appraisal_date", ascending=False).iloc[0]


def get_employee_appraisals(employee_id: str) -> pd.DataFrame:
    df = load_appraisals()
    emp = df[df["employee_id"] == employee_id.strip()].copy()
    return emp.sort_values("appraisal_date", ascending=False) if not emp.empty else pd.DataFrame()


def get_employee_feedback(employee_id: str) -> pd.DataFrame:
    df = load_feedback()
    emp = df[df["employee_id"] == employee_id.strip()].copy()
    return emp.sort_values("feedback_date", ascending=False) if not emp.empty else pd.DataFrame()


def employee_id_exists(employee_id: str) -> bool:
    return employee_id.strip() in load_employees()["employee_id"].values


def get_all_departments() -> list:
    return sorted(load_employees()["department"].dropna().unique().tolist())


def get_all_designations() -> list:
    return sorted(load_employees()["designation"].dropna().unique().tolist())
