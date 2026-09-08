"""
LifeOS AI - Unified Context Service

Phase 6C:
Combines goals, memories, and user information
into a single context layer for the future AI assistant.
"""

from backend.goal_service import get_goals
from backend.memory_service import get_memories, find_relevant_memories


# ======================================================
# USER INFORMATION
# ======================================================

def get_user_information():
    """
    Return available user information.

    User information storage will be implemented
    in a later phase. For now, return a safe structure.
    """

    return {
        "name": "",
        "preferences": [],
        "interests": [],
        "notes": []
    }


# ======================================================
# GET GOAL CONTEXT
# ======================================================

def get_goal_context():
    """
    Retrieve all goals for unified context.
    """

    goals = get_goals()

    context_goals = []

    for goal in goals:

        context_goals.append({
            "id": goal.get("id"),
            "title": goal.get("title", ""),
            "description": goal.get("description", ""),
            "category": goal.get("category", ""),
            "priority": goal.get("priority", ""),
            "deadline": goal.get("deadline", ""),
            "status": goal.get("status", "Pending")
        })

    return context_goals


# ======================================================
# GET MEMORY CONTEXT
# ======================================================

def get_memory_context():
    """
    Retrieve all memories for unified context.
    """

    memories = get_memories()

    context_memories = []

    for memory in memories:

        context_memories.append({
            "id": memory.get("id"),
            "content": memory.get("content", ""),
            "category": memory.get("category", ""),
            "created_at": memory.get("created_at", "")
        })

    return context_memories


# ======================================================
# GET COMPLETE LIFEOS CONTEXT
# ======================================================

def get_user_context():
    """
    Build the complete LifeOS context.

    Combines:
        - User information
        - Goals
        - Memories
    """

    context = {
        "user": get_user_information(),
        "goals": get_goal_context(),
        "memories": get_memory_context()
    }

    return context


# ======================================================
# GET CONTEXT SUMMARY
# ======================================================

def get_context_summary():
    """
    Return a lightweight summary of the user's
    current LifeOS state.
    """

    goals = get_goal_context()
    memories = get_memory_context()
    user = get_user_information()

    total_goals = len(goals)

    completed_goals = sum(
        1
        for goal in goals
        if goal.get("status") == "Completed"
    )

    pending_goals = sum(
        1
        for goal in goals
        if goal.get("status") == "Pending"
    )

    return {
        "user": user,
        "total_goals": total_goals,
        "completed_goals": completed_goals,
        "pending_goals": pending_goals,
        "total_memories": len(memories)
    }


# ======================================================
# GET RELEVANT CONTEXT
# ======================================================

