import streamlit as st
from datetime import datetime, timezone, timedelta
from backend.memory_service import (
    add_memory,
    get_memories,
    search_memories,
    get_memories_by_category,
    get_recent_memories,
    delete_memory,
    update_memory,
    get_memory_statistics,
    find_relevant_memories
)
from backend.memory_ai_service import (
    analyze_memories,
    summarize_memories,
    get_memory_insights
)


# ======================================================
# CONSTANTS
# ======================================================

CATEGORIES = [
    "Personal",
    "Education",
    "Career",
    "Goals",
    "Preferences",
    "Ideas",
    "Other"
]


# ======================================================
# SMART MEMORY INTELLIGENCE
# ======================================================

def show_smart_memory_intelligence():
    """Display AI-powered memory intelligence."""

    st.subheader("🤖 Smart Memory Intelligence")

    st.markdown(
        "Use Gemini to understand patterns, themes, "
        "and useful insights from your stored memories."
    )

    memories = get_memories()

    if not memories:

        st.info(
            "Add some memories first to use "
            "Smart Memory Intelligence."
        )

        return

    # --------------------------------------------------
    # AI ACTIONS
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "🧠 Analyze Memories",
            use_container_width=True,
            key="ai_analyze_memories"
        ):

            with st.spinner(
                "Analyzing your memories..."
            ):

                result = analyze_memories()

            st.session_state[
                "memory_ai_analysis"
            ] = result

    with col2:

        if st.button(
            "📋 Summarize Memories",
            use_container_width=True,
            key="ai_summarize_memories"
        ):

            with st.spinner(
                "Creating memory summary..."
            ):

                result = summarize_memories()

            st.session_state[
                "memory_ai_summary"
            ] = result

    with col3:

        if st.button(
            "💡 Memory Insights",
            use_container_width=True,
            key="ai_memory_insights"
        ):

            with st.spinner(
                "Finding useful insights..."
            ):

                result = get_memory_insights()

            st.session_state[
                "memory_ai_insights"
            ] = result

    # --------------------------------------------------
    # ANALYSIS
    # --------------------------------------------------

    if st.session_state.get(
        "memory_ai_analysis"
    ):

        st.markdown(
            "### 🧠 Memory Analysis"
        )

        with st.container(border=True):

            st.markdown(
                st.session_state[
                    "memory_ai_analysis"
                ]
            )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    if st.session_state.get(
        "memory_ai_summary"
    ):

        st.markdown(
            "### 📋 Memory Summary"
        )

        with st.container(border=True):

            st.markdown(
                st.session_state[
                    "memory_ai_summary"
                ]
            )

    # --------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------

    if st.session_state.get(
        "memory_ai_insights"
    ):

        st.markdown(
            "### 💡 Memory Insights"
        )

        with st.container(border=True):

            st.markdown(
                st.session_state[
                    "memory_ai_insights"
                ]
            )

    st.divider()


# ======================================================
# MEMORY PAGE
# ======================================================

def memory_page():

    st.title("🧠 Memory Engine")

    st.markdown(
        "Store important information that LifeOS can remember for you."
    )

    st.divider()

    show_memory_statistics()

    st.divider()

    show_add_memory()

    st.divider()

    # --------------------------------------------------
    # SMART MEMORY INTELLIGENCE
    # --------------------------------------------------

    show_smart_memory_intelligence()

    # --------------------------------------------------
    # MEMORY SECTION
    # --------------------------------------------------

    show_memory_section()


# ======================================================
# MEMORY STATISTICS
# ======================================================

def show_memory_statistics():

    stats = get_memory_statistics()

    st.subheader("📊 Memory Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Memories",
            stats["total"]
        )

    with col2:
        st.metric(
            "Categories",
            stats["categories"]
        )

    with col3:
        st.metric(
            "Recent Memories",
            stats["recent"]
        )

    with col4:
        st.metric(
            "Top Category",
            stats["top_category"]
        )


# ======================================================
# ADD MEMORY
# ======================================================

def show_add_memory():

    st.subheader("➕ Add New Memory")

    with st.form(
        "add_memory_form",
        clear_on_submit=True
    ):

        content = st.text_area(
            "Memory",
            placeholder="Enter something important you want LifeOS to remember..."
        )

        category = st.selectbox(
            "Category",
            CATEGORIES
        )

        submitted = st.form_submit_button(
            "💾 Save Memory"
        )

        if submitted:

            if content.strip() == "":
                st.warning(
                    "Please enter a memory."
                )

                return

            add_memory(
                content,
                category
            )

            st.success(
                "Memory saved successfully!"
            )

            st.rerun()


# ======================================================
# MEMORY SECTION
# ======================================================

