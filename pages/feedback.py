"""
pages/feedback.py — Feedback logging and history page for Capacity Connect.
Minimalist, elegant light-grey aesthetic without emojis or gradients.
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
    load_employees, load_feedback,
    save_feedback, employee_id_exists,
)
from modules.ui_theme import render_html_table

FEEDBACK_TYPES = ["Positive", "Improvement Needed", "General"]
FEEDBACK_PAGE  = 10


def show_feedback():
    if not st.session_state.get("_dock_rendered"):
        from modules.ui_theme import render_top_dock, apply_theme
        apply_theme(st.session_state.get("theme_mode", "light"))
        render_top_dock("feedback")

    st.markdown("""
    <div class="page-header">
      <div class="page-header-title">Employee Feedback Log</div>
      <div class="page-header-sub">Submit structured peer or managerial feedback and maintain historical observations</div>
    </div>
    """, unsafe_allow_html=True)

    employees_df = load_employees()
    if employees_df.empty:
        st.error("No employee records found in dataset.")
        return

    form_col, hist_col = st.columns([3, 2])

    # ── Feedback Form ──────────────────────────────────────────────────────────
    with form_col:
        st.markdown("#### Submit Feedback")

        with st.form("feedback_form", clear_on_submit=True):
            emp_opts = [
                f"{r['employee_id']} — {r['name']} ({r['department']})"
                for _, r in employees_df.iterrows()
            ]
            selected = st.selectbox("Employee *", emp_opts)

            col_type, col_date = st.columns(2)
            with col_type:
                fb_type = st.selectbox("Feedback Nature *", FEEDBACK_TYPES)
            with col_date:
                fb_date = st.date_input("Date *", value=date.today(), max_value=date.today())

            comments = st.text_area(
                "Feedback Comments * (minimum 10 characters)",
                placeholder="Provide objective, actionable feedback regarding project delivery, work quality, or team collaboration...",
                height=140,
                max_chars=500,
            )

            char_count = len(comments.strip()) if comments else 0
            char_color = "#047857" if char_count >= 10 else "#be123c"
            st.markdown(
                f'<div style="text-align:right; font-size:0.75rem; color:{char_color};">'
                f'{char_count}/500 characters'
                f'{" (Requirement met)" if char_count >= 10 else " (10 characters minimum)"}</div>',
                unsafe_allow_html=True,
            )

            submitted = st.form_submit_button("Record Feedback", use_container_width=True)

        if submitted:
            emp_id = selected.split("—")[0].strip()
            errors = []
            if not employee_id_exists(emp_id):
                errors.append(f"Employee '{emp_id}' not found.")
            if len(comments.strip()) < 10:
                errors.append("Comments must contain at least 10 characters.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                ok, msg = save_feedback(
                    employee_id=emp_id,
                    feedback_type=fb_type,
                    comments=comments.strip(),
                    feedback_date=fb_date.strftime("%Y-%m-%d"),
                )
                if ok:
                    st.success(f"Feedback entry recorded for employee {emp_id}.")
                else:
                    st.error(msg)

        # ── Guidelines ────────────────────────────────────────────────────────
        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("#### Evaluation Standards")
        for ft, desc in [
            ("Positive", "Document recognized achievements, high reliability, and exemplary work contributions."),
            ("Improvement Needed", "Provide constructive critique pinpointing specific developmental needs."),
            ("General", "Log general operational observations, transitions, or informational milestones."),
        ]:
            st.markdown(f"""
            <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-left:3px solid var(--accent-bg);
                        padding:10px 14px; border-radius:0 6px 6px 0; margin-bottom:8px;">
              <span style="font-weight:600; color:var(--text-main); font-size:0.84rem;">{ft}</span><br/>
              <span style="color:var(--text-muted); font-size:0.8rem;">{desc}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── Recent Feedback Feed ──────────────────────────────────────────────────
    with hist_col:
        st.markdown("#### Recent Entries")
        all_fb   = load_feedback().sort_values("feedback_date", ascending=False)
        name_map = employees_df.set_index("employee_id")["name"].to_dict()

        if all_fb.empty:
            st.info("No feedback records logged yet.")
        else:
            for _, row in all_fb.head(7).iterrows():
                fname  = name_map.get(row["employee_id"], row["employee_id"])
                fdate  = row["feedback_date"].strftime("%d %b %Y") if hasattr(row["feedback_date"],"strftime") else str(row["feedback_date"])
                trunc  = str(row["comments"])[:90] + ("..." if len(str(row["comments"])) > 90 else "")
                st.markdown(f"""
                <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-left:3px solid var(--accent-bg);
                            padding:10px 14px; border-radius:0 6px 6px 0; margin-bottom:8px;">
                  <div style="display:flex; justify-content:space-between;">
                    <span style="color:var(--text-main); font-weight:600; font-size:0.85rem;">{row['employee_id']} · {fname}</span>
                    <span style="color:var(--text-muted); font-size:0.75rem;">{fdate}</span>
                  </div>
                  <div style="color:var(--text-muted); font-size:0.78rem; font-weight:500; margin-top:2px;">Type: {row['feedback_type']}</div>
                  <div style="color:var(--text-main); font-size:0.82rem; margin-top:4px;">{trunc}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── Full History Table ─────────────────────────────────────────────────────
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("#### Complete Feedback Ledger")

    all_fb_full = load_feedback()
    if all_fb_full.empty:
        st.info("No feedback records logged yet.")
        return

    merged = all_fb_full.merge(
        employees_df[["employee_id","name","department"]], on="employee_id", how="left"
    )
    merged["feedback_date"] = merged["feedback_date"].apply(
        lambda x: x.strftime("%d %b %Y") if hasattr(x,"strftime") else str(x))
    disp = merged[["feedback_id","employee_id","name","department",
                   "feedback_date","feedback_type","comments"]].copy()
    disp.columns = ["Record ID","Employee ID","Name","Department","Date","Nature","Comments"]

    fa, fb2 = st.columns([3, 1])
    with fa:
        srch = st.text_input("Search", placeholder="Search records by name or employee ID...", label_visibility="collapsed")
    with fb2:
        type_f = st.selectbox("Filter Nature", ["All Types"] + FEEDBACK_TYPES, label_visibility="collapsed")

    if srch:
        disp = disp[disp["Name"].str.contains(srch, case=False, na=False)
                    | disp["Employee ID"].str.contains(srch, case=False, na=False)]
    if type_f != "All Types":
        disp = disp[disp["Nature"] == type_f]

    # Paginate
    if "fb_page" not in st.session_state:
        st.session_state.fb_page = 0
    total_fb = len(disp)
    total_fb_pages = max(1, (total_fb + FEEDBACK_PAGE - 1) // FEEDBACK_PAGE)
    fb_page_idx = min(st.session_state.fb_page, total_fb_pages - 1)

    pa, pb, pc2 = st.columns([1, 1, 4])
    with pa:
        if st.button("← Previous", disabled=(fb_page_idx==0), key="fb_prev"):
            st.session_state.fb_page -= 1
            st.rerun()
    with pb:
        if st.button("Next →", disabled=(fb_page_idx>=total_fb_pages-1), key="fb_next"):
            st.session_state.fb_page += 1
            st.rerun()
    with pc2:
        s_fb = fb_page_idx * FEEDBACK_PAGE + 1
        e_fb = min(s_fb + FEEDBACK_PAGE - 1, total_fb)
        st.caption(f"Showing {s_fb}–{e_fb} of {total_fb} records · Page {fb_page_idx+1} of {total_fb_pages}")

    page_disp = disp.iloc[fb_page_idx*FEEDBACK_PAGE:(fb_page_idx+1)*FEEDBACK_PAGE]
    render_html_table(page_disp.reset_index(drop=True))


if __name__ == "__main__":
    import os, sys
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)
    from modules.ui_theme import apply_theme
    apply_theme()
    show_feedback()
