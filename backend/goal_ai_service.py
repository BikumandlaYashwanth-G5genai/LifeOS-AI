"""
LifeOS AI - Smart Goal Intelligence

Phase 7A:
Uses Gemini and the existing LifeOS goal/context
services to analyze goals and provide useful
recommendations.
"""

from backend.goal_service import get_goals
from backend.context_service import (
    get_context_for_query,
    format_context_for_ai
)
from backend.ai_service import client, MODEL_NAME


# ======================================================
# BUILD GOAL ANALYSIS PROMPT
# ======================================================

def build_goal_analysis_prompt(goals):
    """
    Build a prompt for Gemini to analyze
    the user's current goals.
    """

    if not goals:

        return """
You are LifeOS AI.

The user currently has no goals.

Give a short, encouraging response explaining
that they should create their first meaningful
goal.
"""

    context = {
        "user": {},
        "goals": goals,
        "memories": []
    }

    formatted_context = format_context_for_ai(
        context
    )

    prompt = f"""
You are LifeOS AI, a personal goal-management
assistant.

Analyze the user's current goals.

Use ONLY the goal information provided below.

{formatted_context}

Provide a useful analysis containing:

1. Overall progress
2. High-priority goals
3. Goals that may need attention
4. Upcoming or important deadlines
5. Recommended focus
6. Practical next steps

Keep the response clear and concise.

Do not invent goals, deadlines, or personal
information that is not present in the data.

Use simple language that is useful to the user.
"""

    return prompt


# ======================================================
# ANALYZE ALL GOALS
# ======================================================

def analyze_goals():
    """
    Analyze all current goals using Gemini.
    """

    if client is None:

        return (
            "Gemini is not configured. "
            "Please check your API key."
        )

    goals = get_goals()

    prompt = build_goal_analysis_prompt(
        goals
    )

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response and response.text:

            return response.text.strip()

        return (
            "I couldn't generate a goal analysis "
            "right now."
        )

    except Exception as error:

        print(
            "Goal AI error:",
            error
        )

        return (
            "Sorry, I couldn't analyze your goals "
            "right now."
        )


# ======================================================
# ANALYZE A SPECIFIC GOAL
# ======================================================

def analyze_goal(goal_id):
    """
    Analyze one specific goal.
    """

    if client is None:

        return (
            "Gemini is not configured. "
            "Please check your API key."
        )

    goals = get_goals()

    selected_goal = None

    for goal in goals:

        if goal.get("id") == goal_id:

            selected_goal = goal

            break

    if selected_goal is None:

        return "Goal not found."

    context = {
        "user": {},
        "goals": [selected_goal],
        "memories": []
    }

    formatted_context = format_context_for_ai(
        context
    )

    prompt = f"""
You are LifeOS AI.

Analyze the following goal:

{formatted_context}

Provide:

1. Goal assessment
2. Potential challenges
3. Recommended next action
4. Suggested way to make progress
5. Deadline awareness

Be practical and concise.

Do not invent information.
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response and response.text:

            return response.text.strip()

        return (
            "I couldn't analyze this goal "
            "right now."
        )

    except Exception as error:

        print(
            "Goal analysis error:",
            error
        )

        return (
            "Sorry, I couldn't analyze this goal "
            "right now."
        )


# ======================================================
# GET SMART RECOMMENDATION
# ======================================================

def get_goal_recommendation():
    """
    Generate a concise recommendation about
    what the user should focus on.
    """

    if client is None:

        return (
            "Gemini is not configured."
        )

    goals = get_goals()

    if not goals:

        return (
            "You don't have any goals yet. "
            "Consider creating your first goal."
        )

    context = {
        "user": {},
        "goals": goals,
        "memories": []
    }

    formatted_context = format_context_for_ai(
        context
    )

    prompt = f"""
You are LifeOS AI.

Look at these current goals:

{formatted_context}

Determine the single most useful thing
the user should focus on next.

Consider:

- Priority
- Status
- Deadline
- Practical urgency

Give the answer in this format:

FOCUS:
<one clear recommendation>

WHY:
<short explanation>

NEXT STEP:
<one concrete action>

Do not invent information.
"""

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response and response.text:

            return response.text.strip()

        return (
            "I couldn't generate a recommendation."
        )

    except Exception as error:

        print(
            "Goal recommendation error:",
            error
        )

        return (
            "Sorry, I couldn't generate a "
            "recommendation right now."
        )