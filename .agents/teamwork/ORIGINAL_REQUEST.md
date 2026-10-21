# Original User Request

## Initial Request — 2026-10-21T04:04:31Z

Complete the **Capacity Connect** Employee Performance Web App — a Python + Streamlit college project that is already ~90% built. The goal is to finish the missing Reports page, verify every page loads correctly, fix any bugs found during verification, and ensure the app looks professional and works end-to-end.

**Working directory:** `c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT`
**Integrity mode:** demo

---

## Current State

The following files are already implemented and working:

| File | Status |
|------|--------|
| `app.py` | ✅ Done — custom pill nav, dark theme CSS, Google Fonts |
| `modules/data_manager.py` | ✅ Done — `@st.cache_data`, CSV read/write |
| `modules/performance.py` | ✅ Done — `classify_performance()`, `get_enriched_employees()`, `get_dashboard_stats()` |
| `modules/chatbot.py` | ✅ Done — regex intent engine, 14+ query types |
| `modules/recommendations.py` | ✅ Done — category + remark-based suggestions |
| `pages/dashboard.py` | ✅ Done — custom KPI cards, 4 Plotly charts, filterable table |
| `pages/employees.py` | ✅ Done — paginated (10/page), avatar initials, 4-tab cards |
| `pages/appraisal.py` | ✅ Done — slider + live category preview, appends CSV |
| `pages/feedback.py` | ✅ Done — char counter, paginated history |
| `pages/suggestions.py` | ✅ Done — single + browse modes, bulk engine |
| `pages/chatbot_page.py` | ✅ Done — timestamps, autoscroll, example buttons |
| `data/employees.csv` | ✅ 45 employees |
| `data/appraisals.csv` | ✅ 50 appraisals |
| `data/feedback.csv` | ✅ 50 feedback records |
| `test_capacity_connect.py` | ✅ 60-test suite |
| **`pages/reports.py`** | ❌ **MISSING — must be created** |

---

## Requirements

### R1. Create `pages/reports.py`

Build a Reports page that contains:

1. **Summary stats row** — total employees, appraised count, average score, category breakdown (reuse data already computed by `get_dashboard_stats()`)
2. **Top 5 Performers card** — employees with the 5 highest latest appraisal scores, showing name, department, score, and category badge
3. **Bottom 5 At-Risk card** — employees with the 5 lowest latest appraisal scores (among those who have been appraised), same columns
4. **Department Scorecard table** — one row per department: avg score, employee count, top category, highest scorer name
5. **CSV Export button** — `st.download_button` that lets the user download all employees with their latest score and category as a CSV file

The page must follow the same visual style as every other page: use the `.page-header` div, dark background (`#0d0f1a`), blue accent (`#2563b0`), Inter font, same card/table styling defined in `app.py`'s global CSS.

### R2. Verify all 7 pages load without errors

After creating the Reports page, verify that every page in the sidebar navigation loads without a Python traceback or Streamlit error:

- 📊 Dashboard
- 👥 Employees
- 📝 Add Appraisal
- 💬 Add Feedback
- 💡 Suggestions
- 📈 Reports ← new
- 🤖 Chatbot

Verification method: run `python -X utf8 -c "import sys; sys.path.insert(0, '.'); from pages.dashboard import show_dashboard"` (and equivalent imports) for each page from the project root. A clean import with no exception = page passes.

### R3. Ensure `test_capacity_connect.py` still passes 60/60

The existing test suite must continue to pass in full after all changes. The tests run pure Python logic (no Streamlit runtime), so `@st.cache_data` decorators must not break them.

If any test fails due to the caching changes, patch the affected module so tests pass without removing the caching (e.g., by guarding the decorator with a `try/except` or by making tests bypass the cache).

---

## Acceptance Criteria

### Reports Page
- [ ] `pages/reports.py` exists and is importable with no errors
- [ ] The file is wired into `app.py` routing (the `elif page == "Reports":` branch)
- [ ] Running `python -X utf8 -c "import sys; sys.path.insert(0,'.');from pages.reports import show_reports; print('OK')"` prints `OK`
- [ ] The page contains at minimum: a summary row, a Top 5 table, a Bottom 5 table, a department scorecard, and a CSV download button
- [ ] The download button produces a valid CSV (verify by checking the `st.download_button` call has `data=` and `file_name=` arguments)

### All Pages Import Clean
- [ ] All 7 page modules (`dashboard`, `employees`, `appraisal`, `feedback`, `suggestions`, `reports`, `chatbot_page`) import without raising any exception when run from the project root

### Test Suite
- [ ] Running `python -X utf8 test_capacity_connect.py` from the project root prints `RESULTS: 60/60 passed | 0 failed`

### Visual Consistency
- [ ] `pages/reports.py` uses the `.page-header` HTML block (same as all other pages)
- [ ] No hardcoded colours that differ from the established palette (`#0d0f1a` background, `#7eb8f7` heading blue, `#2563b0` accent)

---

## Verification Script

Run this from `c:\Users\Abhishek\Desktop\NCU\google-antigravity\CAPACITY_CONNECT` to confirm all criteria:

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

Then run: `python -X utf8 test_capacity_connect.py`

Expected final output:
```
RESULTS: 60/60 passed  |  0 failed
```

---

> **Expecting this to run as a focused completion task** — the bulk of the app is done, so the team should concentrate on building `reports.py`, wiring it up, and verifying everything passes. If any page import fails, fix it before declaring done.
