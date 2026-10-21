"""
pages/suggestions.py — Suggestions & Recommendations page.
Clean, elegant light-grey aesthetic without emojis or gradients.
"""

import sys
import os
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import streamlit as st
import pandas as pd
from modules.performance import (
    get_enriched_employees,
    CATEGORY_TOP_NOTCH, CATEGORY_MEDIOCRE,
    CATEGORY_BELOW_AVERAGE, CATEGORY_NOT_APPRAISED,
)
from modules.recommendations import SUGGESTIONS, get_remark_based_suggestions
from modules.data_manager import load_employees


def _cat_badge(cat):
    cls = "badge-na"
    if cat == "Top Notch":
        cls = "badge-top"
    elif cat == "Mediocre":
        cls = "badge-mid"
    elif cat == "Below Average":
        cls = "badge-low"
    return f'<span class="{cls}">{cat}</span>'


def _render_suggestions_inline(row, category_suggestions, remark_suggestions):
    """Render suggestions cleanly without emoji clutter."""
    cat   = row["performance_category"]
    score = row.get("latest_score")
    score_txt = f"{score:.1f}" if pd.notna(score) else "Not appraised"

    st.markdown(
        f'**Category:** {_cat_badge(cat)}'
        f'&nbsp;&nbsp;<span style="color:var(--text-muted); font-size:0.86rem;">Latest Score: <b>{score_txt}</b></span>',
        unsafe_allow_html=True,
    )

    remarks = row.get("latest_remarks","")
    if pd.notna(remarks) and remarks:
        st.markdown(f"**Appraisal Remarks:** *{str(remarks)}*")

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("#### Actionable Recommendations")

    for i, s in enumerate(category_suggestions, 1):
        st.markdown(f"""
        <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:6px;
                    padding:14px 16px; margin-bottom:10px;">
          <div style="font-weight:600; color:var(--text-main); font-size:0.92rem;">{i}. {s['title']}</div>
          <div style="color:var(--text-main); font-size:0.86rem; margin-top:4px;">{s['detail']}</div>
          <div style="color:var(--text-muted); font-size:0.78rem; margin-top:6px;">Rationale: {s['reason']}</div>
        </div>
        """, unsafe_allow_html=True)

    if remark_suggestions:
        st.markdown("#### Tailored Growth Actions")
        for rs in remark_suggestions:
            st.markdown(f"""
            <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-left:3px solid var(--accent-bg);
                        border-radius:0 6px 6px 0; padding:10px 14px; margin-bottom:8px;">
              <span style="color:var(--text-main); font-size:0.85rem;">{rs}</span>
            </div>
            """, unsafe_allow_html=True)