def get_context_for_query(query, limit=5):
    """
    Retrieve LifeOS context relevant to a user query.

    Uses lightweight intent detection and improved
    lexical relevance matching for goals and memories.
    """

    if not query or not query.strip():

        return {
            "query": query,
            "goals": [],
            "memories": [],
            "user": get_user_information()
        }

    original_query = query.strip()
    query = original_query.lower()

    # --------------------------------------------------
    # STOP WORDS
    # --------------------------------------------------

    stop_words = {
        "the", "a", "an", "and", "or", "but",
        "what", "what's", "which", "who", "where",
        "when", "how", "why",
        "are", "is", "am", "do", "does", "did",
        "my", "me", "i", "you", "your",
        "about", "for", "from", "with", "to",
        "of", "in", "on", "at",
        "currently", "please", "tell",
        "show", "give", "can", "could",
        "should", "would"
    }

    # --------------------------------------------------
    # NORMALIZE QUERY
    # --------------------------------------------------

    cleaned_query = query

    for character in [
        "?", "!", ".", ",", ";", ":",
        "(", ")", "[", "]", "{", "}",
        "'", '"'
    ]:
        cleaned_query = cleaned_query.replace(
            character,
            " "
        )

    query_words = {
        word.strip()
        for word in cleaned_query.split()
        if len(word.strip()) > 2
        and word.strip() not in stop_words
    }

    # --------------------------------------------------
    # GET ALL AVAILABLE DATA
    # --------------------------------------------------

    all_goals = get_goal_context()
    all_memories = get_memory_context()

    # --------------------------------------------------
    # INTENT DETECTION
    # --------------------------------------------------

    goal_keywords = {
        "goal",
        "goals",
        "target",
        "targets",
        "objective",
        "objectives",
        "focus",
        "priority",
        "priorities",
        "progress",
        "deadline",
        "deadlines",
        "task",
        "tasks"
    }

    memory_keywords = {
        "memory",
        "memories",
        "remember",
        "remembered",
        "recall",
        "past",
        "history",
        "know",
        "knowledge",
        "learn",
        "learning"
    }

    asks_about_goals = bool(
        set(query.split()).intersection(
            goal_keywords
        )
    )

    asks_about_memories = bool(
        set(query.split()).intersection(
            memory_keywords
        )
    )

    # --------------------------------------------------
    # RELEVANT GOALS
    # --------------------------------------------------

    relevant_goals = []

    if asks_about_goals:

        relevant_goals = [
            dict(goal)
            for goal in all_goals
        ]

    else:

        for goal in all_goals:

            goal_text = " ".join([
                str(goal.get("title", "")),
                str(goal.get("description", "")),
                str(goal.get("category", "")),
                str(goal.get("priority", "")),
                str(goal.get("status", ""))
            ]).lower()

            goal_text_clean = goal_text

            for character in [
                "?", "!", ".", ",", ";", ":",
                "(", ")", "[", "]", "{", "}",
                "'", '"'
            ]:
                goal_text_clean = goal_text_clean.replace(
                    character,
                    " "
                )

            goal_words = {
                word.strip()
                for word in goal_text_clean.split()
                if len(word.strip()) > 2
            }

            matching_words = query_words.intersection(
                goal_words
            )

            if matching_words:

                goal_copy = dict(goal)

                goal_copy["relevance_score"] = (
                    len(matching_words)
                )

                goal_copy["matching_terms"] = sorted(
                    matching_words
                )

                relevant_goals.append(
                    goal_copy
                )

    # --------------------------------------------------
    # HIGH PRIORITY GOALS
    # --------------------------------------------------

    if (
        "high priority" in query
        or "highest priority" in query
        or "important goal" in query
        or "important goals" in query
    ):

        relevant_goals = [
            dict(goal)
            for goal in all_goals
            if goal.get("priority") == "High"
            and goal.get("status") == "Pending"
        ]

    # --------------------------------------------------
    # CURRENT / ACTIVE GOALS
    # --------------------------------------------------

    if (
        "current goals" in query
        or "current goal" in query
        or "active goals" in query
        or "pending goals" in query
    ):

        relevant_goals = [
            dict(goal)
            for goal in all_goals
            if goal.get("status") == "Pending"
        ]

    # --------------------------------------------------
    # RELEVANT MEMORIES
    # --------------------------------------------------

    relevant_memories = []

    # Generic memory questions should return memories.
    if asks_about_memories and not query_words:

        relevant_memories = [
            dict(memory)
            for memory in all_memories
        ]

    elif asks_about_memories:

        # First try relevance matching.
        for memory in all_memories:

            memory_text = " ".join([
                str(memory.get("content", "")),
                str(memory.get("category", ""))
            ]).lower()

            memory_text_clean = memory_text

            for character in [
                "?", "!", ".", ",", ";", ":",
                "(", ")", "[", "]", "{", "}",
                "'", '"'
            ]:
                memory_text_clean = (
                    memory_text_clean.replace(
                        character,
                        " "
                    )
                )

            memory_words = {
                word.strip()
                for word in memory_text_clean.split()
                if len(word.strip()) > 2
            }

            matching_words = query_words.intersection(
                memory_words
            )

            if matching_words:

                memory_copy = dict(memory)

                memory_copy["relevance_score"] = (
                    len(matching_words)
                )

                memory_copy["matching_terms"] = sorted(
                    matching_words
                )

                relevant_memories.append(
                    memory_copy
                )

        # If the user explicitly asks for memories but
        # no specific terms match, show available memories.
        if not relevant_memories:

            relevant_memories = [
                dict(memory)
                for memory in all_memories
            ]

    else:

        # Normal contextual query.
        # First use the existing intelligent retrieval.
        relevant_memories = find_relevant_memories(
            query,
            limit
        )

        # If that retrieval produces nothing,
        # perform a simple fallback search.
        if not relevant_memories:

            for memory in all_memories:

                memory_text = " ".join([
                    str(memory.get("content", "")),
                    str(memory.get("category", ""))
                ]).lower()

                memory_words = set(
                    word.strip(
                        ".,!?;:()[]{}\"'"
                    )
                    for word in memory_text.split()
                    if len(
                        word.strip(
                            ".,!?;:()[]{}\"'"
                        )
                    ) > 2
                )

                matching_words = query_words.intersection(
                    memory_words
                )

                if matching_words:

                    memory_copy = dict(memory)

                    memory_copy[
                        "relevance_score"
                    ] = len(matching_words)

                    memory_copy[
                        "matching_terms"
                    ] = sorted(
                        matching_words
                    )

                    relevant_memories.append(
                        memory_copy
                    )

    # --------------------------------------------------
    # FOCUS QUESTIONS
    # --------------------------------------------------

    if "focus" in query:

        relevant_goals = [
            dict(goal)
            for goal in all_goals
            if goal.get("status") == "Pending"
        ]

    # --------------------------------------------------
    # SORT GOALS
    # --------------------------------------------------

    relevant_goals.sort(
        key=lambda goal: (
            goal.get("priority") == "High",
            goal.get("status") == "Pending",
            goal.get("relevance_score", 0)
        ),
        reverse=True
    )

    # --------------------------------------------------
    # SORT MEMORIES
    # --------------------------------------------------

    relevant_memories.sort(
        key=lambda memory: (
            memory.get(
                "relevance_score",
                0
            )
        ),
        reverse=True
    )

    # --------------------------------------------------
    # LIMIT RESULTS
    # --------------------------------------------------

    relevant_goals = relevant_goals[:limit]
    relevant_memories = relevant_memories[:limit]

    # --------------------------------------------------
    # RETURN UNIFIED CONTEXT
    # --------------------------------------------------

    return {
        "query": original_query,
        "user": get_user_information(),
        "goals": relevant_goals,
        "memories": relevant_memories
    }

