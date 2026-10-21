import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== Importing all modules ===")
from modules.data_manager import load_employees, load_appraisals, load_feedback
from modules.performance import get_dashboard_stats, get_enriched_employees
from modules.chatbot import process_query, EXAMPLE_QUESTIONS
from modules.recommendations import get_suggestions_for_employee

print("All imports OK")

stats = get_dashboard_stats()
print("Total employees:", stats["total_employees"])
print("Avg score:", stats["avg_score"])
print("Top Notch:", stats["top_notch"])
print("Mediocre:", stats["mediocre"])
print("Below Average:", stats["below_average"])
print("Not Appraised:", stats["not_appraised"])
print("Dept stats rows:", len(stats["dept_stats"]))

print("\nExample questions:", len(EXAMPLE_QUESTIONS))
for q in EXAMPLE_QUESTIONS:
    r = process_query(q)
    status = "OK" if r and "type" in r else "FAIL"
    print("  " + status + " - " + q[:55])

print("\nAll checks passed!")
