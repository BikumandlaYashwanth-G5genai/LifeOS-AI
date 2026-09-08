import streamlit as st

from backend.context_service import (
    get_user_context,
    get_context_summary,
    get_context_for_query,
    format_context_for_ai
)


# ======================================================
# USER CONTEXT
# ======================================================

def show_user_context(context):

    st.subheader("👤 User Context")

    user = context.get("user", {})

    if user.get("name"):
        st.write(f"**Name:** {user['name']}")
    else:
        st.info("User information will be added later.")

    if user.get("preferences"):
        st.write(
            "**Preferences:** "
            + ", ".join(user["preferences"])
        )

    if user.get("interests"):
        st.write(
            "**Interests:** "
            + ", ".join(user["interests"])
        )


# ======================================================
# GOALS
# ======================================================

def show_goal_context(context):

    st.subheader("🎯 Goals")

    goals = context.get("goals", [])

    if not goals:
        st.info("No goals available.")
        return

    for goal in goals:

        with st.container(border=True):

            st.markdown(
                f"### {goal.get('title', '')}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    f"**Status:** "
                    f"{goal.get('status', '')}"
                )

                st.write(
                    f"**Priority:** "
                    f"{goal.get('priority', '')}"
                )

            with col2:
                st.write(
                    f"**Category:** "
                    f"{goal.get('category', '')}"
                )

                st.write(
                    f"**Deadline:** "
                    f"{goal.get('deadline', '')}"
                )

            if goal.get("description"):
                st.write(
                    f"**Description:** "
                    f"{goal.get('description')}"
                )


# ======================================================
# MEMORIES
# ======================================================

def show_memory_context(context):

    st.subheader("🧠 Memories")

    memories = context.get("memories", [])

    if not memories:
        st.info("No memories available.")
        return

    for memory in memories:

        with st.container(border=True):

            st.write(
                memory.get("content", "")
            )

            if memory.get("category"):
                st.caption(
                    f"Category: "
                    f"{memory.get('category')}"
                )

            if memory.get("created_at"):
                st.caption(
                    f"Created: "
                    f"{memory.get('created_at')}"
                )


# ======================================================
# CONTEXT SUMMARY
# ======================================================

def show_context_summary():

    summary = get_context_summary()

    st.subheader("📊 LifeOS Context Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Goals",
            summary.get("total_goals", 0)
        )

    with col2:
        st.metric(
            "Completed",
            summary.get("completed_goals", 0)
        )

    with col3:
        st.metric(
            "Pending",
            summary.get("pending_goals", 0)
        )

    with col4:
        st.metric(
            "Memories",
            summary.get("total_memories", 0)
        )


# ======================================================
# CONTEXT SEARCH
# ======================================================

def show_context_search():

    st.subheader("🔎 Search LifeOS Context")

    # --------------------------------------------------
    # SEARCH FORM
    # --------------------------------------------------

    with st.form(
        "context_search_form",
        clear_on_submit=True
    ):

        query = st.text_input(
            "Ask about your stored context",
            placeholder=(
                "Example: What are my current goals?"
            ),
            key="context_search_input"
        )

        submitted = st.form_submit_button(
            "🔎 Search Context",
            use_container_width=True
        )

    # --------------------------------------------------
    # BEFORE SEARCH
    # --------------------------------------------------

    if not submitted:

        st.info(
            "Enter a query to retrieve relevant "
            "goals and memories."
        )

        return

    if not query.strip():

        st.warning(
            "Please enter a query."
        )

        return

    # --------------------------------------------------
    # GET RELEVANT CONTEXT
    # --------------------------------------------------

    context = get_context_for_query(
        query,
        limit=5
    )

    goals = context.get("goals", [])
    memories = context.get("memories", [])

    # --------------------------------------------------
    # RELEVANT GOALS
    # --------------------------------------------------

    st.markdown("### 🎯 Relevant Goals")

    if goals:

        for goal in goals:

            st.write(
                f"**{goal.get('title', '')}** "
                f"— {goal.get('status', '')}"
            )

    else:

        st.info("No relevant goals found.")

    # --------------------------------------------------
    # RELEVANT MEMORIES
    # --------------------------------------------------

    st.markdown("### 🧠 Relevant Memories")

    if memories:

        for memory in memories:

            st.write(
                f"• {memory.get('content', '')}"
            )

    else:

        st.info("No relevant memories found.")

    # --------------------------------------------------
    # AI CONTEXT
    # --------------------------------------------------

    st.markdown("### 🤖 AI Context")

    formatted_context = format_context_for_ai(
        context
    )

    st.code(
        formatted_context,
        language="text"
    )


# ======================================================
# MAIN CONTEXT PAGE
# ======================================================

def context_page():

    st.title("🧩 Unified LifeOS Context")

    st.markdown(
        "Central context layer combining your "
        "goals, memories, and user information."
    )

    st.divider()

    # --------------------------------------------------
    # LOAD CONTEXT
    # --------------------------------------------------

    context = get_user_context()

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    show_context_summary()

    st.divider()

    # --------------------------------------------------
    # USER
    # --------------------------------------------------

    show_user_context(context)

    st.divider()

    # --------------------------------------------------
    # GOALS
    # --------------------------------------------------

    show_goal_context(context)

    st.divider()

    # --------------------------------------------------
    # MEMORIES
    # --------------------------------------------------

    show_memory_context(context)

    st.divider()

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------

    show_context_search()