import streamlit as st

from backend.database import initialize_database

from frontend.sidebar import sidebar
from frontend.dashboard import dashboard
from frontend.goals import goals_page

initialize_database()

page = sidebar()

if page == "Dashboard":
    dashboard()

elif page == "Goals":
    goals_page()

elif page == "Memory":
    st.title("Memory Engine")
    st.info("Coming Soon")

elif page == "Planner":
    st.title("Planner")
    st.info("Coming Soon")

elif page == "Knowledge Vault":
    st.title("Knowledge Vault")
    st.info("Coming Soon")

elif page == "Settings":
    st.title("Settings")
    st.info("Coming Soon")