# 🎓 CAPACITY CONNECT — Viva Q&A Guide

> Use this to prepare for your teacher's questions during the final evaluation.

---

## 🔧 General Questions

**Q1: What is Capacity Connect?**
> Capacity Connect is an Employee Performance Appraisal, Feedback, and Assistance System. It allows HR teams to record employee appraisals, collect feedback, track performance categories, and generate improvement suggestions — all through a web interface built with Python and Streamlit.

**Q2: Why did you choose Streamlit?**
> Streamlit is a Python library that lets us build interactive web apps without writing HTML, CSS, or JavaScript from scratch. It's ideal for data-driven applications and is very easy to understand for beginners.

**Q3: Why are you using CSV files instead of a database?**
> CSV files are simple to read and write using Pandas and don't require setting up a database server. For a college project with a small dataset, CSV files are perfectly adequate. In production, we'd migrate to SQLite or PostgreSQL.

**Q4: What Python libraries are used?**
> - **Streamlit** — for the web interface
> - **Pandas** — for reading, filtering, and saving CSV data
> - **Plotly** — for interactive charts
> - **os, re, sys** — built-in Python modules for file paths, regex, and system operations

---

## 📊 Performance Classification

**Q5: How do you classify employee performance?**
> We use a function called `classify_performance(score)` in `modules/performance.py`. It checks the score:
> - 80–100 → **Top Notch**
> - 50–79 → **Mediocre**
> - 0–49 → **Below Average**
> - None/NaN → **Not Appraised**

**Q6: Can the user manually set the performance category?**
> No. The category is always automatically calculated from the employee's latest appraisal score. This prevents bias and ensures consistency.

**Q7: How do you find the "latest" appraisal for an employee?**
> We sort the appraisals DataFrame by `appraisal_date` in descending order, then take the first row (`.iloc[0]`). This ensures we always use the most recent appraisal.

**Q8: What happens if an employee has no appraisal?**
> The `classify_performance()` function returns `"Not Appraised"` when the score is `None` or `NaN`. The dashboard shows these employees in a separate count card and the chatbot handles this case explicitly.

---

## 🗃 Data Management

**Q9: How do you save a new appraisal without deleting old ones?**
> We use `pandas.DataFrame.to_csv()` with `mode='a'` (append mode) and `header=False`. This adds the new row at the end of the CSV without overwriting existing records.

**Q10: How do you generate unique IDs for new records?**
> We read the existing IDs, extract the numeric part (e.g., "A042" → 42), find the maximum, and increment by 1. Then we format it back (e.g., 43 → "A043").

**Q11: What happens if the CSV file is missing?**
> The `load_employees()`, `load_appraisals()`, and `load_feedback()` functions wrap file operations in try/except blocks. If the file is not found, they return an empty DataFrame with the correct column names.

---

## 🤖 Chatbot

**Q12: How does the chatbot work without an AI API?**
> The chatbot uses **intent detection** through **regular expressions (regex)**. We have a list of patterns (INTENTS) where each pattern is matched against the user's query using `re.search()`. The first matching pattern calls the corresponding handler function, which queries the real CSV data using Pandas.

**Q13: How does the chatbot handle duplicate employee names?**
> When searching by name, the chatbot returns a table of all matching employees with their IDs. For example, if four employees are named "Rahul", all four are displayed so the user can identify the correct one by ID.

**Q14: What happens if the user asks an unsupported question?**
> The chatbot falls through all patterns and returns a friendly fallback message saying it couldn't understand the question, along with example questions the user can try.

**Q15: How is chat history maintained?**
> We use `st.session_state` — a Streamlit feature that stores variables across page interactions. The `chat_history` list is stored in session state so messages persist as long as the browser tab stays open.

---

## 📈 Dashboard & Charts

**Q16: How are the dashboard statistics calculated?**
> The `get_dashboard_stats()` function in `modules/performance.py` calls `get_enriched_employees()`, which merges the employees and appraisals DataFrames using Pandas `.merge()`. It then uses `.value_counts()` for category counts and `.groupby().agg()` for department statistics.

**Q17: Are any values hardcoded in the dashboard?**
> No. Every number and chart is calculated live from the CSV data. If you add a new appraisal, the dashboard updates immediately on the next page load.

---

## 💡 Suggestions

**Q18: How are suggestions generated?**
> The `get_suggestions_for_employee()` function in `modules/recommendations.py` does two things:
> 1. Looks up the employee's performance category and returns a pre-written list of 5 suggestions specific to that category.
> 2. Scans the latest appraisal remarks for keywords (like "communication", "deadline", "error") and adds targeted suggestions for those specific issues.

**Q19: Are suggestions AI-generated?**
> No. They are carefully written recommendation templates stored in Python dictionaries. Each suggestion includes a title, detailed action, and the reason why it's recommended. This makes the system explainable and transparent.

---

## 🏗 Architecture

**Q20: What is the architecture of the project?**
> The project follows a **3-layer architecture**:
> - **Data Layer** (`modules/data_manager.py`) — reads/writes CSV files
> - **Business Logic Layer** (`modules/performance.py`, `recommendations.py`, `chatbot.py`) — classification, statistics, chatbot
> - **Presentation Layer** (`pages/*.py`, `app.py`) — Streamlit UI components

**Q21: Why are modules separated from pages?**
> Separation of concerns makes the code easier to understand, test, and modify. The `modules/` folder contains pure Python logic with no UI code, so it can be tested independently (as demonstrated by our test suite).

**Q22: How does navigation work in the app?**
> Streamlit's `st.radio()` widget in the sidebar creates a navigation menu. Based on the selected option, `app.py` imports and calls the corresponding page function (e.g., `from pages.dashboard import show_dashboard`).

---

## 🧪 Testing

**Q23: How did you test the application?**
> We wrote a `test_capacity_connect.py` file with 60 test cases covering:
> - Performance classification at boundary scores (0, 49, 50, 79, 80, 100)
> - CSV data loading
> - Employee lookup by ID
> - Appraisal and feedback persistence (append without overwrite)
> - Chatbot intent handling for 17 different query types
> - Edge cases (missing employees, invalid scores, unsupported questions)

**Q24: All 60 tests pass?**
> Yes. Running `python -X utf8 test_capacity_connect.py` from the project root produces **60/60 PASS**.

---

## 🚀 Deployment

**Q25: How do you run the application?**
> ```
> cd CAPACITY_CONNECT
> pip install -r requirements.txt
> streamlit run app.py
> ```
> The app opens at http://localhost:8501 in the browser.
