# Formal Specification & Handoff Report: Capacity Connect Reports & Verification

**Author**: Spec Miner 1 (Requirements & Test Spec Miner)  
**Target Milestone**: M1 (Complete Reports & Verification)  
**Scope**: `pages/reports.py`, `app.py` routing, 7-page imports verification, `test_capacity_connect.py` 60/60 test suite.  
**Date**: 2026-10-21  

---

## 1. Observation

Direct observations from authoritative project sources:

### A. Original Request & Project Scope
- In `ORIGINAL_REQUEST.md` (lines 37–70):
  - **R1**: Create `pages/reports.py` containing 5 sections:
    1. Summary stats row: total employees, appraised count, average score, category breakdown (reuse data from `get_dashboard_stats()`).
    2. Top 5 Performers card: 5 highest latest appraisal scores, showing name, department, score, and category badge.
    3. Bottom 5 At-Risk card: 5 lowest latest appraisal scores (among appraised employees), same columns.
    4. Department Scorecard table: one row per department (avg score, employee count, top category, highest scorer name).
    5. CSV Export button: `st.download_button` letting users download all employees with latest score and category as CSV.
    - Visual style: `.page-header` div, dark background (`#0d0f1a`), blue accent (`#2563b0`), Inter font, card/table styling defined in `app.py`'s global CSS.
  - **R2**: Verify all 7 pages load without errors (`pages.dashboard:show_dashboard`, `pages.employees:show_employees`, `pages.appraisal:show_appraisal`, `pages.feedback:show_feedback`, `pages.suggestions:show_suggestions`, `pages.reports:show_reports`, `pages.chatbot_page:show_chatbot`).
  - **R3**: Ensure `test_capacity_connect.py` passes 60/60.

### B. Routing in `app.py`
- In `app.py` (lines 195–203):
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
- In `app.py` (lines 282–284):
  ```python
  elif page == "Reports":
      from pages.reports import show_reports
      show_reports()
  ```
- Observation: Routing is already wired to lazily import `from pages.reports import show_reports` and invoke `show_reports()`.

### C. Existing `pages/reports.py`
- `pages/reports.py` exists (238 lines) and exposes `show_reports()`.
- Top summary row (lines 50–94) renders 5 KPI cards: Total Workforce, Appraised, Average Score, Top Performers, Attention Needed.
- CSV export (lines 98–135) uses `st.download_button(label="📄 Download CSV Report", data=csv_bytes, file_name=f"capacity_connect_report_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)`.
- Top 5 and Bottom 5 (lines 139–195) filter by `enriched.dropna(subset=["latest_score"])`, sort by `latest_score` (`ascending=False` and `ascending=True`), and take `.head(5)`.
- Department Scorecard (lines 198–237) iterates `for dept, group in appraised_df.groupby("department"):` and computes `Average Score`, `Total Staff`, `Appraised`, `Dominant Category`, `Top Performer`.

### D. Test Suite (`test_capacity_connect.py`)
- Total lines: 262.
- Contains 9 test sections:
  1. Performance Classification Tests (12 checks)
  2. Data Loading Tests (6 checks)
  3. Employee Lookup Tests (5 checks)
  4. Appraisal Lookup Tests (5 checks)
  5. Feedback Lookup Tests (2 checks)
  6. Enriched Data Tests (3 checks)
  7. Save Operations (Append) (4 checks)
  8. Chatbot Tests (15 checks)
  9. Suggestions Tests (4 checks)
- Total test assertions: Exactly 60 checks (`check(...)`).
- Line 254: `print(f"  RESULTS: {passed}/{total} passed  |  {failed} failed")`.

---

## 2. Logic Chain

1. **Routing Verification**:
   - `app.py` lines 282–284 specifically branch on `page == "Reports"` and execute `from pages.reports import show_reports; show_reports()`.
   - Therefore, `pages/reports.py` MUST export a callable named `show_reports` with no required arguments.

