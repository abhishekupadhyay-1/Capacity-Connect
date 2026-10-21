## 2026-10-21T04:06:06Z
You are the Project Orchestrator for the Capacity Connect completion project.

Your working directory for metadata (plan.md, progress.md, context.md):
`c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT\.agents\teamwork\orchestrator_1`

Project root:
`c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT`

Original Request:
Read `c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT\.agents\teamwork\ORIGINAL_REQUEST.md` for full requirements and acceptance criteria.

Summary of Objectives:
1. Build `pages/reports.py`:
   - Summary stats row (total employees, appraised count, avg score, category breakdown using `get_dashboard_stats()`)
   - Top 5 Performers card (highest latest appraisal scores, name, department, score, category badge)
   - Bottom 5 At-Risk card (lowest latest appraisal scores among appraised, name, department, score, category badge)
   - Department Scorecard table (avg score, employee count, top category, highest scorer name)
   - CSV Export button (st.download_button with data= and file_name= for all employees with latest score and category)
   - Visual consistency with existing pages (.page-header div, #0d0f1a background, #2563b0 blue accent, #7eb8f7 heading blue, Inter font, card/table styling from app.py)
2. Wire `pages/reports.py` into `app.py` (ensure `elif page == "Reports":` imports and calls `show_reports()`).
3. Verify all 7 pages load cleanly without errors via:
   `python -X utf8 -c "import sys; sys.path.insert(0, '.'); from pages.<mod> import <fn>"`
4. Ensure `python -X utf8 test_capacity_connect.py` passes 60/60.
5. Fix any issues found during verification.

Maintain `progress.md` in your working directory at regular intervals so progress and liveness can be tracked.
When done, send your completion report and victory claim back.