def show_memory_section():

    st.subheader("📚 Your Memories")

    # --------------------------------------------------
    # SEARCH
    # --------------------------------------------------
    search_mode = st.radio(
        "🔎 Search Mode",
        [
            "Standard Search",
            "Intelligent Search"
        ],
        horizontal=True
    )

    search_text = st.text_input(
        "🔍 Search Memories",
        placeholder="Search by memory or category..."
    )

    # --------------------------------------------------
    # FILTERS
    # --------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        category_filter = st.selectbox(
            "🏷️ Category Filter",
            ["All"] + CATEGORIES
        )

    with col2:

        view_filter = st.selectbox(
            "🕐 View",
            [
                "All Memories",
                "Recent Memories"
            ]
        )

    # --------------------------------------------------
    # LOAD MEMORIES
    # --------------------------------------------------

    
    if search_text.strip():

        if search_mode == "Intelligent Search":

            memories = find_relevant_memories(
                search_text
            )

        else:

            memories = search_memories(
                search_text
            )

    elif category_filter != "All":

        memories = get_memories_by_category(
            category_filter
        )

    elif view_filter == "Recent Memories":

        memories = get_recent_memories()

    else:

        memories = get_memories()

    # --------------------------------------------------
    # APPLY CATEGORY FILTER AFTER SEARCH
    # --------------------------------------------------

    if (
        search_text.strip()
        and category_filter != "All"
    ):

        memories = [
            memory
            for memory in memories
            if memory["category"] == category_filter
        ]

    # --------------------------------------------------
    # APPLY RECENT FILTER AFTER SEARCH
    # --------------------------------------------------

    if (
        search_text.strip()
        and view_filter == "Recent Memories"
    ):

        recent_ids = {
            memory["id"]
            for memory in get_recent_memories()
        }

        memories = [
            memory
            for memory in memories
            if memory["id"] in recent_ids
        ]

    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    st.caption(
        f"{len(memories)} memory/memories found"
    )

    if not memories:

        if search_text.strip():

            st.info(
                "No memories found for the selected search and filters."
            )

        else:

            st.info(
                "No memories found for the selected filters."
            )

        return

    for memory in memories:

        show_memory_card(memory)


# ======================================================
# MEMORY CARD
# ======================================================

def show_memory_card(memory):

    with st.container(border=True):

        st.markdown(
            f"### 🧠 {memory['content']}"
        )

        st.write(
            f"🏷️ **Category:** {memory['category']}"
        )

        try:
            created_time = datetime.fromisoformat(
                memory["created_at"]
            )

            created_time = created_time.replace(
                tzinfo=timezone.utc
            ).astimezone(
                timezone(
                    timedelta(
                        hours=5,
                        minutes=30
                    )
                )
            )

            st.caption(
                f"🕐 Created: {created_time.strftime('%d %b %Y, %I:%M %p')}"
            )

        except (ValueError, TypeError):
            st.caption(
                f"🕐 Created: {memory['created_at']}"
            )

        col1, col2 = st.columns(2)
    
        # --------------------------------------------------
        # RELEVANCE INFORMATION
        # --------------------------------------------------

        if "relevance_score" in memory:

            score = memory["relevance_score"]

            matching_terms = memory.get(
                "matching_terms",
                []
            )

            st.info(
                f"🎯 Relevance: {score} matching term(s)"
            )

            if matching_terms:

                st.caption(
                    "Matching terms: "
                    + ", ".join(matching_terms)
                )


        # --------------------------------------------------
        # EDIT
        # --------------------------------------------------

        with col1:

            if st.button(
                "✏️ Edit",
                key=f"edit_memory_{memory['id']}"
            ):

                st.session_state[
                    "editing_memory"
                ] = memory["id"]

                st.rerun()

        # --------------------------------------------------
        # DELETE
        # --------------------------------------------------

        with col2:

            if st.button(
                "🗑️ Delete",
                key=f"delete_memory_{memory['id']}"
            ):

                delete_memory(
                    memory["id"]
                )

                st.success(
                    "Memory deleted successfully!"
                )

                st.rerun()

        # --------------------------------------------------
        # EDIT FORM
        # --------------------------------------------------

        if st.session_state.get(
            "editing_memory"
        ) == memory["id"]:

            show_edit_memory(memory)


# ======================================================
# EDIT MEMORY
# ======================================================

def show_edit_memory(memory):

    st.markdown(
        "#### ✏️ Edit Memory"
    )

    current_category = memory["category"]

    if current_category in CATEGORIES:

        category_index = CATEGORIES.index(
            current_category
        )

    else:

        category_index = 0

    with st.form(
        f"edit_memory_form_{memory['id']}"
    ):

        content = st.text_area(
            "Memory",
            value=memory["content"]
        )

        category = st.selectbox(
            "Category",
            CATEGORIES,
            index=category_index
        )

        col1, col2 = st.columns(2)

        with col1:

            save = st.form_submit_button(
                "💾 Save Changes"
            )

        with col2:

            cancel = st.form_submit_button(
                "❌ Cancel"
            )

        if save:

            if content.strip() == "":

                st.warning(
                    "Memory cannot be empty."
                )

                return

            update_memory(
                memory["id"],
                content,
                category
            )

            st.session_state.pop(
                "editing_memory",
                None
            )

            st.success(
                "Memory updated successfully!"
            )

            st.rerun()

        if cancel:

            st.session_state.pop(
                "editing_memory",
                None
            )

            st.rerun()