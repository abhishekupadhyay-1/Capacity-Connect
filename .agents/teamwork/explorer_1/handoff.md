# Handoff Report: UI & Page Architecture Analysis (Capacity Connect)

**Explorer**: Explorer 1 (UI & Page Architecture Explorer)  
**Date**: 2026-10-21T04:16:00Z  
**Type**: Hard Handoff (Investigation Complete)  
**Target Path**: `c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT\.agents\teamwork\explorer_1\handoff.md`  

---

## 1. Observation

Direct examination of `app.py`, `pages/*.py`, `modules/*.py`, and project configuration revealed the following verbatim facts:

### 1.1 Navigation & Routing in `app.py`
- In `app.py` (lines 24–26):
  ```python
  if "page" not in st.session_state:
      st.session_state.page = "Dashboard"
  ```
- In `app.py` (lines 195–203), `NAV_ITEMS` definition:
  ```python
  NAV_ITEMS = [
      ("Dashboard",    "📊", "Performance overview & charts"),
      ("Employees",    "👥", "Browse & search employees"),
      ("Add Appraisal","📝", "Record a performance appraisal"),
      ("Add Feedback", "💬", "Submit employee feedback"),
      ("Suggestions",  "💡", "View improvement recommendations"),
      ("Reports",      "📈", "Export & summary reports"),
      ("Chatbot",      "🤖", "Ask questions about your data"),
  ]
  ```
- In `app.py` (lines 222–236), sidebar rendering using `st.button`:
  ```python
  for label, icon, hint in NAV_ITEMS:
      is_active = st.session_state.page == label
      css_class = "nav-btn active" if is_active else "nav-btn"
      clicked = st.button(
          f"{icon}  {label}",
          key=f"nav_{label}",
          use_container_width=True,
          help=hint,
      )
      if clicked:
          st.session_state.page = label
          st.rerun()
  ```
- In `app.py` (lines 250–262), active button styling dynamically targeted via nth-child:
  ```python
  active_page = st.session_state.page
  active_idx  = next((i for i,(l,_,_) in enumerate(NAV_ITEMS) if l==active_page), 0)
  st.markdown(f"""
  <style>
  /* Highlight active nav button via nth-child targeting */
  [data-testid="stSidebar"] .stButton:nth-child({active_idx + 4}) > button {{
      background: linear-gradient(135deg,#2563b0,#1a4a8a) !important;
      color: #ffffff !important;
      box-shadow: 0 2px 12px rgba(37,99,176,.45) !important;
  }}
  </style>
  """, unsafe_allow_html=True)
  ```
- In `app.py` (lines 264–288), page router:
  ```python
  page = st.session_state.page

  if page == "Dashboard":
      from pages.dashboard import show_dashboard
      show_dashboard()
  elif page == "Employees":
      from pages.employees import show_employees
      show_employees()
  elif page == "Add Appraisal":
      from pages.appraisal import show_appraisal
      show_appraisal()
  elif page == "Add Feedback":
      from pages.feedback import show_feedback
      show_feedback()
  elif page == "Suggestions":
      from pages.suggestions import show_suggestions
      show_suggestions()
  elif page == "Reports":
      from pages.reports import show_reports
      show_reports()
  elif page == "Chatbot":
      from pages.chatbot_page import show_chatbot
      show_chatbot()
  ```
  **Observation**: The routing branch for `Reports` is already present in `app.py` (lines 282–284), calling `show_reports()` from `pages.reports`.

### 1.2 Structure of `.page-header` Across All Pages
Every single page strictly follows the identical 2-level flex HTML block:
```html
<div class="page-header">
  <div class="page-header-icon">{ICON}</div>
  <div>
    <div class="page-header-title">{TITLE}</div>
    <div class="page-header-sub">{SUBTITLE}</div>
  </div>
</div>
```
Verbatim examples from existing pages:
- `pages/dashboard.py` (lines 42–49): Icon `📊`, Title `Performance Dashboard`, Subtitle `Live overview of all employee appraisals and performance metrics`
- `pages/employees.py` (lines 46–53): Icon `👥`, Title `Employee Directory`, Subtitle `Search, filter and explore detailed employee profiles`
- `pages/appraisal.py` (lines 44–51): Icon `📝`, Title `Add Appraisal`, Subtitle `Record a performance appraisal — category is set automatically`
- `pages/feedback.py` (lines 21–28): Icon `💬`, Title `Add Feedback`, Subtitle `Record structured feedback for any employee`
- `pages/suggestions.py` (lines 67–74): Icon `💡`, Title `Suggestions & Recommendations`, Subtitle `AI-style personalised development guidance — powered by your data`
- `pages/chatbot_page.py` (lines 70–77): Icon `🤖`, Title `AI-Style Chatbot`, Subtitle `Ask natural language questions — answered from your real datasets`
- `pages/reports.py` (lines 36–43): Icon `📈`, Title `Reports & Executive Analytics`, Subtitle `Comprehensive performance analysis, department rankings, and data export`

