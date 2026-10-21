"""
recommendations.py
Generates improvement suggestions based on performance classification and appraisal remarks.
"""

from modules.performance import (
    CATEGORY_TOP_NOTCH,
    CATEGORY_MEDIOCRE,
    CATEGORY_BELOW_AVERAGE,
    CATEGORY_NOT_APPRAISED,
    classify_performance,
)
from modules.data_manager import get_latest_appraisal, get_employee_by_id


# ──────────────────────────────────────────────────────────────────────────────
# Suggestion templates per category
# ──────────────────────────────────────────────────────────────────────────────

SUGGESTIONS = {
    CATEGORY_TOP_NOTCH: [
        {
            "title": "Advanced Technical Training",
            "detail": "Enroll in advanced certification programs (e.g., AWS, PMP, or domain-specific specializations) to further sharpen expertise.",
            "reason": "Top performers benefit most from high-level learning opportunities that match their current capability.",
        },
        {
            "title": "Leadership & Mentoring Role",
            "detail": "Assign junior team members for mentoring. Consider grooming for team lead or managerial responsibilities.",
            "reason": "High performers can accelerate team growth and build stronger succession pipelines.",
        },
        {
            "title": "Recognition & Reward Programs",
            "detail": "Nominate for Employee of the Month, performance bonuses, or public recognition in company communications.",
            "reason": "Recognition sustains high motivation and reinforces exceptional behavior.",
        },
        {
            "title": "High-Visibility Projects",
            "detail": "Assign to strategic or cross-functional projects where their skills can create maximum organizational impact.",
            "reason": "Top performers need challenges that match their capability to remain engaged and motivated.",
        },
        {
            "title": "Career Advancement Planning",
            "detail": "Create a structured career development plan with clear milestones toward promotion.",
            "reason": "Clear career paths prevent attrition of high performers and align individual growth with organizational goals.",
        },
    ],
    CATEGORY_MEDIOCRE: [
        {
            "title": "Targeted Skill Development Plan",
            "detail": "Identify specific skill gaps through a skill-gap analysis and enroll in targeted workshops or online courses.",
            "reason": "Focused training on identified weaknesses leads to faster, measurable improvement.",
        },
        {
            "title": "Regular Progress Reviews",
            "detail": "Schedule bi-monthly one-on-one check-ins with the manager to track progress and adjust goals.",
            "reason": "Consistent monitoring helps catch issues early and keeps the employee accountable.",
        },
        {
            "title": "Peer Collaboration & Knowledge Sharing",
            "detail": "Encourage participation in team workshops and cross-departmental knowledge-sharing sessions.",
            "reason": "Learning from peers in a collaborative environment builds confidence and expands knowledge base.",
        },
        {
            "title": "Goal Setting with SMART Framework",
            "detail": "Work with the manager to define Specific, Measurable, Achievable, Relevant, and Time-bound (SMART) goals.",
            "reason": "Clear goal structures provide direction and make performance measurement more objective.",
        },
        {
            "title": "Mid-cycle Appraisal Check-in",
            "detail": "Conduct an informal mid-appraisal-cycle review to provide timely feedback before the formal assessment.",
            "reason": "Early feedback allows course correction before performance issues become deeply entrenched.",
        },
    ],
    CATEGORY_BELOW_AVERAGE: [
        {
            "title": "Immediate Remedial Training Program",
            "detail": "Enroll in a structured remedial training program addressing core performance deficiencies identified in the appraisal.",
            "reason": "Foundational skill rebuilding is necessary before tackling advanced development goals.",
        },
        {
            "title": "Dedicated Mentorship Assignment",
            "detail": "Pair with a senior mentor for daily or weekly guidance. The mentor should provide both technical and emotional support.",
            "reason": "Personalized mentoring has proven to be one of the most effective interventions for underperforming employees.",
        },
        {
            "title": "Performance Improvement Plan (PIP)",
            "detail": "Formally document a Performance Improvement Plan with clear milestones, timelines, and consequences for non-compliance.",
            "reason": "A structured PIP creates accountability and provides a documented path to improvement.",
        },
        {
            "title": "Weekly Check-ins with Manager",
            "detail": "Implement mandatory weekly one-on-one meetings with the direct manager to review progress and remove blockers.",
            "reason": "Frequent touchpoints ensure that problems are caught early and the employee does not feel abandoned.",
        },
        {
            "title": "Follow-up Appraisal in 90 Days",
            "detail": "Schedule a follow-up appraisal within 90 days rather than waiting for the standard cycle to assess improvement.",
            "reason": "A shorter feedback cycle creates urgency and demonstrates organizational commitment to the employee's growth.",
        },
    ],
    CATEGORY_NOT_APPRAISED: [
        {
            "title": "Schedule Initial Appraisal",
            "detail": "An appraisal has not yet been conducted for this employee. Schedule one as soon as possible.",
            "reason": "Without an appraisal, it is impossible to assess performance or provide meaningful recommendations.",
        },
        {
            "title": "Onboarding Performance Review",
            "detail": "If the employee is relatively new, conduct a 90-day onboarding performance review to set expectations early.",
            "reason": "Early reviews help align new employees with company standards and catch onboarding gaps quickly.",
        },
    ],
}


