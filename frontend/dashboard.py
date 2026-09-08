import streamlit as st
from datetime import datetime

from backend.goal_service import (
    get_dashboard_statistics,
    get_upcoming_deadlines,
    get_high_priority_goals,
    get_completion_percentage
)


# =====================================================
# WELCOME SECTION
# =====================================================

def show_welcome():

    st.title("🏠 Dashboard")

    st.markdown("### Welcome Back!")

    st.info(
        "Track your goals, monitor your progress, "
        "and stay focused on what matters most."
    )


# =====================================================
# STATISTICS
# =====================================================

def show_statistics():

    stats = get_dashboard_statistics()

    completion = get_completion_percentage()

    st.subheader("📊 Goal Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Goals",
            stats["total"]
        )

    with col2:
        st.metric(
            "Completed",
            stats["completed"]
        )

    with col3:
        st.metric(
            "Pending",
            stats["pending"]
        )

    with col4:
        st.metric(
            "High Priority",
            stats["high_priority"]
        )

    st.markdown("### 🎯 Goal Completion")

    st.progress(
        completion / 100
    )

    st.caption(
        f"Completion Rate : {completion}%"
    )


# =====================================================
# UPCOMING DEADLINES
# =====================================================

def show_upcoming_deadlines():

    goals = get_upcoming_deadlines()

    st.subheader(
        "⏰ Upcoming Deadlines"
    )

    if not goals:

        st.info(
            "No upcoming deadlines."
        )

        return

    today = datetime.today().date()

    for goal in goals:

        deadline = datetime.strptime(
            goal["deadline"],
            "%Y-%m-%d"
        ).date()

        days_left = (
            deadline - today
        ).days

        with st.container(
            border=True
        ):

            st.markdown(
                f"### {goal['title']}"
            )

            st.write(
                f"📂 Category : {goal['category']}"
            )

            st.write(
                f"📅 Deadline : {goal['deadline']}"
            )

            if days_left > 1:

                st.success(
                    f"⏳ {days_left} days remaining"
                )

            elif days_left == 1:

                st.warning(
                    "⚠ 1 day remaining"
                )

            elif days_left == 0:

                st.error(
                    "🚨 Due Today"
                )

            else:

                st.error(
                    f"❌ Overdue by "
                    f"{abs(days_left)} day(s)"
                )


# =====================================================
# HIGH PRIORITY GOALS
# =====================================================

def show_high_priority_goals():

    goals = get_high_priority_goals()

    st.subheader(
        "🔥 High Priority Goals"
    )

    if not goals:

        st.success(
            "No high priority goals."
        )

        return

    for goal in goals:

        with st.container(
            border=True
        ):

            st.markdown(
                f"### {goal['title']}"
            )

            st.write(
                f"📅 Deadline : "
                f"**{goal['deadline']}**"
            )

            st.write(
                f"📂 Category : "
                f"{goal['category']}"
            )


# =====================================================
# ACHIEVEMENT
# =====================================================

def show_achievement():

    stats = get_dashboard_statistics()

    completed = stats["completed"]

    st.subheader(
        "🏆 Achievement"
    )

    if completed == 0:

        st.info(
            "🌱 Start your journey by "
            "completing your first goal!"
        )

    elif completed < 5:

        st.success(
            f"🎉 Great Start! You've completed "
            f"{completed} goal(s)."
        )

    elif completed < 10:

        st.success(
            f"🚀 Awesome! You've completed "
            f"{completed} goals."
        )

    else:

        st.success(
            f"🏅 Outstanding! {completed} goals "
            f"completed. Keep it up!"
        )


# =====================================================
# MOTIVATION
# =====================================================

def show_motivation():

    completion = get_completion_percentage()

    st.subheader(
        "💬 Motivation"
    )

    if completion < 25:

        st.info(
            "Every great achievement starts "
            "with a single step."
        )

    elif completion < 50:

        st.info(
            "You're building consistency. "
            "Keep going!"
        )

    elif completion < 75:

        st.success(
            "Fantastic progress! Success comes "
            "from consistency."
        )

    else:

        st.success(
            "Outstanding! You're crushing your goals. "
            "Keep the momentum alive!"
        )


# =====================================================
# QUICK ACTIONS
# =====================================================

def show_quick_actions():

    st.subheader(
        "⚡ Quick Actions"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "➕ Add New Goal",
            use_container_width=True
        ):

            st.session_state[
                "requested_page"
            ] = "Goals"

            st.session_state[
                "open_add_goal"
            ] = True

            st.rerun()

    with col2:

        if st.button(
            "📋 View Goals",
            use_container_width=True
        ):

            st.session_state[
                "requested_page"
            ] = "Goals"

            st.rerun()


# =====================================================
# DASHBOARD
# =====================================================

def dashboard():

    show_welcome()

    st.divider()

    show_statistics()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        show_upcoming_deadlines()

    with col2:
        show_high_priority_goals()

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        show_achievement()

    with col4:
        show_motivation()

    st.divider()

    show_quick_actions()