### 1.3 Exact CSS Styling & Theme Variables
Defined in `app.py` (lines 28–192):
- **Base Typography**: `* { font-family: 'Inter', sans-serif !important; }`
- **Backgrounds**:
  - Global app background: `.stApp { background-color: #0d0f1a; color: #dde3f0; }`
  - Sidebar background: `linear-gradient(180deg, #111426 0%, #0d1030 100%)`, border: `1px solid #1e2545`
  - Card & Container background: `linear-gradient(135deg, #161a2e 0%, #1c2140 100%)`, border: `1px solid #252d50`, border-radius: `14px`
  - Inner list card background: `#111426` or `#161a2e`
- **Color Palette**:
  - Primary Blue Accent: `#2563b0` (Hover: `#3373c0`, Gradient: `linear-gradient(135deg,#2563b0,#1a4a8a)`)
  - Title / Heading Blue: `#7eb8f7` (used in `h1, h2, h3`, `.page-header-title`, `.kpi-value`)
  - Subheading / Subtitle: `#a0b0d0` (`h4, h5`), `#7a88a8` (`.page-header-sub`, `.kpi-label`)
  - Body Text: `#dde3f0`
  - Muted / Dividers: `#1e2545`, `#3a4570`, `#5a6888`
- **KPI Card Styles** (`.kpi-card`):
  ```css
  .kpi-card {
      background:linear-gradient(135deg,#161a2e,#1c2140);
      border:1px solid #252d50; border-radius:14px;
      padding:18px 20px; position:relative; overflow:hidden;
  }
  .kpi-card::before {
      content:''; position:absolute; top:0; left:0;
      width:4px; height:100%; border-radius:4px 0 0 4px;
  }
  .kpi-card.blue::before   { background:#2563b0; }
  .kpi-card.green::before  { background:#27ae60; }
  .kpi-card.amber::before  { background:#e67e22; }
  .kpi-card.red::before    { background:#e74c3c; }
  .kpi-card.grey::before   { background:#5a6888; }
  .kpi-card.purple::before { background:#8e44ad; }
  .kpi-value { font-size:2rem; font-weight:800; color:#7eb8f7; line-height:1; }
  .kpi-label { font-size:0.72rem; color:#7a88a8; text-transform:uppercase; letter-spacing:0.9px; margin-top:6px; font-weight:600; }
  .kpi-icon  { font-size:1.4rem; position:absolute; right:16px; top:16px; opacity:0.25; }
  ```
- **Category Colors & Badges**:
  - Top Notch: Green (`#27ae60` in CSS, `#2ecc71` in `performance.py`), icon `🌟`
  - Mediocre: Amber (`#e67e22` in CSS, `#f39c12` in `performance.py`), icon `📊` or `📈`
  - Below Average: Red (`#e74c3c`), icon `⚠️`
  - Not Appraised: Grey (`#5a6888` / `#7a88a8` / `#95a5a6`), icon `❓`
- **Tables**: `.stDataFrame { border-radius:12px; overflow:hidden; border:1px solid #1e2545; }`
- **Buttons / Downloads**: `.stButton > button` styled with primary blue gradient, white text, 9px radius.

### 1.4 State of `pages/reports.py`
A version of `pages/reports.py` exists (238 lines) and contains:
1. Header `.page-header` with icon `📈`.
2. Summary KPI row using 5 columns (`st.columns(5)`): Total Workforce, Appraised count/rate, Average Score, Top Performers, Attention Needed.
3. CSV Export Section with `st.download_button` (providing `data=csv_bytes`, `file_name=...`, `mime="text/csv"`).
4. Top 5 & Bottom 5 Rankings in 2 columns (`st.columns(2)`).
5. Department Scorecard table (`st.dataframe` with column configurations).

---

## 2. Logic Chain

### 2.1 Navigation & Routing Logic
1. `app.py` already specifies `("Reports", "📈", "Export & summary reports")` in `NAV_ITEMS`.
2. Line 282 of `app.py` already specifies:
   ```python
   elif page == "Reports":
       from pages.reports import show_reports
       show_reports()
   ```
