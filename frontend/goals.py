import streamlit as st
from datetime import datetime

from backend.goal_service import (
    add_goal,
    get_goals,
    delete_goal,
    complete_goal,
    update_goal,
    mark_goal_pending
)

from backend.goal_ai_service import (
    analyze_goals,
    analyze_goal,
    get_goal_recommendation
)


# ======================================================
# GOAL STATISTICS
# ======================================================

def show_statistics(goals):
    """Display goal statistics."""

    total_goals = len(goals)

    completed_goals = sum(
        1
        for goal in goals
        if goal["status"] == "Completed"
    )

    pending_goals = total_goals - completed_goals

    completion_rate = 0

    if total_goals > 0:
        completion_rate = round(
            (completed_goals / total_goals) * 100
        )

    st.subheader("📊 Goal Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Goals", total_goals)

    with col2:
        st.metric("Completed", completed_goals)

    with col3:
        st.metric("Pending", pending_goals)

    with col4:
        st.metric(
            "Completion",
            f"{completion_rate}%"
        )

    st.divider()


# ======================================================
# SEARCH & FILTERS
# ======================================================

def show_search_filters(goals):
    """Search and filter goals."""

    st.subheader("🔍 Search & Filters")

    search_text = st.text_input(
        "Search Goal",
        placeholder="Search by title...",
        key="goal_search"
    )

    categories = sorted(
        list(
            set(
                goal["category"]
                for goal in goals
                if goal["category"]
            )
        )
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        category_filter = st.selectbox(
            "Category",
            ["All"] + categories,
            key="goal_category_filter"
        )

    with col2:

        priority_filter = st.selectbox(
            "Priority",
            [
                "All",
                "High",
                "Medium",
                "Low"
            ],
            key="goal_priority_filter"
        )

    with col3:

        status_filter = st.selectbox(
            "Status",
            [
                "All",
                "Pending",
                "Completed"
            ],
            key="goal_status_filter"
        )

    filtered_goals = goals

    # -----------------------------
    # Search
    # -----------------------------

    if search_text:

        filtered_goals = [

            goal

            for goal in filtered_goals

            if search_text.lower()
            in goal["title"].lower()

        ]

    # -----------------------------
    # Category
    # -----------------------------

    if category_filter != "All":

        filtered_goals = [

            goal

            for goal in filtered_goals

            if goal["category"] == category_filter

        ]

    # -----------------------------
    # Priority
    # -----------------------------

    if priority_filter != "All":

        filtered_goals = [

            goal

            for goal in filtered_goals

            if goal["priority"] == priority_filter

        ]

    # -----------------------------
    # Status
    # -----------------------------

    if status_filter != "All":

        filtered_goals = [

            goal

            for goal in filtered_goals

            if goal["status"] == status_filter

        ]

    st.divider()

    return filtered_goals


# ======================================================
# ADD GOAL FORM
# ======================================================

def show_add_goal_form():
    """Display Add Goal form."""

    st.subheader("➕ Add New Goal")

    with st.form(
        "add_goal_form",
        clear_on_submit=True
    ):

        title = st.text_input(
            "Title",
            key="new_goal_title"
        )

        description = st.text_area(
            "Description",
            key="new_goal_description"
        )

        category = st.selectbox(
            "Category",
            [
                "Personal",
                "Study",
                "Internship",
                "Work",
                "Health",
                "Finance",
                "Other"
            ],
            key="new_goal_category"
        )

        priority = st.selectbox(
            "Priority",
            [
                "High",
                "Medium",
                "Low"
            ],
            key="new_goal_priority"
        )

        deadline = st.date_input(
            "Deadline",
            key="new_goal_deadline"
        )

        submitted = st.form_submit_button(
            "💾 Save Goal"
        )

        if submitted:

            if title.strip() == "":

                st.warning(
                    "Please enter a goal title."
                )

                return

            add_goal(
                title,
                description,
                category,
                priority,
                str(deadline)
            )

            st.success(
                "Goal added successfully!"
            )

            st.rerun()


# ======================================================
# ADD GOAL DIALOG
# ======================================================

@st.dialog("➕ Create New Goal")
def show_add_goal_dialog():

    st.write(
        "Create a new goal and start tracking your progress."
    )

    with st.form(
        "dialog_add_goal_form",
        clear_on_submit=True
    ):

        title = st.text_input(
            "Title",
            key="dialog_goal_title"
        )

        description = st.text_area(
            "Description",
            key="dialog_goal_description"
        )

        category = st.selectbox(
            "Category",
            [
                "Personal",
                "Study",
                "Internship",
                "Work",
                "Health",
                "Finance",
                "Other"
            ],
            key="dialog_goal_category"
        )

        priority = st.selectbox(
            "Priority",
            [
                "High",
                "Medium",
                "Low"
            ],
            key="dialog_goal_priority"
        )

        deadline = st.date_input(
            "Deadline",
            key="dialog_goal_deadline"
        )

        submitted = st.form_submit_button(
            "💾 Save Goal"
        )

        if submitted:

            if title.strip() == "":

                st.warning(
                    "Please enter a goal title."
                )

            else:

                add_goal(
                    title,
                    description,
                    category,
                    priority,
                    str(deadline)
                )

                st.success(
                    "Goal added successfully!"
                )

                st.rerun()


# ======================================================
# SMART GOAL INTELLIGENCE
# ======================================================

def show_smart_goal_intelligence(goals):
    """
    Display AI-powered goal intelligence.

    Phase 7A:
    - Analyze all goals
    - Generate focus recommendation
    - Analyze individual goal
    """

    st.subheader("🧠 Smart Goal Intelligence")

    st.markdown(
        "Use Gemini to analyze your goals and get "
        "personalized recommendations."
    )

    if not goals:

        st.info(
            "Add at least one goal to use Smart Goal Intelligence."
        )

        return

    # ==================================================
    # AI ACTION BUTTONS
    # ==================================================

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "🔍 Analyze My Goals",
            use_container_width=True,
            key="ai_analyze_all_goals"
        ):

            with st.spinner(
                "Analyzing your goals..."
            ):

                result = analyze_goals()

            st.session_state[
                "goal_ai_analysis"
            ] = result

    with col2:

        if st.button(
            "💡 What Should I Focus On?",
            use_container_width=True,
            key="ai_goal_recommendation"
        ):

            with st.spinner(
                "Finding your best next focus..."
            ):

                result = get_goal_recommendation()

            st.session_state[
                "goal_ai_recommendation"
            ] = result

    # ==================================================
    # SHOW GENERAL ANALYSIS
    # ==================================================

    if st.session_state.get(
        "goal_ai_analysis"
    ):

        st.markdown("### 🔍 Goal Analysis")

        with st.container(border=True):

            st.markdown(
                st.session_state[
                    "goal_ai_analysis"
                ]
            )

    # ==================================================
    # SHOW RECOMMENDATION
    # ==================================================

    if st.session_state.get(
        "goal_ai_recommendation"
    ):

        st.markdown("### 💡 Recommended Focus")

        with st.container(border=True):

            st.markdown(
                st.session_state[
                    "goal_ai_recommendation"
                ]
            )

    st.divider()

    # ==================================================
    # INDIVIDUAL GOAL ANALYSIS
    # ==================================================

    st.markdown(
        "### 🎯 Analyze Individual Goal"
    )

    goal_options = {
        f"{goal['title']} "
        f"({goal['status']})": goal["id"]
        for goal in goals
    }

    selected_goal_label = st.selectbox(
        "Select a goal",
        list(goal_options.keys()),
        key="ai_selected_goal"
    )

    selected_goal_id = goal_options[
        selected_goal_label
    ]

    if st.button(
        "🤖 Analyze Selected Goal",
        use_container_width=True,
        key="ai_analyze_selected_goal"
    ):

        with st.spinner(
            "Analyzing selected goal..."
        ):

            result = analyze_goal(
                selected_goal_id
            )

        st.session_state[
            "individual_goal_analysis"
        ] = result

        st.session_state[
            "individual_goal_analysis_id"
        ] = selected_goal_id

    # ==================================================
    # SHOW INDIVIDUAL ANALYSIS
    # ==================================================

    if st.session_state.get(
        "individual_goal_analysis"
    ):

        st.markdown(
            "### 🤖 Individual Goal Analysis"
        )

        with st.container(border=True):

            st.markdown(
                st.session_state[
                    "individual_goal_analysis"
                ]
            )

    st.divider()


