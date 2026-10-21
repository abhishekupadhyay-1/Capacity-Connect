"""
pages/reports.py — Reports & Analytics page for Capacity Connect.
Clean, elegant light-grey aesthetic without emojis or gradients.
"""

import sys
import os
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st
import pandas as pd
from datetime import datetime
from modules.performance import (
    get_dashboard_stats,
    get_enriched_employees,
    classify_performance,
    CATEGORY_TOP_NOTCH,
    CATEGORY_MEDIOCRE,
    CATEGORY_BELOW_AVERAGE,
    CATEGORY_NOT_APPRAISED,
)
from modules.data_manager import load_employees, load_appraisals
from modules.ui_theme import render_html_table


def _cat_badge(cat: str) -> str:
    cls = "badge-na"
    if cat == "Top Notch":
        cls = "badge-top"
    elif cat == "Mediocre":
        cls = "badge-mid"
    elif cat == "Below Average":
        cls = "badge-low"
    return f'<span class="{cls}">{cat}</span>'


def _kpi(col, value, label):
    col.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-value">{value}</div>
      <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def show_reports():
    if not st.session_state.get("_dock_rendered"):
        from modules.ui_theme import render_top_dock, apply_theme
        apply_theme(st.session_state.get("theme_mode", "light"))
        render_top_dock("reports")

    st.markdown("""
    <div class="page-header">
      <div class="page-header-title">Reports & Executive Analytics</div>
      <div class="page-header-sub">Comprehensive performance analysis, department rankings, and data export</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Compiling reports..."):
        stats = get_dashboard_stats()
        enriched = get_enriched_employees()

    # ── Summary KPI Row (6 Columns) ───────────────────────────────────────────
    s1, s2, s3, s4, s5, s6 = st.columns(6)
    total_emp = stats["total_employees"]
    not_app = stats["not_appraised"]
    appraised_cnt = total_emp - not_app
    appraisal_rate = (appraised_cnt / total_emp * 100) if total_emp > 0 else 0.0

    _kpi(s1, total_emp, "Total Staff")
    _kpi(s2, f"{appraised_cnt} ({appraisal_rate:.0f}%)", "Appraised")
    _kpi(s3, f"{stats['avg_score']:.1f}", "Average Score")
    _kpi(s4, stats["top_notch"], "Top Notch (≥80)")
    _kpi(s5, stats["mediocre"], "Mediocre (50–79)")
    _kpi(s6, stats["below_average"], "Below Average (<50)")

    st.markdown(
        f"<div style='font-size:0.75rem; color:var(--text-muted); text-align:right; margin-top:8px;'>"
        f"Coverage: {appraised_cnt} of {total_emp} appraised ({appraisal_rate:.1f}%) · "
        f"{not_app} pending initial appraisal</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── CSV Export Section ────────────────────────────────────────────────────
    exp_col1, exp_col2 = st.columns([3, 1])
    with exp_col1:
        st.markdown("#### Export Consolidated Records")
        st.caption("Download the complete employee performance dataset including current ratings, scores, and evaluation remarks.")

    export_df = enriched.copy()
    export_df["latest_appraisal_date"] = export_df["latest_appraisal_date"].apply(
        lambda x: x.strftime("%Y-%m-%d") if hasattr(x, "strftime") and pd.notna(x) else "Not Appraised"
    )
    export_cols = [
        "employee_id", "name", "department", "designation", "email",
        "latest_score", "performance_category", "latest_appraisal_date", "latest_remarks"
    ]
    export_data = export_df[[c for c in export_cols if c in export_df.columns]].rename(columns={
        "employee_id": "Employee ID",
        "name": "Employee Name",
        "department": "Department",
        "designation": "Designation",
        "email": "Email Address",
        "latest_score": "Latest Score",
        "performance_category": "Performance Category",
        "latest_appraisal_date": "Last Appraisal Date",
        "latest_remarks": "Remarks"
    })
    csv_bytes = export_data.to_csv(index=False).encode("utf-8")

    with exp_col2:
        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        st.download_button(
            label="Download CSV Dataset",
            data=csv_bytes,
            file_name=f"capacity_connect_records_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Top 5 & Bottom 5 Rankings ──────────────────────────────────────────────
    rank_col1, rank_col2 = st.columns(2)
    appraised_df = enriched.dropna(subset=["latest_score"]).copy()

    with rank_col1:
        st.markdown("#### Top 5 Performers")
        if not appraised_df.empty:
            top5 = appraised_df.sort_values(by=["latest_score", "name"], ascending=[False, True]).head(5)
            for idx, (_, r) in enumerate(top5.iterrows(), 1):
                cat = r["performance_category"]
                st.markdown(f"""
                <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-left:3px solid #059669;
                            border-radius:0 6px 6px 0; padding:12px 16px; margin-bottom:8px;
                            display:flex; justify-content:space-between; align-items:center;">
                  <div>
                    <div style="font-weight:600; color:var(--text-main); font-size:0.92rem;">
                      #{idx} {r['name']} <span style="font-size:0.75rem; color:var(--text-muted);">({r['employee_id']})</span>
                    </div>
                    <div style="font-size:0.78rem; color:var(--text-muted); margin-top:2px;">
                      {r['designation']} · {r['department']}
                    </div>
                  </div>
                  <div style="text-align:right;">
                    <div style="font-size:1.15rem; font-weight:700; color:var(--text-main);">{r['latest_score']:.1f}</div>
                    <div style="margin-top:2px;">{_cat_badge(cat)}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No appraisal data available.")

    with rank_col2:
        st.markdown("#### Bottom 5 Performers (Development Priority)")
        if not appraised_df.empty:
            bottom5 = appraised_df.sort_values(by=["latest_score", "name"], ascending=[True, True]).head(5)
            for idx, (_, r) in enumerate(bottom5.iterrows(), 1):
                cat = r["performance_category"]
                st.markdown(f"""
                <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-left:3px solid #dc2626;
                            border-radius:0 6px 6px 0; padding:12px 16px; margin-bottom:8px;
                            display:flex; justify-content:space-between; align-items:center;">
                  <div>
                    <div style="font-weight:600; color:var(--text-main); font-size:0.92rem;">
                      #{idx} {r['name']} <span style="font-size:0.75rem; color:var(--text-muted);">({r['employee_id']})</span>
                    </div>
                    <div style="font-size:0.78rem; color:var(--text-muted); margin-top:2px;">
                      {r['designation']} · {r['department']}
                    </div>
                  </div>
                  <div style="text-align:right;">
                    <div style="font-size:1.15rem; font-weight:700; color:var(--text-main);">{r['latest_score']:.1f}</div>
                    <div style="margin-top:2px;">{_cat_badge(cat)}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No appraisal data available.")

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Department Scorecard Table ─────────────────────────────────────────────
    st.markdown("#### Department Scorecard")
    st.caption("Aggregated performance metrics and benchmark leaders categorized by department.")

    departments = sorted(enriched["department"].dropna().unique())
    if departments:
        scorecard_rows = []
        for dept in departments:
            dept_emp = enriched[enriched["department"] == dept]
            emp_count = len(dept_emp)
            dept_appraised = dept_emp.dropna(subset=["latest_score"])
            appraised_here = len(dept_appraised)

            if not dept_appraised.empty:
                avg_s = dept_appraised["latest_score"].mean()
                top_cat = dept_appraised["performance_category"].mode()[0]
                top_scorer_row = dept_appraised.sort_values(by=["latest_score", "name"], ascending=[False, True]).iloc[0]
                top_scorer_name = f"{top_scorer_row['name']} ({top_scorer_row['latest_score']:.1f})"
            else:
                avg_s = 0.0
                top_cat = "Not Appraised"
                top_scorer_name = "—"

            scorecard_rows.append({
                "Department": dept,
                "Employee Count": emp_count,
                "Appraised": appraised_here,
                "Average Score": round(avg_s, 2),
                "Top Category": top_cat,
                "Highest Scorer": top_scorer_name,
            })

        scorecard_df = pd.DataFrame(scorecard_rows).sort_values("Average Score", ascending=False)
        render_html_table(scorecard_df.reset_index(drop=True))
    else:
        st.info("Department analytics will appear here once appraisals are recorded.")


if __name__ == "__main__":
    import os, sys
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)
    from modules.ui_theme import apply_theme
    apply_theme()
    show_reports()