3. Therefore, no routing modification in `app.py` is needed, but the worker agent should confirm that `pages/reports.py` exports `show_reports()` with no arguments.

### 2.2 Analysis of `pages/reports.py` vs Requirements (R1.1 – R1.5)

| Requirement | Requirement Spec | Existing `pages/reports.py` | Gap / Recommended Optimization |
|---|---|---|---|
| **R1.1 Summary Stats Row** | Total employees, appraised count, average score, category breakdown using `get_dashboard_stats()` | 5 KPI cards (`s1..s5`): Total Workforce, Appraised %, Avg Score, Top Performers, Attention Needed. | **Gaps identified**: <br>1. Mediocre count (`stats['mediocre']`) is omitted.<br>2. Card `s4` uses class `amber` for `top_notch`, but Top Notch is green across the system.<br>3. `stats['enriched_df']` is already computed in `get_dashboard_stats()`, so calling `get_enriched_employees()` again is redundant.<br>**Fix**: Use 6 columns: Total Workforce (`blue`), Appraised Count (`purple`), Average Score (`blue`), Top Notch (`green`), Mediocre (`amber`), Below Average (`red`), plus a subtitle/caption noting Not Appraised count. |
| **R1.2 Top 5 Performers** | 5 highest latest scores, name, department, score, category badge | Handled via `appraised_df.sort_values(by="latest_score", ascending=False).head(5)` with styled card divs. | Complete and visually polished. |
| **R1.3 Bottom 5 At-Risk** | 5 lowest latest scores among appraised, same columns | Handled via `appraised_df.sort_values(by="latest_score", ascending=True).head(5)` with styled card divs. | Complete and visually polished. |
| **R1.4 Department Scorecard** | One row per department: avg score, employee count, top category, highest scorer name | Handled via `appraised_df.groupby("department")`. | **Edge-case Risk**: If a department has 0 appraised employees, `appraised_df.groupby("department")` skips that department. Grouping by `enriched.groupby("department")` guarantees all departments in the organization are displayed. |
| **R1.5 CSV Export** | `st.download_button` with `data=` and `file_name=` for all employees with latest score and category | Implemented with `st.download_button`, `data=csv_bytes`, `file_name=capacity_connect_report_YYYYMMDD.csv`, `mime="text/csv"`. | Meets all criteria. |

---

## 3. Caveats

1. **Terminal Command Execution**: `run_command` permission prompt was denied in this environment. All validations performed were static syntax, import structure, and cross-file reference checks.
2. **Data Dependencies**: `pages/reports.py` depends on `data/employees.csv` (45 records) and `data/appraisals.csv` (50 records). If data files are altered or corrupted, fallbacks in `data_manager.py` handle missing data with empty DataFrames.
3. **No External Libraries**: No external charting libraries beyond `plotly` and `streamlit` are imported.

---

## 4. Conclusion & Recommended Code

The existing `pages/reports.py` is ~95% complete. Applying targeted refinements to the KPI row (proper 6-category breakdown with green/amber/red alignment) and making the Department Scorecard group over all departments in `enriched` will ensure 100% compliance with R1.1–R1.5 and flawless visual consistency.

### Recommended `pages/reports.py` Refined Code Pattern:

