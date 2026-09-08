import streamlit as st

from frontend.sidebar import sidebar
from frontend.dashboard import dashboard

from backend.database import initialize_database

st.set_page_config(
    page_title="LifeOS AI",
    page_icon="🧠",
    layout="wide"
)

initialize_database()

page = sidebar()

if page == "Dashboard":
    dashboard()

elif page == "Goals":
    st.title("🎯 Goals")
    st.info("Coming Soon")

elif page == "Memory":
    st.title("🧠 Memory")
    st.info("Coming Soon")

elif page == "Planner":
    st.title("📅 Planner")
    st.info("Coming Soon")

elif page == "Knowledge Vault":
    st.title("📚 Knowledge Vault")
    st.info("Coming Soon")

else:
    st.title("⚙ Settings")
    st.info("Coming Soon")