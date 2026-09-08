"""
LifeOS AI - Smart Memory Intelligence

Phase 7B:
AI-powered analysis of stored memories.
"""
import streamlit as st
import os
from google import genai

from backend.memory_service import (
    get_memories,
    find_relevant_memories
)


# ======================================================
# GEMINI CLIENT
# ======================================================

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if API_KEY:
    client = genai.Client(
        api_key=API_KEY
    )


MODEL_NAME = "gemini-3.6-flash"


# ======================================================
# GEMINI REQUEST
# ======================================================

def ask_gemini(prompt):
    """
    Send a prompt to Gemini and return the response.
    """

    if client is None:

        return (
            "Gemini API is not configured. "
            "Please check your GEMINI_API_KEY."
        )

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:

     st.error(
        f"Gemini Error: {e}"
    )

    return (
        "Memory analysis failed. "
        "Check the error above."
    )


# ======================================================
# FORMAT MEMORIES
# ======================================================

def format_memories(memories):
    """
    Convert memories into clean text for Gemini.
    """

    if not memories:

        return "No memories are currently stored."

    lines = []

    for index, memory in enumerate(
        memories,
        start=1
    ):

        content = memory.get(
            "content",
            ""
        )

        category = memory.get(
            "category",
            ""
        )

        created_at = memory.get(
            "created_at",
            ""
        )

        lines.append(
            f"Memory {index}:"
        )

        lines.append(
            f"Content: {content}"
        )

        if category:

            lines.append(
                f"Category: {category}"
            )

        if created_at:

            lines.append(
                f"Created: {created_at}"
            )

        lines.append("")

    return "\n".join(lines)


# ======================================================
# ANALYZE ALL MEMORIES
# ======================================================

def analyze_memories():
    """
    Ask Gemini to analyze the user's stored memories.
    """

    memories = get_memories()

    if not memories:

        return (
            "There are no memories available "
            "to analyze yet."
        )

    memory_text = format_memories(
        memories
    )

    prompt = f"""
You are the Smart Memory Intelligence
component of LifeOS.

Analyze the user's stored memories.

Identify:

1. Important themes
2. Recurring interests
3. Useful patterns
4. Important personal or academic context
5. Potentially useful information for future assistance

Do not invent facts.

Only use information contained
in the memories below.

Keep the response clear and practical.

STORED MEMORIES
===============

{memory_text}
"""

    return ask_gemini(
        prompt
    )


# ======================================================
# SUMMARIZE MEMORIES
# ======================================================

def summarize_memories():
    """
    Generate a concise summary of stored memories.
    """

    memories = get_memories()

    if not memories:

        return (
            "There are no memories available "
            "to summarize yet."
        )

    memory_text = format_memories(
        memories
    )

    prompt = f"""
You are a memory summarization assistant
for LifeOS.

Create a concise but useful summary
of the user's stored memories.

Group related information together.

Focus on information that could help
a future personal AI assistant understand
the user better.

Do not invent information.

STORED MEMORIES
===============

{memory_text}
"""

    return ask_gemini(
        prompt
    )


# ======================================================
# MEMORY INSIGHTS
# ======================================================

def get_memory_insights():
    """
    Generate useful insights from memories.
    """

    memories = get_memories()

    if not memories:

        return (
            "There are no memories available "
            "for generating insights."
        )

    memory_text = format_memories(
        memories
    )

    prompt = f"""
You are LifeOS Smart Memory Intelligence.

Review the user's stored memories and
identify useful observations.

Look for:

- recurring interests
- repeated activities
- important projects
- learning patterns
- preferences explicitly mentioned
- information that may help future assistance

Separate observations from assumptions.

Do not invent facts.

STORED MEMORIES
===============

{memory_text}
"""

    return ask_gemini(
        prompt
    )


# ======================================================
# SMART MEMORY SEARCH
# ======================================================

def smart_memory_search(query, limit=5):
    """
    Retrieve memories relevant to a natural-language query.
    """

    if not query or not query.strip():

        return []

    memories = find_relevant_memories(
        query,
        limit
    )

    return memories


# ======================================================
# EXPLAIN MEMORY RELEVANCE
# ======================================================

def explain_memory_relevance(
    query,
    memories
):
    """
    Ask Gemini why retrieved memories are
    relevant to a user's query.
    """

    if not memories:

        return (
            "No relevant memories were found."
        )

    memory_text = format_memories(
        memories
    )

    prompt = f"""
You are LifeOS Smart Memory Intelligence.

The user asked:

"{query}"

Below are memories retrieved from
the user's stored information.

Explain briefly why these memories
are relevant to the user's query.

Only use information contained
in the memories.

Do not invent facts.

RELEVANT MEMORIES
=================

{memory_text}
"""

    return ask_gemini(
        prompt
    )