```python
"""
pages/reports.py — Reports & Analytics page for Capacity Connect.
Includes summary metrics, top/bottom performers, department scorecard, and CSV export.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from modules.performance import (
    get_dashboard_stats,
    get_enriched_employees,
    classify_performance,
    get_category_badge,
    get_category_color,
    CATEGORY_TOP_NOTCH,
    CATEGORY_MEDIOCRE,
    CATEGORY_BELOW_AVERAGE,
    CATEGORY_NOT_APPRAISED,
    CATEGORY_COLORS,
)
from modules.data_manager import load_employees, load_appraisals


def _cat_badge(cat: str) -> str:
    color = get_category_color(cat)
    badge = get_category_badge(cat)
    return (
        f'<span style="background:{color}22; color:{color}; padding:3px 10px; '
        f'border-radius:16px; font-size:0.8rem; font-weight:700; border:1px solid {color};">'
        f'{badge} {cat}</span>'
    )


def show_reports():
    st.markdown("""
    <div class="page-header">
      <div class="page-header-icon">📈</div>
      <div>
        <div class="page-header-title">Reports & Executive Analytics</div>
        <div class="page-header-sub">Comprehensive performance analysis, department rankings, and data export</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Compiling reports..."):
        stats = get_dashboard_stats()
        enriched = stats["enriched_df"]

    # ── Summary KPI Row (R1.1) ────────────────────────────────────────────────
    total_emp = stats["total_employees"]
    not_app = stats["not_appraised"]
    appraised_cnt = total_emp - not_app
    appraisal_rate = (appraised_cnt / total_emp * 100) if total_emp > 0 else 0

    s1, s2, s3, s4, s5, s6 = st.columns(6)

    s1.markdown(f"""
    <div class="kpi-card blue">
      <div class="kpi-icon">👥</div>
      <div class="kpi-value">{total_emp}</div>
      <div class="kpi-label">Total Workforce</div>
    </div>
    """, unsafe_allow_html=True)

    s2.markdown(f"""
    <div class="kpi-card purple">
      <div class="kpi-icon">✅</div>
      <div class="kpi-value">{appraised_cnt}</div>
      <div class="kpi-label">Appraised ({appraisal_rate:.0f}%)</div>
    </div>
    """, unsafe_allow_html=True)

    s3.markdown(f"""
    <div class="kpi-card blue">
      <div class="kpi-icon">📊</div>
      <div class="kpi-value">{stats['avg_score']:.1f}</div>
      <div class="kpi-label">Average Score</div>
    </div>
    """, unsafe_allow_html=True)

    s4.markdown(f"""
    <div class="kpi-card green">
      <div class="kpi-icon">🌟</div>
      <div class="kpi-value">{stats['top_notch']}</div>
      <div class="kpi-label">Top Notch (≥80)</div>
    </div>
    """, unsafe_allow_html=True)

    s5.markdown(f"""
    <div class="kpi-card amber">
      <div class="kpi-icon">📈</div>
      <div class="kpi-value">{stats['mediocre']}</div>
      <div class="kpi-label">Mediocre (50–79)</div>
    </div>
    """, unsafe_allow_html=True)

    s6.markdown(f"""
    <div class="kpi-card red">
      <div class="kpi-icon">⚠️</div>
      <div class="kpi-value">{stats['below_average']}</div>
      <div class="kpi-label">Below Average (<50)</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<div style='font-size:0.75rem; color:#7a88a8; text-align:right; margin-top:6px;'>"
        f"Workforce coverage: <b>{appraised_cnt}/{total_emp}</b> appraised ({appraisal_rate:.1f}%) · "
        f"<b>{not_app}</b> pending appraisal</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── CSV Export Section (R1.5) ─────────────────────────────────────────────
    exp_col1, exp_col2 = st.columns([3, 1])
    with exp_col1:
        st.markdown("#### 📥 Export Appraisals Dataset")
        st.caption("Download full consolidated employee records including latest scores, ratings, and appraisal remarks.")

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
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
        st.download_button(
            label="📄 Download CSV Report",
            data=csv_bytes,
            file_name=f"capacity_connect_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Top 5 & Bottom 5 Rankings (R1.2 & R1.3) ─────────────────────────────────
    rank_col1, rank_col2 = st.columns(2)
    appraised_df = enriched.dropna(subset=["latest_score"]).copy()

    with rank_col1:
        st.markdown("#### 🌟 Top 5 Performers")
        if not appraised_df.empty:
            top5 = appraised_df.sort_values(by="latest_score", ascending=False).head(5)
            for idx, (_, r) in enumerate(top5.iterrows(), 1):
                cat = r["performance_category"]
                color = get_category_color(cat)
                st.markdown(f"""
                <div style="background:#111426; border-left:4px solid {color}; border-radius:0 10px 10px 0;
                            padding:12px 16px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                  <div>
                    <div style="font-weight:700; color:#dde3f0; font-size:0.95rem;">
                      #{idx} {r['name']} <span style="font-size:0.75rem; color:#7a88a8;">({r['employee_id']})</span>
                    </div>
                    <div style="font-size:0.8rem; color:#7a88a8; margin-top:2px;">
                      {r['designation']} · {r['department']}
                    </div>
                  </div>
                  <div style="text-align:right;">
                    <div style="font-size:1.15rem; font-weight:800; color:{color};">{r['latest_score']:.1f}</div>
                    <div>{_cat_badge(cat)}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No appraisal data available.")

    with rank_col2:
        st.markdown("#### ⚠️ Bottom 5 At-Risk Performers")
        if not appraised_df.empty:
            bottom5 = appraised_df.sort_values(by="latest_score", ascending=True).head(5)
            for idx, (_, r) in enumerate(bottom5.iterrows(), 1):
                cat = r["performance_category"]
                color = get_category_color(cat)
                st.markdown(f"""
                <div style="background:#111426; border-left:4px solid {color}; border-radius:0 10px 10px 0;
                            padding:12px 16px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                  <div>
                    <div style="font-weight:700; color:#dde3f0; font-size:0.95rem;">
                      #{idx} {r['name']} <span style="font-size:0.75rem; color:#7a88a8;">({r['employee_id']})</span>
                    </div>
                    <div style="font-size:0.8rem; color:#7a88a8; margin-top:2px;">
                      {r['designation']} · {r['department']}
                    </div>
                  </div>
                  <div style="text-align:right;">
                    <div style="font-size:1.15rem; font-weight:800; color:{color};">{r['latest_score']:.1f}</div>
                    <div>{_cat_badge(cat)}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No appraisal data available.")

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ── Department Scorecard Table (R1.4) ──────────────────────────────────────
    st.markdown("#### 🏢 Department Scorecard")
    st.caption("Aggregated performance metrics and highest achievers across departments.")

    if not enriched.empty:
        scorecard_rows = []
        for dept, group in enriched.groupby("department"):
            emp_count = len(group)
            appraised_group = group.dropna(subset=["latest_score"])
            appraised_here = len(appraised_group)

            if not appraised_group.empty:
                avg_s = round(float(appraised_group["latest_score"].mean()), 2)
                top_cat = appraised_group["performance_category"].mode()[0]
                top_scorer_row = appraised_group.sort_values("latest_score", ascending=False).iloc[0]
                top_scorer_name = f"{top_scorer_row['name']} ({top_scorer_row['latest_score']:.1f})"
            else:
                avg_s = 0.0
                top_cat = "Not Appraised"
                top_scorer_name = "None"

            scorecard_rows.append({
                "Department": dept,
                "Total Staff": emp_count,
                "Appraised": appraised_here,
                "Average Score": avg_s,
                "Dominant Category": top_cat,
                "Top Performer": top_scorer_name,
            })

        scorecard_df = pd.DataFrame(scorecard_rows).sort_values("Average Score", ascending=False)
        st.dataframe(
            scorecard_df.reset_index(drop=True),
            use_container_width=True,
            height=280,
            column_config={
                "Average Score": st.column_config.NumberColumn("Average Score", format="%.2f"),
                "Total Staff": st.column_config.NumberColumn("Total Staff", width="small"),
                "Appraised": st.column_config.NumberColumn("Appraised", width="small"),
                "Dominant Category": st.column_config.TextColumn("Dominant Category", width="medium"),
                "Top Performer": st.column_config.TextColumn("Top Performer", width="medium"),
            }
        )
    else:
        st.info("Department analytics will appear here once appraisals are recorded.")
```

