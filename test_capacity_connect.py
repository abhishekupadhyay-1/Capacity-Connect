# -*- coding: utf-8 -*-
"""
test_capacity_connect.py
Automated logic tests for Capacity Connect.
Run from the project root: python test_capacity_connect.py
"""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import sys
import os

# Ensure project root is in path
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from modules.performance import classify_performance, validate_score
from modules.data_manager import (
    load_employees,
    load_appraisals,
    load_feedback,
    get_employee_by_id,
    get_latest_appraisal,
    get_employee_appraisals,
    get_employee_feedback,
    employee_id_exists,
    save_appraisal,
    save_feedback,
)
from modules.chatbot import process_query
from modules.recommendations import get_suggestions_for_employee
from modules.performance import get_enriched_employees

PASS = "✅ PASS"
FAIL = "❌ FAIL"
results = []


def check(test_name, condition, detail=""):
    status = PASS if condition else FAIL
    results.append((test_name, status, detail))
    print(f"  {status} | {test_name}" + (f" — {detail}" if detail else ""))


print("\n" + "="*60)
print("  CAPACITY CONNECT — Automated Test Suite")
print("="*60)

# ══════════════════════════════════════════════════════════════
# 1. Classification Logic Tests
# ══════════════════════════════════════════════════════════════
print("\n[1] Performance Classification Tests")
check("Score 0   → Below Average",   classify_performance(0)   == "Below Average")
check("Score 49  → Below Average",   classify_performance(49)  == "Below Average")
check("Score 50  → Mediocre",        classify_performance(50)  == "Mediocre")
check("Score 79  → Mediocre",        classify_performance(79)  == "Mediocre")
check("Score 80  → Top Notch",       classify_performance(80)  == "Top Notch")
check("Score 100 → Top Notch",       classify_performance(100) == "Top Notch")
check("Score None → Not Appraised",  classify_performance(None) == "Not Appraised")
check("Score NaN → Not Appraised",   classify_performance(float("nan")) == "Not Appraised")

# Validate score
v1, _ = validate_score(75)
v2, _ = validate_score(-1)
v3, _ = validate_score(101)
v4, _ = validate_score("abc")
check("Validate 75 → valid",    v1 is True)
check("Validate -1 → invalid",  v2 is False)
check("Validate 101 → invalid", v3 is False)
check("Validate 'abc' → invalid", v4 is False)

# Invalid score raises ValueError
try:
    classify_performance(-5)
    check("Score -5 raises ValueError", False, "No exception raised!")
except ValueError:
    check("Score -5 raises ValueError", True)

# ══════════════════════════════════════════════════════════════
# 2. Data Loading Tests
# ══════════════════════════════════════════════════════════════
print("\n[2] Data Loading Tests")
employees = load_employees()
appraisals = load_appraisals()
feedback = load_feedback()

check("Employees loaded (≥40)",  len(employees) >= 40,  f"Got {len(employees)}")
check("Appraisals loaded (≥40)", len(appraisals) >= 40, f"Got {len(appraisals)}")
check("Feedback loaded (≥40)",   len(feedback) >= 40,   f"Got {len(feedback)}")

check("employee_id column exists", "employee_id" in employees.columns)
check("performance_score column exists", "performance_score" in appraisals.columns)
check("feedback_type column exists", "feedback_type" in feedback.columns)

# ══════════════════════════════════════════════════════════════
# 3. Employee Lookup Tests
# ══════════════════════════════════════════════════════════════
print("\n[3] Employee Lookup Tests")
emp = get_employee_by_id("E101")
check("E101 found", emp is not None)
check("E101 name correct", emp is not None and emp["name"] == "Rahul Sharma")

missing = get_employee_by_id("E999")
check("E999 returns None", missing is None)

check("E101 exists (ID check)", employee_id_exists("E101") is True)
check("E999 does not exist", employee_id_exists("E999") is False)

# ══════════════════════════════════════════════════════════════
# 4. Appraisal Lookup Tests
# ══════════════════════════════════════════════════════════════
print("\n[4] Appraisal Lookup Tests")
latest_e101 = get_latest_appraisal("E101")
check("E101 has latest appraisal", latest_e101 is not None)
check("E101 latest score ≥ 80 (should be Top Notch)", latest_e101 is not None and latest_e101["performance_score"] >= 80)

# Employee 145 (Rahul Singh) has no appraisal in sample data
no_appraisal = get_latest_appraisal("E145")
check("E145 has no appraisal → None", no_appraisal is None)

# Multiple appraisals: E101 has A001 and A044
all_e101 = get_employee_appraisals("E101")
check("E101 has multiple appraisals", len(all_e101) >= 2, f"Got {len(all_e101)}")
check("E101 appraisals sorted newest first", all_e101.iloc[0]["appraisal_date"] >= all_e101.iloc[-1]["appraisal_date"])

# ══════════════════════════════════════════════════════════════
# 5. Feedback Lookup Tests
# ══════════════════════════════════════════════════════════════
print("\n[5] Feedback Lookup Tests")
fb_e102 = get_employee_feedback("E102")
check("E102 has feedback", len(fb_e102) >= 1, f"Got {len(fb_e102)}")

fb_none = get_employee_feedback("E999")
check("E999 feedback is empty", fb_none.empty)