# ======================================================
# GOAL CARD
# ======================================================

def show_goal_card(goal):
    """Display a single goal."""

    with st.container(border=True):

        st.markdown(
            f"### 🎯 {goal['title']}"
        )

        if goal["description"]:

            st.write(
                goal["description"]
            )

        st.write(
            f"**📂 Category:** {goal['category']}"
        )

        st.write(
            f"**🚩 Priority:** {goal['priority']}"
        )

        st.write(
            f"**📅 Deadline:** {goal['deadline']}"
        )

        if goal["status"] == "Completed":

            st.success(
                "✅ Completed"
            )

        else:

            st.warning(
                "🟡 Pending"
            )

        col1, col2, col3 = st.columns(3)

        # -----------------------------
        # Complete / Mark Pending
        # -----------------------------

        with col1:

            if goal["status"] == "Pending":

                if st.button(
                    "✔ Complete",
                    key=f"complete_{goal['id']}"
                ):

                    complete_goal(
                        goal["id"]
                    )

                    st.rerun()

            else:

                if st.button(
                    "↩ Mark Pending",
                    key=f"pending_{goal['id']}"
                ):

                    mark_goal_pending(
                        goal["id"]
                    )

                    st.rerun()

        # -----------------------------
        # Edit
        # -----------------------------

        with col2:

            if st.button(
                "✏ Edit",
                key=f"edit_{goal['id']}"
            ):

                st.session_state[
                    "editing_goal"
                ] = goal["id"]

                st.rerun()

        # -----------------------------
        # Delete
        # -----------------------------

        with col3:

            if st.button(
                "🗑 Delete",
                key=f"delete_{goal['id']}"
            ):

                delete_goal(
                    goal["id"]
                )

                st.rerun()

        st.divider()