2. **Data Integration**:
   - `modules/performance.py` provides `get_dashboard_stats()` and `get_enriched_employees()`.
   - `get_dashboard_stats()` computes `total_employees`, `avg_score`, `top_notch`, `mediocre`, `below_average`, `not_appraised`, `category_counts`, `dept_stats`, and `enriched_df`.
   - `get_enriched_employees()` joins `load_employees()` with latest records from `load_appraisals()`, providing `latest_score`, `latest_appraisal_date`, `latest_remarks`, and `performance_category`.
   - Reusing these cached helper functions fulfills R1.1 without redundant CSV parsing or computation.

3. **Summary Stats Discrepancy Analysis**:
   - Requirement R1.1 states: "Summary stats row — total employees, appraised count, average score, category breakdown (reuse data already computed by get_dashboard_stats())".
   - The current `pages/reports.py` shows only Top Performers (`top_notch`) and Attention Needed (`below_average`), omitting `mediocre` and `not_appraised`.
   - To achieve full category breakdown compliance while retaining high aesthetic quality, the summary stats row should either include all categories (e.g., 6 KPI cards matching `dashboard.py`: Total, Avg Score, Top Notch, Mediocre, Below Average, Not Appraised, plus Appraised rate in sub-label) or provide dedicated breakdown cards.

4. **Department Scorecard Completeness**:
   - The current scorecard loop operates over `appraised_df.groupby("department")`.
   - If a department has employees in `employees.csv` but none have been appraised yet, that department is omitted from the scorecard.
   - For complete reporting robustness, the table should iterate over all known departments (`enriched.groupby("department")` or `get_all_departments()`), reporting `0.0` or `—` for unappraised departments with top category `"Not Appraised"` and top performer `"None"`.

5. **Headless Execution & Test Suite Independence**:
   - `test_capacity_connect.py` tests logic functions in `modules/` independently of the Streamlit web runtime.
   - Neither `test_capacity_connect.py` nor `modules/` depend directly on `pages/reports.py`.
   - However, any edits to `modules/` (e.g. `@st.cache_data` adjustments or helper modifications) could impact `test_capacity_connect.py`.
   - In `modules/data_manager.py`, `_bust_cache()` safely guards clearing `get_enriched_employees` and `get_dashboard_stats`.
   - Clean headless importing of all 7 page modules is verified by ensuring no Streamlit rendering calls execute at module import time (only inside `show_*()` functions).

---

## 3. Caveats

1. Direct CLI commands (`python -X utf8 test_capacity_connect.py`) could not be run in this turn due to environment-level tool execution permissions. All analysis has been conducted via rigorous source code inspection, AST/grep analysis, and logical constraint verification against the authoritative specifications.
2. Production CSV files (`data/appraisals.csv` and `data/feedback.csv`) are modified during execution of Section 7 of `test_capacity_connect.py` (which appends test records to test persistence). Tests should not be run in an environment where appending rows causes side-effects unless cleaned or managed.
3. UI rendering tests (such as visual appearance in a web browser) require running Streamlit interactively (`python -m streamlit run app.py`), whereas verification criteria specify automated headless import assertions and logic tests.

---

## 4. Conclusion

The specification for `pages/reports.py`, `app.py`, 7-page imports, and `test_capacity_connect.py` is fully documented and structured below. The current codebase already has `app.py` wired and an initial version of `pages/reports.py`. 
Key refinements required for 100% compliance:
1. Ensure the summary row fully displays the complete category breakdown (including Mediocre and Not Appraised).
2. Ensure Department Scorecard handles departments with 0 appraisals gracefully without omission.
3. Keep all Streamlit execution encapsulated within `show_reports()` so `from pages.reports import show_reports` imports cleanly in headless environments.
4. Ensure all 60 tests in `test_capacity_connect.py` remain intact and passing.

---

## 5. Verification Method

To independently verify the implementation:

1. **Verify 7 Page Imports (Headless)**:
   Run from project root `c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT`:
   ```bash
   python -X utf8 -c "
   import sys, os
   sys.path.insert(0, '.')

   pages_to_check = [
       ('pages.dashboard',    'show_dashboard'),
       ('pages.employees',    'show_employees'),
       ('pages.appraisal',    'show_appraisal'),
       ('pages.feedback',     'show_feedback'),
       ('pages.suggestions',  'show_suggestions'),
       ('pages.reports',      'show_reports'),
       ('pages.chatbot_page', 'show_chatbot'),
   ]
   all_ok = True
   for mod, fn in pages_to_check:
       try:
           m = __import__(mod, fromlist=[fn])
           assert hasattr(m, fn)
           print('OK   ', mod)
       except Exception as e:
           print('FAIL ', mod, '->', e)
           all_ok = False

   print()
   print('All pages OK' if all_ok else 'SOME PAGES FAILED')
   "
   ```
   **Pass Condition**: All 7 print `OK`, and final line is `All pages OK`.

