"""
pages/appraisal.py — Add Appraisal page for Capacity Connect.
Clean, elegant light-grey aesthetic without emojis or gradients.
"""

import sys
import os
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st
import pandas as pd
from datetime import date
from modules.data_manager import (
    load_employees, load_appraisals,
    save_appraisal, employee_id_exists,
)
from modules.performance import classify_performance
from modules.ui_theme import render_html_table


def _preview_card(score: float):
    cat = classify_performance(score)
    cls = "badge-na"
    if cat == "Top Notch":
        cls = "badge-top"
        tip = "High achievement benchmark. Candidate for advanced training and leadership assignments."
    elif cat == "Mediocre":
        cls = "badge-mid"
        tip = "Meets expected operational standards. Targeted skill development plan advised."
    elif cat == "Below Average":
        cls = "badge-low"
        tip = "Below benchmark threshold. Structured performance improvement plan required."
    else:
        tip = "Set score between 0 and 100."

    st.markdown(f"""
    <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:8px; padding:16px 18px; margin-top:4px;">
      <div style="font-size:0.75rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.05em; font-weight:600; margin-bottom:8px;">
        Automatic Classification
      </div>
      <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
        <span class="{cls}" style="font-size:0.85rem; padding:4px 12px;">{cat}</span>
        <span style="font-size:1.1rem; font-weight:700; color:var(--text-main);">Score: {score:.1f}</span>
      </div>
      <div style="font-size:0.8rem; color:var(--text-muted); line-height:1.4;">{tip}</div>
    </div>
    """, unsafe_allow_html=True)


def show_appraisal():
    if not st.session_state.get("_dock_rendered"):
        from modules.ui_theme import render_top_dock, apply_theme
        apply_theme(st.session_state.get("theme_mode", "light"))
        render_top_dock("appraisal")

    st.markdown("""
    <div class="page-header">
      <div class="page-header-title">Record Performance Appraisal</div>
      <div class="page-header-sub">Submit formal performance assessment ratings — classifications are calculated automatically</div>
    </div>
    """, unsafe_allow_html=True)

    employees_df = load_employees()
    if employees_df.empty:
        st.error("No employee records found in dataset.")
        return

    if "ap_score_preview" not in st.session_state:
        st.session_state.ap_score_preview = 75.0

    form_col, right_col = st.columns([3, 2])

    with right_col:
        st.markdown("#### Classification Preview")
        _preview_card(st.session_state.ap_score_preview)

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("#### Recent Submissions")
        recent = load_appraisals().sort_values("appraisal_date", ascending=False).head(5)
        if not recent.empty:
            name_map = employees_df.set_index("employee_id")["name"].to_dict()
            for _, row in recent.iterrows():
                cat = classify_performance(row["performance_score"])
                cls = "badge-na"
                if cat == "Top Notch":
                    cls = "badge-top"
                elif cat == "Mediocre":
                    cls = "badge-mid"
                elif cat == "Below Average":
                    cls = "badge-low"

                emp_name = name_map.get(row["employee_id"], row["employee_id"])
                d = row["appraisal_date"].strftime("%d %b %Y") if hasattr(row["appraisal_date"],"strftime") else str(row["appraisal_date"])
                st.markdown(f"""
                <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-left:3px solid var(--accent-bg);
                            padding:9px 12px; border-radius:0 6px 6px 0; margin-bottom:6px;">
                  <div style="display:flex; justify-content:space-between;">
                    <span style="color:var(--text-main); font-weight:600; font-size:0.85rem;">
                      {row['employee_id']} · {emp_name}
                    </span>
                    <span style="color:var(--text-muted); font-size:0.75rem;">{d}</span>
                  </div>
                  <div style="margin-top:3px; display:flex; align-items:center; gap:8px;">
                    <span style="font-weight:700; color:var(--text-main); font-size:0.88rem;">{row['performance_score']:.1f}</span>
                    <span class="{cls}" style="font-size:0.72rem; padding:1px 8px;">{cat}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No prior appraisal records available.")

    with form_col:
        st.markdown("#### Appraisal Details")

        with st.form("appraisal_form", clear_on_submit=True):
            emp_opts = [
                f"{r['employee_id']} — {r['name']} ({r['department']})"
                for _, r in employees_df.iterrows()
            ]
            selected = st.selectbox("Employee *", emp_opts)

            ap_date = st.date_input(
                "Appraisal Date *",
                value=date.today(), max_value=date.today(),
            )

            score = st.slider(
                "Performance Score (0 – 100) *",
                min_value=0, max_value=100, value=75, step=1,
                help="Adjust to compute category rating in real-time.",
            )

            remarks = st.text_area(
                "Evaluator Remarks",
                placeholder="Detail specific accomplishments, areas of excellence, and targeted development goals...",
                height=130,
            )

            submitted = st.form_submit_button("Submit Appraisal Record", use_container_width=True)

        st.session_state.ap_score_preview = float(score)

        if submitted:
            emp_id = selected.split("—")[0].strip()
            errors = []
            if not employee_id_exists(emp_id):
                errors.append(f"Employee record '{emp_id}' not found.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                ok, msg = save_appraisal(
                    employee_id=emp_id,
                    appraisal_date=ap_date.strftime("%Y-%m-%d"),
                    performance_score=float(score),
                    remarks=remarks.strip() or "Standard appraisal record.",
                )
                if ok:
                    cat = classify_performance(float(score))
                    st.success(f"Appraisal successfully recorded for {emp_id}.")
                    st.markdown(f"""
                    <div style="background:var(--bg-subtle); border:1px solid var(--border-subtle); border-radius:6px; padding:12px; margin-top:8px;">
                      <div style="font-size:0.9rem; font-weight:600; color:var(--text-main);">Assigned Category: {cat} (Score: {score:.0f})</div>
                      <div style="color:var(--text-muted); font-size:0.8rem; margin-top:2px;">Employee master record and dashboard metrics have been updated.</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error(msg)

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Full History Table ─────────────────────────────────────────────────────
    st.markdown("#### Appraisal Ledger")

    all_ap  = load_appraisals()
    all_emp = load_employees()

    if all_ap.empty:
        st.info("No appraisal entries recorded yet.")
        return

    merged = all_ap.merge(
        all_emp[["employee_id","name","department"]], on="employee_id", how="left"
    )
    merged["category"] = merged["performance_score"].apply(classify_performance)
    merged["appraisal_date"] = merged["appraisal_date"].apply(
        lambda x: x.strftime("%d %b %Y") if hasattr(x,"strftime") else str(x)
    )
    disp = merged[["appraisal_id","employee_id","name","department",
                   "appraisal_date","performance_score","category","remarks"]].copy()
    disp.columns = ["Record ID","Employee ID","Name","Department","Date","Score","Classification","Remarks"]

    s1, s2 = st.columns([3, 1])
    with s1:
        search = st.text_input("Filter", placeholder="Filter records by name or ID...",
                               label_visibility="collapsed")
    with s2:
        cat_f = st.selectbox("Category", ["All Classifications","Top Notch","Mediocre","Below Average"],
                             label_visibility="collapsed")

    if search:
        disp = disp[disp["Name"].str.contains(search, case=False, na=False)
                    | disp["Employee ID"].str.contains(search, case=False, na=False)]
    if cat_f != "All Classifications":
        disp = disp[disp["Classification"] == cat_f]

    st.caption(f"Showing {len(disp)} appraisal records")
    render_html_table(disp.reset_index(drop=True), height=340)


if __name__ == "__main__":
    import os, sys
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)
    from modules.ui_theme import apply_theme
    apply_theme()
    show_appraisal()