def show_suggestions():
    if not st.session_state.get("_dock_rendered"):
        from modules.ui_theme import render_top_dock, apply_theme
        apply_theme(st.session_state.get("theme_mode", "light"))
        render_top_dock("suggestions")

    st.markdown("""
    <div class="page-header">
      <div class="page-header-title">Development Suggestions & Action Plans</div>
      <div class="page-header-sub">Objective improvement recommendations derived from performance appraisal scores and remark patterns</div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "View mode",
        ["Individual Employee", "Browse by Category"],
        horizontal=True,
        label_visibility="collapsed",
    )
    st.markdown("")

    enriched = get_enriched_employees()

    if mode == "Individual Employee":
        employees_df = load_employees()
        emp_opts = [
            f"{r['employee_id']} — {r['name']} ({r['department']})"
            for _, r in employees_df.iterrows()
        ]
        col_sel, col_btn = st.columns([4, 1])
        with col_sel:
            selected = st.selectbox("Employee", emp_opts, label_visibility="collapsed")
        with col_btn:
            go = st.button("Generate Plan", type="primary", use_container_width=True)

        if go:
            emp_id = selected.split("—")[0].strip()
            emp_row = enriched[enriched["employee_id"] == emp_id]

            if emp_row.empty:
                st.error(f"Employee {emp_id} not found in database.")
                return

            row    = emp_row.iloc[0]
            cat    = row["performance_category"]
            remarks= str(row.get("latest_remarks","")) if pd.notna(row.get("latest_remarks")) else ""
            cat_suggs = SUGGESTIONS.get(cat, [])
            rem_suggs = get_remark_based_suggestions(remarks)

            score = row.get("latest_score")
            score_txt = f"{score:.1f}" if pd.notna(score) else "Not Appraised"
            st.markdown(f"""
            <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:8px; padding:18px; margin-bottom:18px;">
              <div style="font-size:1.15rem; font-weight:700; color:var(--text-main);">
                {row['name']} · {emp_id}
              </div>
              <div style="color:var(--text-muted); font-size:0.84rem; margin-top:3px;">
                {row['designation']} · {row['department']}
              </div>
              <div style="margin-top:10px;">
                {_cat_badge(cat)}
                &nbsp;&nbsp;
                <span style="color:var(--text-muted); font-size:0.85rem;">Score: <b>{score_txt}</b></span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            _render_suggestions_inline(row, cat_suggs, rem_suggs)

    else:
        cat_options = ["All Categories", CATEGORY_TOP_NOTCH, CATEGORY_MEDIOCRE,
                       CATEGORY_BELOW_AVERAGE, CATEGORY_NOT_APPRAISED]
        cat_f = st.selectbox("Filter Category", cat_options, label_visibility="collapsed")

        subset = enriched if cat_f == "All Categories" else enriched[enriched["performance_category"] == cat_f]

        if subset.empty:
            st.info("No employee records found in this category.")
            return

        st.caption(f"Showing {len(subset)} employee profiles")

        for _, row in subset.iterrows():
            score = row.get("latest_score")
            score_disp = f"{score:.1f}" if pd.notna(score) else "—"
            cat = row["performance_category"]

            with st.expander(
                f"{row['employee_id']} · {row['name']} · {cat} · Score: {score_disp}",
                expanded=False,
            ):
                remarks = str(row.get("latest_remarks","")) if pd.notna(row.get("latest_remarks")) else ""
                cat_suggs = SUGGESTIONS.get(cat, [])
                rem_suggs = get_remark_based_suggestions(remarks)
                _render_suggestions_inline(row, cat_suggs, rem_suggs)

    # ── Category Legend ────────────────────────────────────────────────────────
    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown("#### Category Benchmark Criteria")
    leg1, leg2, leg3, leg4 = st.columns(4)
    for col, cat, score_range, actions in [
        (leg1, CATEGORY_TOP_NOTCH,    "80–100", "Leadership tracks, advanced certifications, and team mentoring."),
        (leg2, CATEGORY_MEDIOCRE,     "50–79",  "Targeted skill workshops, SMART goal frameworks, and bi-monthly reviews."),
        (leg3, CATEGORY_BELOW_AVERAGE,"0–49",   "Remedial training program, designated mentor, and 90-day re-evaluation."),
        (leg4, CATEGORY_NOT_APPRAISED,"N/A",    "Pending baseline appraisal cycle submission."),
    ]:
        with col:
            st.markdown(f"""
            <div style="background:var(--bg-card); border:1px solid var(--border-subtle); border-radius:6px;
                        padding:14px; text-align:left;">
              <div style="color:var(--text-main); font-weight:600; font-size:0.88rem;">{cat}</div>
              <div style="color:var(--text-muted); font-size:0.78rem; margin-top:2px;">Score: {score_range}</div>
              <div style="color:var(--text-muted); font-size:0.78rem; margin-top:6px; line-height:1.4;">{actions}</div>
            </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    import os, sys
    _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _root not in sys.path:
        sys.path.insert(0, _root)
    from modules.ui_theme import apply_theme
    apply_theme()
    show_suggestions()