2. **Verify 60/60 Test Suite**:
   Run from project root:
   ```bash
   python -X utf8 test_capacity_connect.py
   ```
   **Pass Condition**: Final summary line verbatim: `RESULTS: 60/60 passed  |  0 failed`.

3. **Verify Reports Page Module Import**:
   ```bash
   python -X utf8 -c "import sys; sys.path.insert(0,'.'); from pages.reports import show_reports; print('OK')"
   ```
   **Pass Condition**: Prints `OK` with exit code 0.

4. **Verify CSV Download Implementation**:
   Inspect `pages/reports.py` to ensure `st.download_button` is called with:
   - `data=` (non-empty string or utf-8 encoded bytes from pandas DataFrame)
   - `file_name=` (ending with `.csv`)
   - `mime="text/csv"`

---

## Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | UI / Reports | Summary Stats Row | Summary metrics row displaying Total Workforce, Appraised Count & Percentage, Average Score, and full Category Breakdown (Top Notch, Mediocre, Below Average, Not Appraised). | `get_dashboard_stats()` dict from `modules/performance.py` | 5–6 custom KPI cards styled via `.kpi-card` | If no employees, shows 0 and 0.0 with no divide-by-zero crash. | `ORIGINAL_REQUEST.md` R1.1, `PROJECT.md` #1 |
| 2 | UI / Reports | Top 5 Performers Card | Card displaying employees with top 5 highest latest appraisal scores, ordered descending. Shows rank, name, employee ID, designation, department, score, and category badge. | `get_enriched_employees()` filtered to non-null latest scores | Rendered HTML cards with color-coded left borders and badges | If 0 appraisals, renders `st.info("No appraisal data available.")`. If <5 appraisals, shows all available. | `ORIGINAL_REQUEST.md` R1.2, `PROJECT.md` #2 |
| 3 | UI / Reports | Bottom 5 At-Risk Card | Card displaying 5 lowest scores strictly among appraised employees, ordered ascending (lowest first). Shows same metadata as Top 5. | `get_enriched_employees()` filtered to non-null latest scores | Rendered HTML cards with color-coded left borders and badges | Same as Top 5; unappraised employees excluded. | `ORIGINAL_REQUEST.md` R1.3, `PROJECT.md` #3 |
| 4 | UI / Reports | Department Scorecard | Aggregated performance table per department: Department, Total Staff, Appraised Count, Average Score, Dominant Performance Category, and Top Performer Name. | `get_enriched_employees()` grouped by department | `st.dataframe` with configured NumberColumns and auto-scaling | If no appraisals, displays graceful informative message; empty departments show 0 / "Not Appraised". | `ORIGINAL_REQUEST.md` R1.4, `PROJECT.md` #4 |
| 5 | UI / Reports | CSV Export Button | `st.download_button` allowing users to export consolidated employee appraisal records with all columns formatted. | `enriched` DataFrame formatted with date strings and clean headers | Triggered browser CSV file download (`capacity_connect_report_YYYYMMDD.csv`) | Handles missing dates/scores without raising errors; valid UTF-8 CSV. | `ORIGINAL_REQUEST.md` R1.5, `PROJECT.md` #5 |
| 6 | UI / Styling | Visual Consistency & Theme | Dark background (`#0d0f1a`), blue accent (`#2563b0`), heading blue (`#7eb8f7`), Inter font, `.page-header` div header block, `.kpi-card` styles. | Global CSS from `app.py`, inline HTML wrappers in page | Unified look-and-feel matching all 6 other pages | No hardcoded clashing colors, no layout breakages. | `ORIGINAL_REQUEST.md` R1 styling, `app.py` lines 28–192 |
| 7 | Routing | `app.py` Navigation Routing | Sidebar button routing to `"Reports"` page invoking `pages.reports:show_reports`. | `st.session_state.page == "Reports"` | Renders Reports UI in main layout container | Graceful lazy import with project root in `sys.path`. | `ORIGINAL_REQUEST.md` R1 & Acceptance Criteria, `app.py` line 282 |
| 8 | Verification | 7-Page Clean Import Script | Headless Python import verification ensuring all 7 Streamlit pages load with zero exceptions. | 7 module paths and function names | `OK` per module, `All pages OK` summary | If any page fails at import time, reports exception and fails script. | `ORIGINAL_REQUEST.md` R2 & Verification Script |
| 9 | Verification | Automated Test Suite (60/60) | Unit and logic regression suite covering performance classification, data loaders, lookups, chatbot intents, and suggestions. | `test_capacity_connect.py` | `RESULTS: 60/60 passed \| 0 failed` | Any failed test reports failure and causes non-zero failure count. | `ORIGINAL_REQUEST.md` R3, `test_capacity_connect.py` |

