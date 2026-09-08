import streamlit as st
from backend.goal_service import add_goal, get_goals


def goals_page():
    st.title("🎯 Goal Manager")

    st.subheader("Add New Goal")

    title = st.text_input("Goal Title")

    description = st.text_area("Description")

    category = st.selectbox(
        "Category",
        [
            "College",
            "Internship",
            "Personal",
            "Career",
            "Health",
            "Finance"
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

    if st.button("Save Goal"):

        if title.strip() == "":
            st.warning("Please enter a goal title.")

        else:
            add_goal(
                title,
                description,
                category,
                priority,
                str(deadline)
            )

            st.success("Goal saved successfully!")

    st.divider()

    st.subheader("Your Goals")

    goals = get_goals()

    if len(goals) == 0:
        st.info("No goals added yet.")

    else:

        for goal in goals:

            st.markdown(f"### 🎯 {goal[1]}")

            st.write(f"**Description:** {goal[2]}")
            st.write(f"**Category:** {goal[3]}")
            st.write(f"**Priority:** {goal[4]}")
            st.write(f"**Deadline:** {goal[5]}")
            st.write(f"**Status:** {goal[6]}")

            st.divider()