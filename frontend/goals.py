import streamlit as st
from datetime import datetime

from backend.goal_service import (
    add_goal,
    get_goals,
    delete_goal,
    complete_goal,
    update_goal
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
        st.metric("Completion", f"{completion_rate}%")

    st.divider()


# ======================================================
# SEARCH & FILTERS
# ======================================================

def show_search_filters(goals):
    """Search and filter goals."""

    st.subheader("🔍 Search & Filters")

    search_text = st.text_input(
        "Search Goal",
        placeholder="Search by title..."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        categories = sorted(
            list(
                set(
                    goal["category"]
                    for goal in goals
                    if goal["category"]
                )
            )
        )

        category_filter = st.selectbox(
            "Category",
            ["All"] + categories
        )

    with col2:

        priority_filter = st.selectbox(
            "Priority",
            [
                "All",
                "High",
                "Medium",
                "Low"
            ]
        )

    with col3:

        status_filter = st.selectbox(
            "Status",
            [
                "All",
                "Pending",
                "Completed"
            ]
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

        title = st.text_input("Title")

        description = st.text_area("Description")

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
            ]

        )

        priority = st.selectbox(

            "Priority",

            [
                "High",
                "Medium",
                "Low"
            ]

        )

        deadline = st.date_input("Deadline")

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
# GOAL CARD
# ======================================================

def show_goal_card(goal):
    """Display a single goal."""

    with st.container():

        st.markdown(f"### 🎯 {goal['title']}")

        if goal["description"]:
            st.write(goal["description"])

        st.write(f"**📂 Category:** {goal['category']}")
        st.write(f"**🚩 Priority:** {goal['priority']}")
        st.write(f"**📅 Deadline:** {goal['deadline']}")

        if goal["status"] == "Completed":
            st.success("✅ Completed")
        else:
            st.warning("🟡 Pending")

        handle_goal_actions(goal)

        st.divider()


# ======================================================
# GOAL ACTIONS
# ======================================================

def handle_goal_actions(goal):
    """Display action buttons for a goal."""

    col1, col2, col3 = st.columns(3)

    # -----------------------------
    # Complete
    # -----------------------------
    with col1:

        if goal["status"] == "Pending":

            if st.button(
                "✔ Complete",
                key=f"complete_{goal['id']}"
            ):

                complete_goal(goal["id"])

                st.success("Goal marked as completed.")

                st.rerun()

    # -----------------------------
    # Edit
    # -----------------------------
    with col2:

        if st.button(
            "✏ Edit",
            key=f"edit_{goal['id']}"
        ):

            st.session_state["editing_goal"] = goal["id"]

            st.rerun()

    # -----------------------------
    # Delete
    # -----------------------------
    with col3:

        if st.button(
            "🗑 Delete",
            key=f"delete_{goal['id']}"
        ):

            delete_goal(goal["id"])

            st.success("Goal deleted successfully.")

            st.rerun()
            # ======================================================
# EDIT GOAL FORM
# ======================================================

def show_edit_form(goal):
    """Display the Edit Goal form."""

    st.info("✏ Edit Goal")

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

    with st.form(f"edit_goal_{goal['id']}"):

        title = st.text_input(
            "Title",
            value=goal["title"]
        )

        description = st.text_area(
            "Description",
            value=goal["description"]
        )

        category = st.selectbox(
            "Category",
            categories,
            index=categories.index(goal["category"])
        )

        priority = st.selectbox(
            "Priority",
            priorities,
            index=priorities.index(goal["priority"])
        )

        deadline = st.date_input(
            "Deadline",
            value=datetime.strptime(
                goal["deadline"],
                "%Y-%m-%d"
            ).date()
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
                st.warning("Title cannot be empty.")
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

    st.title("🎯 Goal Manager")

    # -----------------------------
    # Load Goals
    # -----------------------------
    goals = get_goals()

    # -----------------------------
    # Statistics
    # -----------------------------
    show_statistics(goals)

    # -----------------------------
    # Search & Filters
    # -----------------------------
    filtered_goals = show_search_filters(goals)

    # -----------------------------
    # Add Goal
    # -----------------------------
    show_add_goal_form()

    st.divider()

    # -----------------------------
    # No Goals
    # -----------------------------
    if not filtered_goals:

        st.info(
            "No goals found. Add your first goal!"
        )

        return

    # -----------------------------
    # Display Goals
    # -----------------------------
    for goal in filtered_goals:

        show_goal_card(goal)

        if (
            st.session_state.get("editing_goal")
            == goal["id"]
        ):

            show_edit_form(goal)