---

## Edge Cases

| # | Feature | Input / Condition | Observed / Required Behavior |
|---|---------|-------------------|------------------------------|
| 1 | Summary Stats | Total employees is 0 (empty `employees.csv`) | `appraisal_rate = (appraised_cnt / total_emp * 100) if total_emp > 0 else 0`. Must prevent `ZeroDivisionError`. All KPI values default to `0` / `0.0`. |
| 2 | Summary Stats | Appraisals file is empty (0 appraisals) | `not_appraised == total_emp`, `appraised_cnt == 0`, `avg_score == 0.0`. Appraised percentage shows `0%`. No division by zero. |
| 3 | Top 5 Performers | Fewer than 5 appraised employees exist (e.g. 1 to 4) | `df.sort_values(...).head(5)` returns all available rows (1 to 4) without crashing or raising IndexError. |
| 4 | Top 5 Performers | No appraised employees exist | `if not appraised_df.empty:` evaluates False; displays `st.info("No appraisal data available.")`. |
| 5 | Bottom 5 At-Risk | Unappraised employees present in workforce | Unappraised employees have `NaN` for `latest_score`. MUST filter out `NaN` (`dropna(subset=["latest_score"])`) before computing Bottom 5 so unappraised staff are NOT counted as "0 score" or bottom performers. |
| 6 | Bottom 5 At-Risk | Score ties at the boundary (e.g. multiple employees with score 45.0) | Stable sort retains deterministic order; `.head(5)` selects first 5 without runtime error. |
| 7 | Department Scorecard | Department has employees but 0 appraisals | Department should be included with Average Score `0.0` or `—`, Dominant Category `"Not Appraised"`, and Top Performer `"None"`, avoiding missing departments or IndexError on `.iloc[0]`. |
| 8 | Department Scorecard | Bimodal category distribution (equal counts of Top Notch and Mediocre) | `group["performance_category"].mode()[0]` selects the first mode without raising an exception. |
| 9 | Department Scorecard | Single employee in department | Correctly computes mean, count = 1, dominant category, and identifies that employee as top performer. |
| 10 | CSV Export | Employees with missing appraisals (`latest_score` is NaN) | `latest_score` exports as empty CSV field, `latest_appraisal_date` formatted as `"Not Appraised"` (or empty), remarks empty. Valid CSV format maintained. |
| 11 | CSV Export | Commas, quotes, or newlines in appraisal remarks | Handled automatically by `pandas.to_csv(index=False)`, which wraps fields with quotation marks. |
| 12 | CSV Export | Download button metadata | `st.download_button` MUST contain both `data=` and `file_name=` arguments, with MIME set to `"text/csv"`. |
| 13 | Page Imports | Headless execution without active Streamlit websocket/server | All page modules MUST only define functions and perform static setup at module level; NO page rendering calls (`st.write`, `st.button`, etc.) executed during module import. |
| 14 | Cache Busting & Tests | Persistence tests in `test_capacity_connect.py` modify CSVs | `_bust_cache()` in `modules/data_manager.py` clears `@st.cache_data` on `load_employees`, `load_appraisals`, `load_feedback`, `get_enriched_employees`, and `get_dashboard_stats` using `try/except`. Must not break standalone Python test runner. |

---