# ══════════════════════════════════════════════════════════════
# 6. Enriched Employees & Dashboard Stats
# ══════════════════════════════════════════════════════════════
print("\n[6] Enriched Data Tests")
enriched = get_enriched_employees()
check("Enriched has performance_category", "performance_category" in enriched.columns)
check("Not Appraised category present for E145", enriched[enriched["employee_id"] == "E145"]["performance_category"].iloc[0] == "Not Appraised")

# Duplicate name test (Rahul appears in 3 employees: E101, E105, E126, E145)
rahul_employees = employees[employees["name"].str.contains("Rahul", case=False)]
check("Duplicate name 'Rahul' found", len(rahul_employees) >= 2, f"Found {len(rahul_employees)}")

# ══════════════════════════════════════════════════════════════
# 7. Save Appraisal & Feedback (Persistence Test)
# ══════════════════════════════════════════════════════════════
print("\n[7] Save Operations (Append)")
# Count current records
appraisals_before = len(load_appraisals())
feedback_before = len(load_feedback())

success_a, msg_a = save_appraisal("E101", "2024-10-21", 88.0, "Test appraisal from automated test suite.")
check("Save appraisal succeeds", success_a, msg_a)

appraisals_after = len(load_appraisals())
check("Appraisal count increased by 1", appraisals_after == appraisals_before + 1, f"{appraisals_before} → {appraisals_after}")

success_f, msg_f = save_feedback("E102", "Positive", "Test feedback from automated test suite.", "2024-10-21")
check("Save feedback succeeds", success_f, msg_f)

feedback_after = len(load_feedback())
check("Feedback count increased by 1", feedback_after == feedback_before + 1, f"{feedback_before} → {feedback_after}")

# ══════════════════════════════════════════════════════════════
# 8. Chatbot Tests
# ══════════════════════════════════════════════════════════════
print("\n[8] Chatbot Tests")

# Greeting
resp = process_query("Hello")
check("Chatbot greeting works", resp["type"] == "text" and "Welcome" in resp.get("content", "") or "Hello" in resp.get("content", ""))

# Total employees
resp = process_query("How many employees are there?")
check("Total employees query works", resp["type"] == "text" and "employees" in resp.get("content", "").lower())

# Name search (Rahul — duplicates)
resp = process_query("How many employees are named Rahul?")
check("Name search 'Rahul' returns table", resp["type"] == "table")
check("Rahul search finds ≥2 results", resp["type"] == "table" and len(resp.get("data", [])) >= 2)

# Employee details by ID
resp = process_query("Show details for employee E104")
check("E104 details query works", resp["type"] == "text" and "E104" in resp.get("content", ""))
check("E104 name in response", "Sneha Verma" in resp.get("content", ""))

# Department search
resp = process_query("Find employees in IT department")
check("IT department search works", resp["type"] == "table")
check("IT search finds employees", resp["type"] == "table" and len(resp.get("data", [])) > 0)

# Category count — Top Notch
resp = process_query("How many employees are Top Notch?")
check("Top Notch count query works", resp["type"] == "text" and "Top Notch" in resp.get("content", ""))

# Category count — Below Average
resp = process_query("How many employees are Below Average?")
check("Below Average count query works", resp["type"] == "text" and "Below Average" in resp.get("content", ""))

# Highest score
resp = process_query("Who has the highest latest appraisal score?")
check("Highest score query works", resp["type"] == "text" and "highest" in resp.get("content", "").lower() or "Score" in resp.get("content", ""))

# Not appraised
resp = process_query("Which employees have not been appraised?")
check("Not appraised query works", resp["type"] in ("text", "table"))

# Latest appraisal for specific employee
resp = process_query("Show latest appraisal for employee E105")
check("Latest appraisal for E105 works", resp["type"] == "text" and "E105" in resp.get("content", ""))

# Feedback history
resp = process_query("Show feedback history for employee E102")
check("Feedback history for E102 works", resp["type"] == "table")

# Non-existent employee
resp = process_query("Show details for employee E999")
check("Non-existent E999 handled gracefully", resp["type"] == "text" and ("No employee" in resp.get("content", "") or "not found" in resp.get("content", "").lower()))

# Unsupported question
resp = process_query("What is the weather today?")
check("Unsupported question handled gracefully", resp["type"] == "text")

# Category breakdown
resp = process_query("Show performance breakdown by category")
check("Category breakdown query works", resp["type"] in ("text", "table"))

# ══════════════════════════════════════════════════════════════
# 9. Suggestions Tests
# ══════════════════════════════════════════════════════════════
print("\n[9] Suggestions Tests")
result = get_suggestions_for_employee("E103")
check("E103 suggestions returned", result.get("error") is None)
check("E103 has category_suggestions", len(result.get("category_suggestions", [])) > 0)

result_na = get_suggestions_for_employee("E145")
check("E145 (not appraised) has suggestions", len(result_na.get("category_suggestions", [])) > 0)
check("E145 category is Not Appraised", result_na.get("category") == "Not Appraised")

result_bad = get_suggestions_for_employee("E999")
check("E999 returns error gracefully", result_bad.get("error") is not None)

# ══════════════════════════════════════════════════════════════
# Summary
# ══════════════════════════════════════════════════════════════
print("\n" + "="*60)
passed = sum(1 for _, s, _ in results if s == PASS)
failed = sum(1 for _, s, _ in results if s == FAIL)
total = len(results)
print(f"  RESULTS: {passed}/{total} passed  |  {failed} failed")
print("="*60 + "\n")

if failed > 0:
    print("Failed tests:")
    for name, status, detail in results:
        if status == FAIL:
            print(f"  ❌ {name}" + (f" — {detail}" if detail else ""))
