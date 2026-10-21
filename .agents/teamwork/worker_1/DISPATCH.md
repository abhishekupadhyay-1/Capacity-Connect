## 2026-10-21T04:15:24Z

You are Worker 1 (Implementation & Verification Worker).
Your working directory: c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT\.agents\teamwork\worker_1
Original Request Path (MANDATORY TO READ FIRST): c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT\.agents\teamwork\ORIGINAL_REQUEST.md
Project Scope Document: c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT\.agents\teamwork\orchestrator_1\PROJECT.md
Project root: c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT

Explorer Reports to review:
- Explorer 1 (UI Architecture): c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT\.agents\teamwork\explorer_1\handoff.md
- Explorer 2 (Data & Logic): c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT\.agents\teamwork\explorer_2\handoff.md
- Spec Miner 1 (Spec & Acceptance Criteria): c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT\.agents\teamwork\spec_miner_1\handoff.md

Write Ownership:
You own `pages/reports.py` and `app.py`.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Objectives:
1. Review ORIGINAL_REQUEST.md, PROJECT.md, and the three handoff reports.
2. Confirm wiring in `app.py` for "Reports" (lines 282–284). Ensure `elif page == "Reports": from pages.reports import show_reports; show_reports()` is present and correct.
3. Implement `pages/reports.py` to production standard:
   - Header: `.page-header` HTML block with icon 📈, title "Reports & Executive Analytics", and subtitle.
   - Summary stats row: 6 KPI cards (Total Workforce, Appraised count & %, Average Score, Top Notch count, Mediocre count, Below Average count, plus coverage caption) using `get_dashboard_stats()`.
   - CSV Export: `st.download_button(label="📄 Download CSV Report", data=csv_bytes, file_name=f"capacity_connect_report_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)` containing all employees with ID, Name, Department, Designation, Email, Latest Score, Performance Category, Last Appraisal Date, Remarks.
   - Top 5 Performers card: Employees with 5 highest latest appraisal scores, showing name, ID, department, designation, score, and category badge.
   - Bottom 5 At-Risk card: Employees with 5 lowest latest appraisal scores (strictly among appraised employees with non-null scores), showing name, ID, department, designation, score, and category badge.
   - Department Scorecard table: Grouped over all unique departments in the organization (ensuring departments with 0 appraisals are not dropped), with columns: Department, Employee Count, Appraised, Average Score, Top Category, Highest Scorer, rendered via `st.dataframe`.
   - Styling: Use established palette (#0d0f1a background, #2563b0 primary blue, #7eb8f7 heading blue, Inter font, card & badge styling).
4. Run verification commands from project root (`c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT`):
   - 7-Page headless import verification:
     `python -X utf8 -c "import sys, os; sys.path.insert(0, '.'); pages_to_check = [('pages.dashboard', 'show_dashboard'), ('pages.employees', 'show_employees'), ('pages.appraisal', 'show_appraisal'), ('pages.feedback', 'show_feedback'), ('pages.suggestions', 'show_suggestions'), ('pages.reports', 'show_reports'), ('pages.chatbot_page', 'show_chatbot')]; all_ok = True; [print('OK   ', mod) if hasattr(__import__(mod, fromlist=[fn]), fn) else (print('FAIL ', mod), exec('all_ok = False')) for mod, fn in pages_to_check]; print('All pages OK' if all_ok else 'SOME PAGES FAILED'); sys.exit(0 if all_ok else 1)"`
   - Test suite verification:
     `python -X utf8 test_capacity_connect.py`
     Must pass 60/60.
5. If any import or test fails, fix it immediately without breaking caching.
6. Maintain progress.md in your working directory.
7. Write your comprehensive completion report to `c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT\.agents\teamwork\worker_1\handoff.md`. Include all command outputs and verification logs.
8. Send a message to the caller when done with the path to your handoff.md and summary of test results.