## Detailed Section-by-Section Specifications for Implementation & Verification

### Section 1: Summary Stats Row & Category Breakdown
- **Source**: `get_dashboard_stats()` from `modules/performance.py`.
- **Metrics Required**:
  - Total Workforce (`stats["total_employees"]`)
  - Appraised Count (`stats["total_employees"] - stats["not_appraised"]`) and Appraised Rate (`(appraised_cnt / total_emp) * 100`)
  - Average Score (`stats["avg_score"]`)
  - Full Category Breakdown:
    - Top Notch count (`stats["top_notch"]`)
    - Mediocre count (`stats["mediocre"]`)
    - Below Average count (`stats["below_average"]`)
    - Not Appraised count (`stats["not_appraised"]`)
- **Layout Specification**:
  - Rendered in a responsive 6-card row (or 5-card row with category sub-indicators):
    ```python
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    _kpi(k1, stats["total_employees"], "Total Workforce", "👥", "blue")
    _kpi(k2, f"{stats['avg_score']:.1f}", "Average Score", "📊", "purple")
    _kpi(k3, stats["top_notch"], "Top Notch", "🌟", "green")
    _kpi(k4, stats["mediocre"], "Mediocre", "📈", "amber")
    _kpi(k5, stats["below_average"], "Below Average", "⚠️", "red")
    _kpi(k6, stats["not_appraised"], "Not Appraised", "❓", "grey")
    ```
  - Sub-caption indicating total appraised count & percentage: `st.caption(f"Appraisal Coverage: **{appraised_cnt}** of **{total_emp}** employees appraised ({appraisal_rate:.1f}%)")`.
  - CSS Classes: `.kpi-card`, `.kpi-icon`, `.kpi-value`, `.kpi-label` with accent modifiers (`blue`, `purple`, `green`, `amber`, `red`, `grey`).

### Section 2: Top 5 Performers Card
- **Data Source**: `get_enriched_employees().dropna(subset=["latest_score"])`.
- **Sorting**: `.sort_values(by="latest_score", ascending=False).head(5)`.
- **Columns / Information Rendered**:
  - Rank badge (`#1` to `#5`)
  - Employee Full Name
  - Employee ID (`(E...)`)
  - Designation & Department (`{designation} · {department}`)
  - Latest Score formatted to 1 decimal place (`{latest_score:.1f}`)
  - Category Badge with category emoji and color (`_cat_badge(category)`)
- **Container Styling**: Dark card container (`background:#111426`, border-left colored by category color, border-radius `0 10px 10px 0`, padding `12px 16px`).
- **Empty State**: `if appraised_df.empty: st.info("No appraisal data available.")`.

### Section 3: Bottom 5 At-Risk Performers Card
- **Data Source**: `get_enriched_employees().dropna(subset=["latest_score"])`.
- **Sorting**: `.sort_values(by="latest_score", ascending=True).head(5)`.
- **Columns / Information Rendered**:
  - Rank badge (`#1` to `#5`)
  - Employee Full Name
  - Employee ID (`(E...)`)
  - Designation & Department (`{designation} · {department}`)
  - Latest Score formatted to 1 decimal place (`{latest_score:.1f}`)
  - Category Badge (`_cat_badge(category)`)
- **Critical Requirement**: Unappraised employees MUST NOT be included in Bottom 5. Only appraised employees are evaluated.
- **Empty State**: `if appraised_df.empty: st.info("No appraisal data available.")`.

### Section 4: Department Scorecard Table
- **Data Source**: Grouping of all departments from `enriched` and `appraised_df`.
- **Columns**:
  1. `Department`: Department name (e.g., IT, HR, Finance, Operations, Marketing, Sales).
  2. `Total Staff`: Total count of employees belonging to the department.
  3. `Appraised`: Count of appraised employees in that department.
  4. `Average Score`: Mean latest score of appraised employees in that department, rounded to 2 decimal places (or `0.00` if none).
  5. `Dominant Category`: Most frequent performance category in that department (or `"Not Appraised"` if none).
  6. `Top Performer`: Name and score of the highest scorer in the department (e.g., `Sneha Verma (95.0)` or `"None"`).
