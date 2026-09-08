"""
LifeOS AI - Proactive Intelligence Service

Phase 7D:
Provides proactive analysis of goals, deadlines,
priorities, and LifeOS activity.
"""

from datetime import datetime

from backend.goal_service import (
    get_goals,
    get_dashboard_statistics,
    get_upcoming_deadlines,
    get_high_priority_goals,
)


# ======================================================
# DATE HELPERS
# ======================================================

def parse_deadline(deadline):
    """
    Convert a stored deadline into a datetime object.

    Supports common LifeOS date formats.
    """

    if not deadline:
        return None

    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
    ]

    for date_format in formats:

        try:
            return datetime.strptime(
                str(deadline),
                date_format
            )

        except ValueError:
            continue

    return None


# ======================================================
# GET DAYS UNTIL DEADLINE
# ======================================================

def get_days_until_deadline(deadline):
    """
    Return the number of days remaining
    until a deadline.
    """

    deadline_date = parse_deadline(deadline)

    if not deadline_date:
        return None

    today = datetime.now().date()

    return (
        deadline_date.date() - today
    ).days


# ======================================================
# OVERDUE GOALS
# ======================================================

def get_overdue_goals():
    """
    Return pending goals whose deadlines have passed.
    """

    goals = get_goals()

    overdue = []

    for goal in goals:

        if goal.get("status") != "Pending":
            continue

        days_left = get_days_until_deadline(
            goal.get("deadline")
        )

        if days_left is not None and days_left < 0:

            goal["days_overdue"] = abs(days_left)

            overdue.append(goal)

    overdue.sort(
        key=lambda goal: goal.get(
            "days_overdue",
            0
        ),
        reverse=True
    )

    return overdue


# ======================================================
# APPROACHING DEADLINES
# ======================================================

def get_approaching_deadlines(days=7):
    """
    Return pending goals whose deadlines are
    within the specified number of days.
    """

    goals = get_goals()

    approaching = []

    for goal in goals:

        if goal.get("status") != "Pending":
            continue

        days_left = get_days_until_deadline(
            goal.get("deadline")
        )

        if (
            days_left is not None
            and 0 <= days_left <= days
        ):

            goal["days_remaining"] = days_left

            approaching.append(goal)

    approaching.sort(
        key=lambda goal: goal.get(
            "days_remaining",
            9999
        )
    )

    return approaching


# ======================================================
# HIGH PRIORITY ATTENTION
# ======================================================

def get_goals_needing_attention():
    """
    Identify goals that deserve immediate attention.
    """

    goals = get_goals()

    attention_goals = []

    for goal in goals:

        if goal.get("status") != "Pending":
            continue

        priority = str(
            goal.get("priority", "")
        ).lower()

        days_left = get_days_until_deadline(
            goal.get("deadline")
        )

        # High priority goals
        if priority == "high":

            goal["attention_reason"] = (
                "High priority pending goal"
            )

            attention_goals.append(goal)

        # Deadlines within 3 days
        elif (
            days_left is not None
            and 0 <= days_left <= 3
        ):

            goal["attention_reason"] = (
                "Deadline approaching"
            )

            attention_goals.append(goal)

        # Overdue goals
        elif (
            days_left is not None
            and days_left < 0
        ):

            goal["attention_reason"] = (
                "Goal is overdue"
            )

            attention_goals.append(goal)

    return attention_goals


# ======================================================
# PROACTIVE INSIGHTS
# ======================================================

def generate_proactive_insights():
    """
    Generate human-readable proactive insights
    from the current LifeOS state.
    """

    insights = []

    overdue = get_overdue_goals()

    approaching = get_approaching_deadlines()

    high_priority = get_high_priority_goals(
        limit=5
    )

    statistics = get_dashboard_statistics()

    # --------------------------------------------------
    # OVERDUE
    # --------------------------------------------------

    for goal in overdue:

        insights.append({
            "type": "overdue",
            "priority": "critical",
            "title": "Overdue Goal",
            "message": (
                f"'{goal.get('title', '')}' "
                f"is overdue by "
                f"{goal.get('days_overdue', 0)} day(s)."
            ),
            "goal_id": goal.get("id")
        })

    # --------------------------------------------------
    # APPROACHING DEADLINES
    # --------------------------------------------------

    for goal in approaching:

        days = goal.get(
            "days_remaining",
            0
        )

        if days == 0:

            message = (
                f"'{goal.get('title', '')}' "
                f"is due today."
            )

        elif days == 1:

            message = (
                f"'{goal.get('title', '')}' "
                f"is due tomorrow."
            )

        else:

            message = (
                f"'{goal.get('title', '')}' "
                f"is due in {days} days."
            )

        insights.append({
            "type": "deadline",
            "priority": "high",
            "title": "Upcoming Deadline",
            "message": message,
            "goal_id": goal.get("id")
        })

    # --------------------------------------------------
    # HIGH PRIORITY
    # --------------------------------------------------

    for goal in high_priority:

        # Avoid excessive duplicate alerts
        # for goals already covered above.

        goal_id = goal.get("id")

        already_added = any(
            insight.get("goal_id") == goal_id
            for insight in insights
        )

        if already_added:
            continue

        insights.append({
            "type": "priority",
            "priority": "medium",
            "title": "High Priority Goal",
            "message": (
                f"'{goal.get('title', '')}' "
                f"is a high-priority goal that "
                f"still needs attention."
            ),
            "goal_id": goal_id
        })

    # --------------------------------------------------
    # GENERAL PROGRESS
    # --------------------------------------------------

    total = statistics.get(
        "total",
        0
    )

    completed = statistics.get(
        "completed",
        0
    )

    pending = statistics.get(
        "pending",
        0
    )

    if total == 0:

        insights.append({
            "type": "general",
            "priority": "low",
            "title": "Get Started",
            "message": (
                "You don't have any goals yet. "
                "Consider adding a goal to get started."
            )
        })

    elif pending > 0 and completed == 0:

        insights.append({
            "type": "general",
            "priority": "low",
            "title": "Goals Waiting",
            "message": (
                f"You currently have {pending} "
                f"pending goal(s). Consider "
                f"starting with the highest-priority one."
            )
        })

    # --------------------------------------------------
    # SORT INSIGHTS
    # --------------------------------------------------

    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3
    }

    insights.sort(
        key=lambda insight: priority_order.get(
            insight.get("priority"),
            99
        )
    )

    return insights


# ======================================================
# DAILY BRIEFING DATA
# ======================================================

def get_daily_briefing():
    """
    Return the information required for a
    LifeOS daily briefing.
    """

    statistics = get_dashboard_statistics()

    overdue = get_overdue_goals()

    approaching = get_approaching_deadlines(
        days=7
    )

    high_priority = get_high_priority_goals(
        limit=5
    )

    insights = generate_proactive_insights()

    return {
        "date": datetime.now().strftime(
            "%Y-%m-%d"
        ),
        "statistics": statistics,
        "overdue": overdue,
        "approaching": approaching,
        "high_priority": high_priority,
        "insights": insights
    }


# ======================================================
# PROACTIVE SERVICE STATUS
# ======================================================

def is_proactive_service_available():
    """
    Check whether the proactive intelligence
    service is available.
    """

    try:

        get_goals()

        return True

    except Exception:

        return False