# ======================================================
# EDIT GOAL FORM
# ======================================================

def show_edit_form(goal):
    """Display Edit Goal form."""

    st.info(
        "✏ Edit Goal"
    )

    categories = [
        "Personal",
        "Study",
        "Internship",
        "Work",
        "Health",
        "Finance",
        "Other"
    ]

    priorities = [
        "High",
        "Medium",
        "Low"
    ]

    with st.form(
        f"edit_goal_{goal['id']}"
    ):

        title = st.text_input(
            "Title",
            value=goal["title"],
            key=f"edit_title_{goal['id']}"
        )

        description = st.text_area(
            "Description",
            value=goal["description"],
            key=f"edit_description_{goal['id']}"
        )

        category = st.selectbox(
            "Category",
            categories,
            index=categories.index(
                goal["category"]
            ),
            key=f"edit_category_{goal['id']}"
        )

        priority = st.selectbox(
            "Priority",
            priorities,
            index=priorities.index(
                goal["priority"]
            ),
            key=f"edit_priority_{goal['id']}"
        )

        deadline = st.date_input(
            "Deadline",
            value=datetime.strptime(
                goal["deadline"],
                "%Y-%m-%d"
            ).date(),
            key=f"edit_deadline_{goal['id']}"
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

            if title.strip() == "":

                st.warning(
                    "Title cannot be empty."
                )

                return

            update_goal(
                goal["id"],
                title,
                description,
                category,
                priority,
                str(deadline)
            )

            st.session_state.pop(
                "editing_goal",
                None
            )

            st.success(
                "Goal updated successfully!"
            )

            st.rerun()

        if cancel:

            st.session_state.pop(
                "editing_goal",
                None
            )

            st.rerun()


# ======================================================
# MAIN GOALS PAGE
# ======================================================

def goals_page():
    """Main Goal Manager page."""

    st.title(
        "🎯 Goal Manager"
    )

    # ==================================================
    # DASHBOARD ADD GOAL REQUEST
    # ==================================================

    if st.session_state.pop(
        "open_add_goal",
        False
    ):

        show_add_goal_dialog()

    # ==================================================
    # LOAD GOALS
    # ==================================================

    goals = get_goals()

    # ==================================================
    # STATISTICS
    # ==================================================

    show_statistics(
        goals
    )

    # ==================================================
    # SEARCH & FILTERS
    # ==================================================

    filtered_goals = show_search_filters(
        goals
    )

    # ==================================================
    # ADD GOAL BUTTON
    # ==================================================

    if st.button(
        "➕ Add New Goal",
        use_container_width=True,
        key="goals_page_add_goal"
    ):

        show_add_goal_dialog()

    st.divider()

    # ==================================================
    # SMART GOAL INTELLIGENCE
    # ==================================================

    show_smart_goal_intelligence(
        goals
    )

    # ==================================================
    # NO GOALS
    # ==================================================

    if not filtered_goals:

        st.info(
            "No goals found. Add your first goal!"
        )

        return

    # ==================================================
    # DISPLAY GOALS
    # ==================================================

    for goal in filtered_goals:

        show_goal_card(
            goal
        )

        if (
            st.session_state.get(
                "editing_goal"
            )
            == goal["id"]
        ):

            show_edit_form(
                goal
            )