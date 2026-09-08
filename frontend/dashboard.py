import streamlit as st


def dashboard():

    st.title("🧠 LifeOS AI")

    st.subheader("Your Intelligent Life Operating System")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Goals", 0)

    with col2:
        st.metric("Memories", 0)

    with col3:
        st.metric("Documents", 0)

    st.markdown("## Welcome")

    st.info(
        "LifeOS AI helps you organize goals, memories, documents and planning using Artificial Intelligence."
    )