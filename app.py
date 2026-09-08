import streamlit as st

from backend.database import initialize_database

from frontend.sidebar import sidebar
from frontend.dashboard import dashboard
from frontend.goals import goals_page
from frontend.memory import memory_page
from frontend.context import context_page
from frontend.assistant import assistant_page
from frontend.knowledge_vault import knowledge_vault_page
from frontend.settings import settings_page



# =====================================================
# DATABASE
# =====================================================

initialize_database()


# =====================================================
# SIDEBAR
# =====================================================

page = sidebar()


# =====================================================
# PAGE ROUTING
# =====================================================

if page == "Dashboard":

    dashboard()


elif page == "Goals":

    goals_page()


elif page == "Memory":

    memory_page()


elif page == "LifeOS Context":

    context_page()


elif page == "AI Assistant":

    assistant_page()


elif page == "Planner":

    from frontend.planner import planner_page

    planner_page()



elif page == "Knowledge Vault":

    knowledge_vault_page()


elif page == "Settings":

    settings_page()