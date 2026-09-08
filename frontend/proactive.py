import streamlit as st

from backend.proactive_service import (
    get_daily_briefing
)


# ======================================================
# PAGE HEADER
# ======================================================

def show_header():

    st.title("🚀 LifeOS Proactive")

    st.markdown(
        "LifeOS automatically identifies important "
        "goals, deadlines, and items that need your attention."
    )

    st.divider()


# ======================================================
# DAILY SUMMARY
# ======================================================

def show_summary(briefing):

    statistics = briefing.get(
        "statistics",
        {}
    )

    st.subheader("📊 Today's Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Goals",
            statistics.get("total", 0)
        )

    with col2:

        st.metric(
            "Completed",
            statistics.get("completed", 0)
        )

    with col3:

        st.metric(
            "Pending",
            statistics.get("pending", 0)
        )

    with col4:

        st.metric(
            "High Priority",
            statistics.get("high_priority", 0)
        )


# ======================================================
# PROACTIVE INSIGHTS
# ======================================================

def show_insights(briefing):

    st.subheader("🧠 LifeOS Insights")

    insights = briefing.get(
        "insights",
        []
    )

    if not insights:

        st.success(
            "🎉 Nothing requires your immediate attention."
        )

        return

    for insight in insights:

        priority = insight.get(
            "priority",
            "low"
        )

        title = insight.get(
            "title",
            "Insight"
        )

        message = insight.get(
            "message",
            ""
        )

        if priority == "critical":

            st.error(
                f"🚨 **{title}**\n\n{message}"
            )

        elif priority == "high":

            st.warning(
                f"⚠️ **{title}**\n\n{message}"
            )

        elif priority == "medium":

            st.info(
                f"💡 **{title}**\n\n{message}"
            )

        else:

            st.success(
                f"✅ **{title}**\n\n{message}"
            )


# ======================================================
# OVERDUE GOALS
# ======================================================

def show_overdue_goals(briefing):

    overdue = briefing.get(
        "overdue",
        []
    )

    st.subheader("🚨 Overdue Goals")

    if not overdue:

        st.success(
            "No overdue goals."
        )

        return

    for goal in overdue:

        with st.container(border=True):

            st.markdown(
                f"### {goal.get('title', '')}"
            )

            st.write(
                f"**Priority:** "
                f"{goal.get('priority', '')}"
            )

            st.write(
                f"**Category:** "
                f"{goal.get('category', '')}"
            )

            st.write(
                f"**Deadline:** "
                f"{goal.get('deadline', '')}"
            )

            st.error(
                f"Overdue by "
                f"{goal.get('days_overdue', 0)} day(s)"
            )


# ======================================================
# UPCOMING DEADLINES
# ======================================================

def show_upcoming_deadlines(briefing):

    approaching = briefing.get(
        "approaching",
        []
    )

    st.subheader("📅 Upcoming Deadlines")

    if not approaching:

        st.info(
            "No deadlines within the next 7 days."
        )

        return

    for goal in approaching:

        days = goal.get(
            "days_remaining",
            0
        )

        if days == 0:

            deadline_text = "Due today"

        elif days == 1:

            deadline_text = "Due tomorrow"

        else:

            deadline_text = (
                f"Due in {days} days"
            )

        with st.container(border=True):

            st.markdown(
                f"### {goal.get('title', '')}"
            )

            st.write(
                f"**Deadline:** "
                f"{goal.get('deadline', '')}"
            )

            st.write(
                f"**Priority:** "
                f"{goal.get('priority', '')}"
            )

            st.warning(
                deadline_text
            )


# ======================================================
# HIGH PRIORITY GOALS
# ======================================================

def show_high_priority(briefing):

    goals = briefing.get(
        "high_priority",
        []
    )

    st.subheader("🔥 High Priority Goals")

    if not goals:

        st.info(
            "No pending high-priority goals."
        )

        return

    for goal in goals:

        with st.container(border=True):

            st.markdown(
                f"### {goal.get('title', '')}"
            )

            st.write(
                f"**Status:** "
                f"{goal.get('status', '')}"
            )

            st.write(
                f"**Category:** "
                f"{goal.get('category', '')}"
            )

            st.write(
                f"**Deadline:** "
                f"{goal.get('deadline', '')}"
            )


# ======================================================
# MAIN PROACTIVE PAGE
# ======================================================

def proactive_page():

    show_header()

    # --------------------------------------------------
    # LOAD DAILY BRIEFING
    # --------------------------------------------------

    with st.spinner(
        "🧠 Analyzing your LifeOS..."
    ):

        briefing = get_daily_briefing()

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    show_summary(
        briefing
    )

    st.divider()

    # --------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------

    show_insights(
        briefing
    )

    st.divider()

    # --------------------------------------------------
    # OVERDUE
    # --------------------------------------------------

    show_overdue_goals(
        briefing
    )

    st.divider()

    # --------------------------------------------------
    # UPCOMING
    # --------------------------------------------------

    show_upcoming_deadlines(
        briefing
    )

    st.divider()

    # --------------------------------------------------
    # HIGH PRIORITY
    # --------------------------------------------------

    show_high_priority(
        briefing
    )

    st.divider()

    st.caption(
        f"LifeOS briefing generated for "
        f"{briefing.get('date', '')}"
    )