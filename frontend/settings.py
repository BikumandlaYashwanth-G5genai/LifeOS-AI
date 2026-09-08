import streamlit as st

from backend.goal_service import (
    get_dashboard_statistics
)

from backend.knowledge_service import (
    get_knowledge_statistics
)


# =====================================================
# HEADER
# =====================================================

def show_header():

    st.title("⚙️ Settings")

    st.markdown(
        "Manage your LifeOS preferences, review your "
        "system information, and control your experience."
    )

    st.divider()


# =====================================================
# PROFILE SETTINGS
# =====================================================

def show_profile_settings():

    st.subheader("👤 Profile")

    name = st.text_input(
        "Your Name",
        value=st.session_state.get(
            "lifeos_name",
            ""
        ),
        placeholder="Enter your name",
        key="settings_name"
    )

    description = st.text_area(
        "About You",
        value=st.session_state.get(
            "lifeos_description",
            ""
        ),
        placeholder=(
            "Write a short description about yourself..."
        ),
        height=100,
        key="settings_description"
    )

    if st.button(
        "💾 Save Profile",
        type="primary",
        use_container_width=True
    ):

        st.session_state[
            "lifeos_name"
        ] = name.strip()

        st.session_state[
            "lifeos_description"
        ] = description.strip()

        st.success(
            "✅ Profile settings saved."
        )


# =====================================================
# AI SETTINGS
# =====================================================

def show_ai_settings():

    st.subheader("🤖 AI Assistant")

    ai_enabled = st.toggle(
        "Enable LifeOS AI Assistant",
        value=st.session_state.get(
            "ai_enabled",
            True
        ),
        key="settings_ai_enabled"
    )

    st.session_state[
        "ai_enabled"
    ] = ai_enabled

    st.caption(
        "When enabled, the LifeOS AI Assistant can "
        "use relevant goals and memories to answer questions."
    )

    st.info(
        "🧠 LifeOS AI uses your stored LifeOS context "
        "when it is relevant to your question."
    )


# =====================================================
# NOTIFICATION SETTINGS
# =====================================================

def show_notification_settings():

    st.subheader("🔔 Notifications")

    deadline_alerts = st.toggle(
        "⏰ Deadline Alerts",
        value=st.session_state.get(
            "deadline_alerts",
            True
        ),
        key="settings_deadline_alerts"
    )

    overdue_alerts = st.toggle(
        "🚨 Overdue Goal Alerts",
        value=st.session_state.get(
            "overdue_alerts",
            True
        ),
        key="settings_overdue_alerts"
    )

    priority_alerts = st.toggle(
        "🔥 High Priority Goal Alerts",
        value=st.session_state.get(
            "priority_alerts",
            True
        ),
        key="settings_priority_alerts"
    )

    st.session_state[
        "deadline_alerts"
    ] = deadline_alerts

    st.session_state[
        "overdue_alerts"
    ] = overdue_alerts

    st.session_state[
        "priority_alerts"
    ] = priority_alerts


# =====================================================
# APPEARANCE SETTINGS
# =====================================================

def show_appearance_settings():

    st.subheader("🎨 Appearance")

    layout = st.radio(
        "Interface Layout",
        [
            "Comfortable",
            "Compact"
        ],
        index=0 if st.session_state.get(
            "layout",
            "Comfortable"
        ) == "Comfortable" else 1,
        key="settings_layout"
    )

    st.session_state[
        "layout"
    ] = layout

    st.caption(
        "This preference can be used for future "
        "interface customization."
    )


# =====================================================
# SYSTEM INFORMATION
# =====================================================

def show_system_information():

    st.subheader("ℹ️ LifeOS Information")

    try:

        goal_stats = get_dashboard_statistics()

        total_goals = goal_stats.get(
            "total",
            0
        )

    except Exception:

        total_goals = 0

    try:

        knowledge_stats = get_knowledge_statistics()

        total_knowledge = knowledge_stats.get(
            "total",
            0
        )

    except Exception:

        total_knowledge = 0

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🎯 Goals",
            total_goals
        )

    with col2:

        st.metric(
            "📚 Knowledge",
            total_knowledge
        )

    with col3:

        st.metric(
            "🚀 Version",
            "1.0"
        )

    st.caption(
        "LifeOS — Personal AI-powered life management system."
    )


# =====================================================
# DATA MANAGEMENT
# =====================================================

def show_data_management():

    st.subheader("💾 Data Management")

    st.info(
        "Your LifeOS data is stored locally in the "
        "application database."
    )

    st.warning(
        "⚠️ Be careful when performing destructive "
        "data operations."
    )

    if st.button(
        "🔄 Reset Session Preferences",
        use_container_width=True
    ):

        preference_keys = [
            "lifeos_name",
            "lifeos_description",
            "ai_enabled",
            "deadline_alerts",
            "overdue_alerts",
            "priority_alerts",
            "layout"
        ]

        for key in preference_keys:

            st.session_state.pop(
                key,
                None
            )

        st.success(
            "✅ Session preferences reset."
        )

        st.rerun()


# =====================================================
# MAIN SETTINGS PAGE
# =====================================================

def settings_page():

    show_header()

    # -------------------------------------------------
    # PROFILE
    # -------------------------------------------------

    show_profile_settings()

    st.divider()

    # -------------------------------------------------
    # AI
    # -------------------------------------------------

    show_ai_settings()

    st.divider()

    # -------------------------------------------------
    # NOTIFICATIONS
    # -------------------------------------------------

    show_notification_settings()

    st.divider()

    # -------------------------------------------------
    # APPEARANCE
    # -------------------------------------------------

    show_appearance_settings()

    st.divider()

    # -------------------------------------------------
    # SYSTEM INFORMATION
    # -------------------------------------------------

    show_system_information()

    st.divider()

    # -------------------------------------------------
    # DATA MANAGEMENT
    # -------------------------------------------------

    show_data_management()