# ======================================================
# FORMAT CONTEXT FOR AI
# ======================================================

def format_context_for_ai(context):
    """
    Convert structured LifeOS context into a clean
    text format that can later be passed to an AI model.
    """

    lines = []

    lines.append("LIFEOS USER CONTEXT")
    lines.append("===================")

    # --------------------------------------------------
    # USER
    # --------------------------------------------------

    user = context.get("user", {})

    lines.append("")
    lines.append("USER INFORMATION")
    lines.append("----------------")

    if user.get("name"):

        lines.append(
            f"Name: {user['name']}"
        )

    if user.get("preferences"):

        lines.append(
            "Preferences: "
            + ", ".join(user["preferences"])
        )

    if user.get("interests"):

        lines.append(
            "Interests: "
            + ", ".join(user["interests"])
        )

    # --------------------------------------------------
    # GOALS
    # --------------------------------------------------

    lines.append("")
    lines.append("GOALS")
    lines.append("-----")

    goals = context.get("goals", [])

    if not goals:

        lines.append("No goals available.")

    else:

        for goal in goals:

            lines.append(
                f"- {goal.get('title', '')}"
            )

            lines.append(
                f"  Status: {goal.get('status', '')}"
            )

            lines.append(
                f"  Priority: {goal.get('priority', '')}"
            )

            lines.append(
                f"  Category: {goal.get('category', '')}"
            )

            lines.append(
                f"  Deadline: {goal.get('deadline', '')}"
            )

    # --------------------------------------------------
    # MEMORIES
    # --------------------------------------------------

    lines.append("")
    lines.append("MEMORIES")
    lines.append("--------")

    memories = context.get("memories", [])

    if not memories:

        lines.append("No memories available.")

    else:

        for memory in memories:

            lines.append(
                f"- {memory.get('content', '')}"
            )

            if memory.get("category"):

                lines.append(
                    f"  Category: "
                    f"{memory.get('category')}"
                )

    return "\n".join(lines)
# ======================================================
# GOAL → MEMORY INTELLIGENCE
# ======================================================

def find_memories_for_goal(goal_id, limit=5):

    goals = get_goals()

    goal = None

    for item in goals:

        if item.get("id") == goal_id:
            goal = item
            break

    if not goal:
        return []

    goal_text = " ".join([
        str(goal.get("title", "")),
        str(goal.get("description", "")),
        str(goal.get("category", "")),
        str(goal.get("priority", ""))
    ]).lower()

    goal_words = set(
        word.strip(".,!?;:()[]{}\"'")
        for word in goal_text.split()
        if len(word.strip(".,!?;:()[]{}\"'")) > 2
    )

    memories = get_memories()

    results = []

    for memory in memories:

        memory_text = " ".join([
            str(memory.get("content", "")),
            str(memory.get("category", ""))
        ]).lower()

        memory_words = set(
            word.strip(".,!?;:()[]{}\"'")
            for word in memory_text.split()
            if len(word.strip(".,!?;:()[]{}\"'")) > 2
        )

        matching_words = goal_words.intersection(
            memory_words
        )

        if matching_words:

            memory_copy = dict(memory)

            memory_copy["relevance_score"] = len(
                matching_words
            )

            memory_copy["matching_terms"] = sorted(
                matching_words
            )

            results.append(memory_copy)

    results.sort(
        key=lambda item: item["relevance_score"],
        reverse=True
    )

    return results[:limit]