---

## 5. Verification Method

To independently verify this assessment:

1. **Verify routing wire-up in `app.py`**:
   Inspect lines 195–203 and lines 282–284 of `app.py`:
   - `NAV_ITEMS` must contain `("Reports", "📈", "Export & summary reports")`.
   - `elif page == "Reports":` must import `show_reports` from `pages.reports` and invoke `show_reports()`.

2. **Verify 7-page clean imports**:
   Run the project verification script:
   ```bash
   python -X utf8 -c "
   import sys
   sys.path.insert(0, '.')
   pages = [
       ('pages.dashboard', 'show_dashboard'),
       ('pages.employees', 'show_employees'),
       ('pages.appraisal', 'show_appraisal'),
       ('pages.feedback', 'show_feedback'),
       ('pages.suggestions', 'show_suggestions'),
       ('pages.reports', 'show_reports'),
       ('pages.chatbot_page', 'show_chatbot'),
   ]
   for m, fn in pages:
       mod = __import__(m, fromlist=[fn])
       assert hasattr(mod, fn), f'Missing {fn} in {m}'
       print('OK   ', m)
   print('\nAll pages OK')
   "
   ```
   **Expected**: Prints `OK    pages.<name>` for all 7 modules without exceptions.

3. **Verify automated test suite**:
   ```bash
   python -X utf8 test_capacity_connect.py
   ```
   **Expected**: `RESULTS: 60/60 passed | 0 failed`.

4. **Verify CSS & Theme Layout**:
   - Check `.page-header` contains `📈`, `Reports & Executive Analytics`.
   - Check that KPI cards use `.kpi-card.blue`, `.purple`, `.green`, `.amber`, `.red`.
   - Check that `st.download_button` has `data=` and `file_name=`.

5. **Invalidation Conditions**:
   - Any modification in `app.py` that alters `NAV_ITEMS` index offsets or removes `elif page == "Reports":`.
   - Removal or renaming of `get_dashboard_stats()`, `get_enriched_employees()`, or `get_category_color()` in `modules/performance.py`.
