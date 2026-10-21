"""
pages/employees.py — Employee directory with pagination and clean typography.
Minimalist, elegant light-grey aesthetic without emojis or gradients.
"""

import sys
import os
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st
import pandas as pd
from modules.performance import (
    get_enriched_employees, classify_performance,
    CATEGORY_TOP_NOTCH, CATEGORY_MEDIOCRE, CATEGORY_BELOW_AVERAGE,
)
from modules.data_manager import (
    get_employee_appraisals, get_employee_feedback,
    get_all_departments, get_all_designations,
)
from modules.recommendations import get_suggestions_for_employee
from modules.ui_theme import render_html_table

PAGE_SIZE = 10


def _cat_badge(cat: str) -> str:
    cls = "badge-na"
    if cat == "Top Notch":
        cls = "badge-top"
    elif cat == "Mediocre":
        cls = "badge-mid"
    elif cat == "Below Average":
        cls = "badge-low"
    return f'<span class="{cls}">{cat}</span>'


def _avatar(name: str) -> str:
    initials = "".join(w[0].upper() for w in name.split()[:2])
    return f'<div class="avatar">{initials}</div>'


def show_employees():
    if not st.session_state.get("_dock_rendered"):
        from modules.ui_theme import render_top_dock, apply_theme
        apply_theme(st.session_state.get("theme_mode", "light"))
        render_top_dock("employees")

    st.markdown("""
    <div class="page-header">
      <div class="page-header-title">Employee Directory</div>
      <div class="page-header-sub">Search, inspect, and manage individual employee performance records</div>
    </div>
    """, unsafe_allow_html=True)

    enriched = get_enriched_employees()

    # ── Filters ───────────────────────────────────────────────────────────────
    f1, f2, f3, f4 = st.columns([2, 2, 2, 2])
    with f1:
        search = st.text_input("Search", placeholder="Search name or ID...", label_visibility="collapsed")
    with f2:
        dept_f = st.selectbox("Department", ["All Departments"] + get_all_departments(), label_visibility="collapsed")
    with f3:
        desig_f= st.selectbox("Designation", ["All Roles"] + get_all_designations(), label_visibility="collapsed")
    with f4:
        cat_f  = st.selectbox("Category",
            ["All Categories", "Top Notch", "Mediocre", "Below Average", "Not Appraised"],
            label_visibility="collapsed")

    filtered = enriched.copy()
    if search:
        mask = (filtered["name"].str.contains(search, case=False, na=False)
                | filtered["employee_id"].str.contains(search, case=False, na=False))
        filtered = filtered[mask]
    if dept_f  != "All Departments": filtered = filtered[filtered["department"]          == dept_f]
    if desig_f != "All Roles":       filtered = filtered[filtered["designation"]         == desig_f]
    if cat_f   != "All Categories":  filtered = filtered[filtered["performance_category"] == cat_f]

    total = len(filtered)

    # ── Pagination ────────────────────────────────────────────────────────────
    if "emp_page" not in st.session_state:
        st.session_state.emp_page = 0

    filter_key = f"{search}|{dept_f}|{desig_f}|{cat_f}"
    if st.session_state.get("_last_emp_filter") != filter_key:
        st.session_state.emp_page = 0
        st.session_state["_last_emp_filter"] = filter_key

    total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page_idx    = min(st.session_state.emp_page, total_pages - 1)

    caption_col, pag_col = st.columns([3, 2])
    with caption_col:
        start = page_idx * PAGE_SIZE + 1
        end   = min(start + PAGE_SIZE - 1, total)
        st.caption(f"Showing {start}–{end} of {total} employees · Page {page_idx+1} of {total_pages}")
    with pag_col:
        pc1, pc2, pc3 = st.columns([1, 1.2, 1])
        with pc1:
            if st.button("← Previous", disabled=(page_idx == 0), use_container_width=True, key="emp_prev_btn"):
                st.session_state.emp_page -= 1
                st.rerun()
        with pc2:
            st.markdown(f"<div style='text-align:center; padding:7px 0; color:var(--text-muted); font-size:0.85rem; font-weight:600;'>"
                        f"{page_idx+1} / {total_pages}</div>", unsafe_allow_html=True)
        with pc3:
            if st.button("Next →", disabled=(page_idx >= total_pages-1), use_container_width=True, key="emp_next_btn"):
                st.session_state.emp_page += 1
                st.rerun()

    page_rows = filtered.iloc[page_idx*PAGE_SIZE : (page_idx+1)*PAGE_SIZE]

    if page_rows.empty:
        st.info("No employee records found matching your filter criteria.")
        return

    # ── Employee Cards ────────────────────────────────────────────────────────
    for _, row in page_rows.iterrows():
        score_disp = f"{row['latest_score']:.1f}" if pd.notna(row.get("latest_score")) else "—"
        cat        = row["performance_category"]

        date_disp = (
            row["latest_appraisal_date"].strftime("%d %b %Y")
            if pd.notna(row.get("latest_appraisal_date"))
            and hasattr(row["latest_appraisal_date"], "strftime")
            else "Not appraised"
        )

        header = f"{row['employee_id']} · {row['name']} · {row['department']} · Score: {score_disp} · {cat}"

        with st.expander(header, expanded=False):
            tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Appraisal History", "Feedback Log", "Recommendations"])

            # ── Overview Tab ─────────────────────────────────────────────────
            with tab1:
                pr1, pr2 = st.columns(2)
                with pr1:
                    st.markdown(
                        f'<div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">'
                        f'{_avatar(row["name"])}'
                        f'<div><div style="font-size:1.05rem; font-weight:600; color:var(--text-main);">'
                        f'{row["name"]}</div>'
                        f'<div style="font-size:0.8rem; color:var(--text-muted);">'
                        f'{row["designation"]}</div></div></div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(f"**Employee ID:** `{row['employee_id']}`")
                    st.markdown(f"**Department:** {row['department']}")
                    st.markdown(f"**Email:** {row['email']}")
                    joining = (row["joining_date"].strftime("%d %b %Y")
                               if pd.notna(row.get("joining_date"))
                               and hasattr(row["joining_date"],"strftime") else "—")
                    st.markdown(f"**Date Joined:** {joining}")
                with pr2:
                    st.markdown(f"**Current Score:** `{score_disp}`")
                    st.markdown(f"**Appraisal Date:** {date_disp}")
                    st.markdown(
                        f"**Classification:** {_cat_badge(cat)}",
                        unsafe_allow_html=True,
                    )
                    if pd.notna(row.get("latest_remarks")):
                        st.markdown(f"**Latest Remarks:** *{row['latest_remarks']}*")

            # ── Appraisals Tab ────────────────────────────────────────────────
            with tab2:
                ap_df = get_employee_appraisals(row["employee_id"])
                if ap_df.empty:
                    st.info("No historical appraisals recorded for this employee.")
                else:
                    disp = ap_df[["appraisal_id","appraisal_date","performance_score","remarks"]].copy()
                    disp["appraisal_date"] = disp["appraisal_date"].apply(
                        lambda x: x.strftime("%d %b %Y") if hasattr(x,"strftime") else str(x))
                    disp["category"] = disp["performance_score"].apply(classify_performance)
                    disp.columns = ["Record ID", "Date", "Score", "Remarks", "Classification"]
                    render_html_table(disp.reset_index(drop=True))

            # ── Feedback Tab ──────────────────────────────────────────────────
            with tab3:
                fb_df = get_employee_feedback(row["employee_id"])
                if fb_df.empty:
                    st.info("No feedback entries submitted for this employee yet.")
                else:
                    for _, fb in fb_df.iterrows():
                        fdate = fb["feedback_date"].strftime("%d %b %Y") if hasattr(fb["feedback_date"],"strftime") else str(fb["feedback_date"])
                        st.markdown(f"""
                        <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-left:3px solid var(--accent-bg);
                                    padding:10px 14px; border-radius:0 6px 6px 0; margin-bottom:8px;">
                          <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
                            <span style="font-weight:600; font-size:0.8rem; color:var(--text-main);">{fb['feedback_type']}</span>
                            <span style="font-size:0.75rem; color:var(--text-muted);">{fdate}</span>
                          </div>
                          <div style="color:var(--text-main); font-size:0.86rem;">{fb['comments']}</div>
                        </div>
                        """, unsafe_allow_html=True)

            # ── Suggestions Tab ───────────────────────────────────────────────
            with tab4:
                res = get_suggestions_for_employee(row["employee_id"])
                if res.get("error"):
                    st.error(res["error"])
                else:
                    cat_s = res["category"]
                    st.markdown(f"**Classification:** {_cat_badge(cat_s)}", unsafe_allow_html=True)
                    if res["score"] is not None:
                        st.markdown(f"**Score Reference:** {res['score']:.1f}")
                    st.markdown("<hr/>", unsafe_allow_html=True)
                    for s in res["category_suggestions"]:
                        st.markdown(f"""
                        <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:6px;
                                    padding:12px 14px; margin-bottom:8px;">
                          <div style="font-weight:600; color:var(--text-main); font-size:0.9rem;">{s['title']}</div>
                          <div style="color:var(--text-main); font-size:0.84rem; margin-top:3px;">{s['detail']}</div>
                          <div style="color:var(--text-muted); font-size:0.78rem; margin-top:5px;">Rationale: {s['reason']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    if res.get("remark_suggestions"):
                        st.markdown("**Remarks-driven observations:**")
                        for rs in res["remark_suggestions"]:
                            st.markdown(f"- {rs}")


if __name__ == "__main__":
    import os, sys
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)
    from modules.ui_theme import apply_theme
    apply_theme()
    show_employees()
