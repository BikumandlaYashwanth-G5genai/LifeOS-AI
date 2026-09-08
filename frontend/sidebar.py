import streamlit as st


def sidebar():

    st.sidebar.title("🧠 LifeOS AI")

    pages = [
        "Dashboard",
        "Goals",
        "Memory",
        "Planner",
        "Knowledge Vault",
        "LifeOS Context",
        "AI Assistant",
        "Settings"
    ]

    requested_page = st.session_state.pop(
        "requested_page",
        None
    )

    if requested_page in pages:

        st.session_state[
            "main_navigation"
        ] = requested_page

    page = st.sidebar.radio(
        "Navigation",
        pages,
        key="main_navigation"
    )

    return page