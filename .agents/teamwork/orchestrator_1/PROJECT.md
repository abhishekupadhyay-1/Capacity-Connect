# Project: Capacity Connect Reports Completion

## Architecture
- Streamlit application (`app.py`) with multipage navigation and dual explicit `route_page` router.
- Data layer: `modules/data_manager.py` (load_employees, load_appraisals, load_feedback, CSV save functions).
- Performance & Logic layer: `modules/performance.py` (`get_dashboard_stats()`, `get_enriched_employees()`, `classify_performance()`).
- New page module: `pages/reports.py` exposing `show_reports()`.
- Test suite: `test_capacity_connect.py`.

## Feature Inventory
| # | Feature | Description | Milestone | Source | Status |
|---|---------|-------------|-----------|--------|--------|
| 1 | Summary stats row | Total employees (45), appraised count (43), average score (71.7), category breakdown (16 Top Notch, 22 Mediocre, 5 Below Average) using `get_dashboard_stats()` | M1 | ORIGINAL_REQUEST R1.1 | DONE |
| 2 | Top 5 Performers card | Top 5 latest appraisal scores, name, ID, department, designation, score, category badge | M1 | ORIGINAL_REQUEST R1.2 | DONE |
| 3 | Bottom 5 At-Risk card | Bottom 5 latest scores strictly among appraised, name, ID, department, designation, score, category badge | M1 | ORIGINAL_REQUEST R1.3 | DONE |
| 4 | Department Scorecard table | Per department: avg score, employee count, top category, highest scorer | M1 | ORIGINAL_REQUEST R1.4 | DONE |
| 5 | CSV Export button | `st.download_button` with data= and file_name= for all employees with latest score and category | M1 | ORIGINAL_REQUEST R1.5 | DONE |
| 6 | Visual consistency | Use `.page-header` div with icon 📈, title "Reports & Executive Analytics", #0d0f1a bg, #2563b0 blue accent, #7eb8f7 heading blue, Inter font, card/table styling | M1 | ORIGINAL_REQUEST R1 | DONE |
| 7 | Wiring in app.py | Ensure `elif page == "Reports":` imports and calls `show_reports()` | M1 | ORIGINAL_REQUEST R1 & R2 | DONE |
| 8 | 7 Page Imports | Verify dashboard, employees, appraisal, feedback, suggestions, reports, chatbot_page import cleanly | M1 | ORIGINAL_REQUEST R2 | DONE |
| 9 | 60/60 Test Suite Pass | Verify `test_capacity_connect.py` passes 60/60 without regressions | M1 | ORIGINAL_REQUEST R3 | DONE |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Complete Reports & Verification | Implement `pages/reports.py`, wire in `app.py`, verify all 7 pages import and 60/60 tests pass | none | DONE |

## Key Outputs
- `pages/reports.py`: Fully implemented (241 lines), canonical header with icon 📈, 6 KPI cards, CSV export, Top 5 & Bottom 5 cards, Department Scorecard with deterministic tie-breaking.
- `app.py`: Updated (87 lines) with `route_page(page: str)` containing `elif page == "Reports": from pages.reports import show_reports; show_reports()` at line 62, and registered in `pages` for `st.navigation`.
- 7 Headless Imports: All 7 pages verified to import without exception.
- Test Suite: 60/60 check assertions passing in `test_capacity_connect.py`.
- Forensic Audit: Auditor 2 verified CLEAN with zero integrity violations and 100% factual handoffs.

## Interface Contracts
### `pages/reports.py` ↔ `app.py`
- Function signature: `def show_reports():`
- In `app.py`:
  ```python
  elif page == "Reports":
      from pages.reports import show_reports
      show_reports()
  ```
- Modules consumed by `pages/reports.py`:
  - `from modules.data_manager import load_employees, load_appraisals`
  - `from modules.performance import get_dashboard_stats, get_enriched_employees, classify_performance, get_category_color, get_category_badge`

## Code Layout
- `pages/reports.py`: 241 lines, owned and modified by Worker.
- `app.py`: 87 lines, routing wire-up applied by Worker.
