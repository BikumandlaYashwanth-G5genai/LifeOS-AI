import streamlit as st


def sidebar():

    st.sidebar.title("🧠 LifeOS AI")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Goals",
            "Memory",
            "Planner",
            "Knowledge Vault",
            "Settings"
        ]
    )

    return page