# ──────────────────────────────────────────────────────────────────────────────
# Remark-based keyword detection
# ──────────────────────────────────────────────────────────────────────────────

REMARK_KEYWORDS = {
    "communication": "Communication Training: Consider enrolling in a business communication course to improve written and verbal interaction with teams.",
    "time management": "Time Management Workshop: Attend a time management or productivity workshop to improve deadline adherence and task prioritization.",
    "leadership": "Leadership Development: Participate in a leadership bootcamp or take on a team lead role in a small project.",
    "documentation": "Documentation Practices: Review and adopt standard documentation templates and practices used across the team.",
    "training": "Structured Training: Engage in a formal training program aligned with the identified skill gap.",
    "error": "Quality Assurance Habits: Implement a personal checklist or peer-review step before submitting work to reduce errors.",
    "errors": "Quality Assurance Habits: Implement a personal checklist or peer-review step before submitting work to reduce errors.",
    "collaboration": "Team Collaboration: Join cross-functional project teams to build stronger inter-departmental relationships.",
    "mentor": "Seek Mentorship: Request pairing with an experienced colleague for knowledge transfer and guidance.",
    "delay": "Scheduling & Planning: Use project management tools (e.g., Trello, Jira) to better plan and track tasks.",
    "deadline": "Deadline Management: Break tasks into smaller milestones and use calendar reminders to stay on track.",
    "roi": "ROI Analysis Training: Learn to track, measure, and report Return on Investment for better strategic alignment.",
    "vendor": "Vendor Relationship Management: Attend a workshop on negotiation and vendor partnership strategies.",
    "security": "Security Best Practices: Stay updated with the latest cybersecurity protocols and certifications.",
    "bug": "Testing & QA Practices: Adopt test-driven development and more rigorous code review practices to reduce bug escapes.",
    "forecast": "Forecasting & Analytics: Take a data analysis or financial modeling course to improve forecasting accuracy.",
}


def get_remark_based_suggestions(remarks: str) -> list:
    """
    Parse appraisal remarks for keywords and return specific suggestions.
    """
    if not remarks or not isinstance(remarks, str):
        return []

    remarks_lower = remarks.lower()
    found = []
    seen = set()

    for keyword, suggestion in REMARK_KEYWORDS.items():
        if keyword in remarks_lower and suggestion not in seen:
            found.append(suggestion)
            seen.add(suggestion)

    return found


def get_suggestions_for_employee(employee_id: str) -> dict:
    """
    Generate a full set of suggestions for an employee based on:
    1. Their performance classification (category-based suggestions)
    2. Keywords in their latest appraisal remarks

    Returns a dict with:
        - employee: employee Series or None
        - category: performance category string
        - score: latest score or None
        - category_suggestions: list of suggestion dicts
        - remark_suggestions: list of remark-based suggestion strings
        - error: error string or None
    """
    employee = get_employee_by_id(employee_id)
    if employee is None:
        return {"error": f"No employee found with ID '{employee_id}'.", "employee": None}

    latest_appraisal = get_latest_appraisal(employee_id)

    if latest_appraisal is not None:
        score = latest_appraisal.get("performance_score")
        remarks = latest_appraisal.get("remarks", "")
    else:
        score = None
        remarks = ""

    category = classify_performance(score)
    category_suggestions = SUGGESTIONS.get(category, [])
    remark_suggestions = get_remark_based_suggestions(remarks)

    return {
        "employee": employee,
        "category": category,
        "score": score,
        "remarks": remarks,
        "category_suggestions": category_suggestions,
        "remark_suggestions": remark_suggestions,
        "error": None,
    }