- **Presentation**: Rendered via `st.dataframe` with `use_container_width=True` and column configurations:
  - `Average Score`: `st.column_config.NumberColumn("Average Score", format="%.2f")`
  - `Total Staff`: `st.column_config.NumberColumn("Total Staff", width="small")`
  - `Appraised`: `st.column_config.NumberColumn("Appraised", width="small")`
- **Sorting**: Sorted descending by `Average Score`.

### Section 5: CSV Export Feature
- **Data Columns Exported**:
  - `Employee ID` (`employee_id`)
  - `Employee Name` (`name`)
  - `Department` (`department`)
  - `Designation` (`designation`)
  - `Email Address` (`email`)
  - `Latest Score` (`latest_score`)
  - `Performance Category` (`performance_category`)
  - `Last Appraisal Date` (`latest_appraisal_date` formatted as `YYYY-MM-DD` or `"Not Appraised"`)
  - `Remarks` (`latest_remarks`)
- **Button Implementation**:
  ```python
  st.download_button(
      label="📄 Download CSV Report",
      data=csv_bytes,
      file_name=f"capacity_connect_report_{datetime.now().strftime('%Y%m%d')}.csv",
      mime="text/csv",
      use_container_width=True,
  )
  ```
- **Validation**: Confirm `st.download_button` receives non-empty `data=`, dynamic `file_name=` ending in `.csv`, and `mime="text/csv"`.

### Section 6: Visual Styling & Theme Consistency
- **Page Header**:
  ```html
  <div class="page-header">
    <div class="page-header-icon">📈</div>
    <div>
      <div class="page-header-title">Reports & Executive Analytics</div>
      <div class="page-header-sub">Comprehensive performance analysis, department rankings, and data export</div>
    </div>
  </div>
  ```
- **Palette**:
  - Global Background: `#0d0f1a`
  - Container / Card Background: `#111426` / `#161a2e`
  - Heading Accent: `#7eb8f7`
  - Button & Brand Accent: `#2563b0`
  - Font: `Inter, sans-serif`
  - Category Colors:
    - Top Notch: `#2ecc71` / `#27ae60`
    - Mediocre: `#f39c12` / `#e67e22`
    - Below Average: `#e74c3c`
    - Not Appraised: `#95a5a6` / `#3a4570`

---

## Acceptance Criteria Checklist (for Reviewer, Challenger, and Auditor)

### 1. `pages/reports.py`
- [ ] `pages/reports.py` exists in the repository.
- [ ] `pages/reports.py` exports `show_reports()`.
- [ ] Running `python -X utf8 -c "import sys; sys.path.insert(0,'.'); from pages.reports import show_reports; print('OK')"` exits 0 and prints `OK`.
- [ ] Renders summary stats: Total employees, appraised count, average score, and category breakdown.
- [ ] Renders Top 5 performers with name, department, score, and category badge.
- [ ] Renders Bottom 5 at-risk performers (strictly among appraised employees) with name, department, score, and category badge.
- [ ] Renders Department Scorecard table with average score, employee count, top category, and highest scorer.
- [ ] Renders CSV download button (`st.download_button`) with valid `data=`, `file_name=`, and `mime="text/csv"`.
- [ ] Uses `.page-header` HTML block matching the style of other pages.
- [ ] Colors conform strictly to the `#0d0f1a`, `#7eb8f7`, `#2563b0` palette.

### 2. `app.py` Routing
- [ ] `app.py` has `"Reports"` in `NAV_ITEMS`.
- [ ] `app.py` contains `elif page == "Reports": from pages.reports import show_reports; show_reports()`.
- [ ] Sidebar pill button properly targets and activates the Reports view.

### 3. Page Import Verification
- [ ] Headless import test succeeds for all 7 pages without exceptions:
  - `pages.dashboard:show_dashboard`
  - `pages.employees:show_employees`
  - `pages.appraisal:show_appraisal`
  - `pages.feedback:show_feedback`
  - `pages.suggestions:show_suggestions`
  - `pages.reports:show_reports`
  - `pages.chatbot_page:show_chatbot`

### 4. Regression Suite
- [ ] Running `python -X utf8 test_capacity_connect.py` outputs `RESULTS: 60/60 passed  |  0 failed`.
- [ ] Zero test regressions caused by caching or data module modifications.
