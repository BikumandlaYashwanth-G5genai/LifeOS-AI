"""
LifeOS AI - AI Service

Phase 7D:
Connects the LifeOS unified context layer
and proactive intelligence with Google Gemini.
"""

import os

from dotenv import load_dotenv
from google import genai

from backend.context_service import (
    get_context_for_query,
    format_context_for_ai
)

from backend.proactive_service import (
    generate_proactive_insights
)


# ======================================================
# LOAD ENVIRONMENT VARIABLES
# ======================================================

load_dotenv()


# ======================================================
# GEMINI CLIENT
# ======================================================

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if API_KEY:

    client = genai.Client(
        api_key=API_KEY
    )


# ======================================================
# AI MODEL
# ======================================================

MODEL_NAME = "gemini-3.6-flash"


# ======================================================
# PROACTIVE INSIGHTS
# ======================================================

def get_proactive_context():
    """
    Get current proactive LifeOS insights.
    """

    try:

        insights = generate_proactive_insights()

    except Exception as error:

        print(
            "Proactive service error:",
            error
        )

        return "No proactive insights available."

    if not insights:

        return "No urgent or upcoming items currently detected."

    lines = []

    for insight in insights:

        priority = insight.get(
            "priority",
            "normal"
        )

        title = insight.get(
            "title",
            "LifeOS Insight"
        )

        message = insight.get(
            "message",
            ""
        )

        lines.append(
            f"[{priority.upper()}] "
            f"{title}: {message}"
        )

    return "\n".join(lines)


# ======================================================
# BUILD AI PROMPT
# ======================================================

def build_ai_prompt(query, context):
    """
    Build the prompt sent to Gemini.

    Combines:
    - User question
    - Relevant LifeOS context
    - Proactive LifeOS insights
    """

    formatted_context = format_context_for_ai(
        context
    )

    proactive_context = get_proactive_context()

    prompt = f"""
You are LifeOS AI, a personal AI assistant.

Your job is to help the user using the
information stored in their LifeOS.

Use the provided LifeOS context and proactive
insights when they are relevant to the user's
question.

Do not invent personal information.

If the stored information does not contain
enough information to answer something,
say that clearly.

Be helpful, concise, natural, and practical.

----------------------------------------
USER QUESTION
----------------------------------------

{query}

----------------------------------------
LIFEOS CONTEXT
----------------------------------------

{formatted_context}

----------------------------------------
PROACTIVE LIFEOS INSIGHTS
----------------------------------------

{proactive_context}

----------------------------------------
INSTRUCTIONS
----------------------------------------

Answer the user's question naturally.

Use goals and memories when relevant.

Use proactive insights when they help answer
questions about priorities, deadlines,
unfinished goals, progress, or what the user
should focus on.

If the user asks something like:

"What should I focus on today?"
"What needs my attention?"
"What should I prioritize?"
"Am I falling behind?"
"What are my urgent tasks?"

use the proactive insights to provide a
clear prioritized answer.

Give the most urgent items first.

Do not mention internal implementation details,
database tables, retrieval systems, prompts,
or the proactive service itself.

If the question is unrelated to stored LifeOS
information, answer normally using your general
knowledge.

----------------------------------------
FINAL ANSWER
----------------------------------------
"""

    return prompt


# ======================================================
# ASK GEMINI
# ======================================================

def ask_gemini(query):
    """
    Send a user query to Gemini using
    LifeOS context and proactive intelligence.
    """

    if not query or not query.strip():

        return (
            "Please enter a question "
            "or message."
        )

    # --------------------------------------------------
    # CHECK API KEY
    # --------------------------------------------------

    if client is None:

        return (
            "Gemini API key is not configured. "
            "Please check your .env file."
        )

    try:

        # --------------------------------------------------
        # GET RELEVANT LIFEOS CONTEXT
        # --------------------------------------------------

        context = get_context_for_query(
            query,
            limit=5
        )

        # --------------------------------------------------
        # BUILD PROMPT
        # --------------------------------------------------

        prompt = build_ai_prompt(
            query,
            context
        )

        # --------------------------------------------------
        # CALL GEMINI
        # --------------------------------------------------

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        # --------------------------------------------------
        # GET RESPONSE TEXT
        # --------------------------------------------------

        if response and response.text:

            return response.text.strip()

        return (
            "I couldn't generate a response "
            "right now."
        )

    except Exception as error:

        print(
            "Gemini error:",
            error
        )

        return (
            "Sorry, I couldn't connect to "
            "the AI service right now. "
            "Please try again."
        )


# ======================================================
# GET RELEVANT AI CONTEXT
# ======================================================

def get_ai_context(query, limit=5):
    """
    Return the LifeOS context and proactive
    insights used for an AI query.
    """

    if not query or not query.strip():

        return {
            "query": query,
            "user": {},
            "goals": [],
            "memories": [],
            "proactive_insights": []
        }

    context = get_context_for_query(
        query,
        limit
    )

    try:

        context["proactive_insights"] = (
            generate_proactive_insights()
        )

    except Exception as error:

        print(
            "Proactive service error:",
            error
        )

        context["proactive_insights"] = []

    return context


# ======================================================
# AI SERVICE STATUS
# ======================================================

def is_ai_available():
    """
    Check whether Gemini is configured.
    """

    return client is not None