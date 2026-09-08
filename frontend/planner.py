import streamlit as st
from datetime import date, time

from backend.planner_service import (
    add_task,
    get_tasks_by_date,
    update_task,
    complete_task,
    mark_task_pending,
    delete_task,
    get_daily_statistics
)

from backend.goal_service import get_goals


# =====================================================
# HEADER
# =====================================================

def show_header():

    st.title("📅 LifeOS Planner")

    st.markdown(
        "Plan your day, schedule tasks, connect them to your goals, "
        "and track what you actually complete."
    )

    st.divider()


# =====================================================
# DATE SELECTOR
# =====================================================

def show_date_selector():

    return st.date_input(
        "📆 Select planning date",
        value=date.today(),
        key="planner_selected_date"
    )


# =====================================================
# DAILY STATISTICS
# =====================================================

def show_daily_statistics(selected_date):

    stats = get_daily_statistics(
        selected_date.strftime("%Y-%m-%d")
    )

    st.subheader("📊 Daily Progress")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Tasks", stats["total"])

    with col2:
        st.metric("Completed", stats["completed"])

    with col3:
        st.metric("Pending", stats["pending"])

    with col4:
        st.metric(
            "Progress",
            f"{stats['completion']}%"
        )

    st.progress(
        stats["completion"] / 100
    )


# =====================================================
# ADD TASK
# =====================================================

def show_add_task(selected_date):

    with st.expander(
        "➕ Add New Task",
        expanded=False
    ):

        with st.form(
            "add_planner_task_form",
            clear_on_submit=True
        ):

            title = st.text_input(
                "Task title",
                placeholder="Example: Study Cloud Computing Unit 1"
            )

            description = st.text_area(
                "Description",
                placeholder="What needs to be completed?"
            )

            col1, col2 = st.columns(2)

            with col1:

                start_time = st.time_input(
                    "🕐 Start time",
                    value=time(9, 0)
                )

            with col2:

                end_time = st.time_input(
                    "🕐 End time",
                    value=time(10, 0)
                )

            goals = get_goals()

            goal_options = {
                "No linked goal": None
            }

            for goal in goals:

                goal_options[
                    f"{goal.get('title', 'Untitled Goal')} "
                    f"(ID: {goal.get('id')})"
                ] = goal.get("id")

            selected_goal = st.selectbox(
                "🎯 Link to Goal",
                list(goal_options.keys())
            )

            priority = st.selectbox(
                "🔥 Priority",
                [
                    "Low",
                    "Medium",
                    "High"
                ],
                index=1
            )

            submitted = st.form_submit_button(
                "➕ Add Task",
                type="primary",
                use_container_width=True
            )

            if submitted:

                if not title.strip():

                    st.warning(
                        "Please enter a task title."
                    )

                    return

                if end_time <= start_time:

                    st.warning(
                        "End time must be after start time."
                    )

                    return

                add_task(
                    title=title.strip(),
                    description=description.strip(),
                    task_date=selected_date.strftime(
                        "%Y-%m-%d"
                    ),
                    start_time=start_time.strftime(
                        "%H:%M"
                    ),
                    end_time=end_time.strftime(
                        "%H:%M"
                    ),
                    goal_id=goal_options[selected_goal],
                    priority=priority
                )

                st.success(
                    "✅ Task added successfully."
                )

                st.rerun()

# =====================================================
# EDIT TASK
# =====================================================

def show_edit_task(task):

    task_id = task["id"]

    goals = get_goals()

    goal_options = {
        "No linked goal": None
    }

    for goal in goals:

        goal_options[
            f"{goal.get('title', 'Untitled Goal')} "
            f"(ID: {goal.get('id')})"
        ] = goal.get("id")

    current_goal_id = task.get("goal_id")

    current_goal_name = "No linked goal"

    for name, goal_id in goal_options.items():

        if goal_id == current_goal_id:

            current_goal_name = name
            break

    # -------------------------------------------------
    # DEFAULT TIMES
    # -------------------------------------------------

    try:

        current_start = datetime.strptime(
            task.get("start_time", "09:00"),
            "%H:%M"
        ).time()

    except Exception:

        current_start = time(9, 0)

    try:

        current_end = datetime.strptime(
            task.get("end_time", "10:00"),
            "%H:%M"
        ).time()

    except Exception:

        current_end = time(10, 0)

    try:

        current_date = datetime.strptime(
            task.get("task_date"),
            "%Y-%m-%d"
        ).date()

    except Exception:

        current_date = date.today()

    # -------------------------------------------------
    # EDIT FORM
    # -------------------------------------------------

    with st.form(
        f"edit_task_form_{task_id}"
    ):

        st.markdown(
            "### ✏️ Edit Task"
        )

        title = st.text_input(
            "Task title",
            value=task.get("title", "")
        )

        description = st.text_area(
            "Description",
            value=task.get("description", "")
        )

        edit_date = st.date_input(
            "📆 Date",
            value=current_date
        )

        col1, col2 = st.columns(2)

        with col1:

            edit_start = st.time_input(
                "🕐 Start time",
                value=current_start
            )

        with col2:

            edit_end = st.time_input(
                "🕐 End time",
                value=current_end
            )

        selected_goal = st.selectbox(
            "🎯 Link to Goal",
            list(goal_options.keys()),
            index=list(
                goal_options.keys()
            ).index(current_goal_name)
        )

        priority_options = [
            "Low",
            "Medium",
            "High"
        ]

        current_priority = task.get(
            "priority",
            "Medium"
        )

        if current_priority not in priority_options:

            current_priority = "Medium"

        priority = st.selectbox(
            "🔥 Priority",
            priority_options,
            index=priority_options.index(
                current_priority
            )
        )

        col1, col2 = st.columns(2)

        with col1:

            save = st.form_submit_button(
                "💾 Save Changes",
                type="primary",
                use_container_width=True
            )

        with col2:

            cancel = st.form_submit_button(
                "❌ Cancel",
                use_container_width=True
            )

        if save:

            if not title.strip():

                st.error(
                    "Task title cannot be empty."
                )

                return

            if edit_end <= edit_start:

                st.error(
                    "End time must be after start time."
                )

                return

            update_task(
                task_id=task_id,
                title=title.strip(),
                description=description.strip(),
                task_date=edit_date.strftime(
                    "%Y-%m-%d"
                ),
                start_time=edit_start.strftime(
                    "%H:%M"
                ),
                end_time=edit_end.strftime(
                    "%H:%M"
                ),
                goal_id=goal_options[selected_goal],
                priority=priority
            )

            st.session_state[
                f"editing_task_{task_id}"
            ] = False

            st.success(
                "✅ Task updated successfully."
            )

            st.rerun()

        if cancel:

            st.session_state[
                f"editing_task_{task_id}"
            ] = False

            st.rerun()


# =====================================================
# TASK CARD
# =====================================================

def show_task(task):

    task_id = task["id"]

    status = task.get(
        "status",
        "Pending"
    )

    title = task.get(
        "title",
        ""
    )

    description = task.get(
        "description",
        ""
    )

    start_time = task.get(
        "start_time",
        ""
    )

    end_time = task.get(
        "end_time",
        ""
    )

    priority = task.get(
        "priority",
        "Medium"
    )

    goal_title = task.get(
        "goal_title"
    )

    editing_key = f"editing_task_{task_id}"

    if st.session_state.get(
        editing_key,
        False
    ):

        show_edit_task(task)

        return

    # -------------------------------------------------
    # NORMAL TASK VIEW
    # -------------------------------------------------

    with st.container(border=True):

        if status == "Completed":

            st.markdown(
                f"### ✅ ~~{title}~~"
            )

        else:

            st.markdown(
                f"### 📌 {title}"
            )

        if start_time and end_time:

            st.write(
                f"🕐 **{start_time} – {end_time}**"
            )

        if description:

            st.write(
                description
            )

        info_col1, info_col2, info_col3 = st.columns(3)

        with info_col1:

            st.caption(
                f"🔥 Priority: {priority}"
            )

        with info_col2:

            if goal_title:

                st.caption(
                    f"🎯 Goal: {goal_title}"
                )

            else:

                st.caption(
                    "🎯 No linked goal"
                )

        with info_col3:

            st.caption(
                f"Status: {status}"
            )

        # -------------------------------------------------
        # ACTION BUTTONS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            if status == "Pending":

                if st.button(
                    "✅ Complete",
                    key=f"complete_{task_id}",
                    use_container_width=True
                ):

                    complete_task(
                        task_id
                    )

                    st.rerun()

            else:

                if st.button(
                    "↩️ Reopen",
                    key=f"pending_{task_id}",
                    use_container_width=True
                ):

                    mark_task_pending(
                        task_id
                    )

                    st.rerun()

        with col2:

            if st.button(
                "✏️ Edit",
                key=f"edit_{task_id}",
                use_container_width=True
            ):

                st.session_state[
                    editing_key
                ] = True

                st.rerun()

        with col3:

            if st.button(
                "🗑️ Delete",
                key=f"delete_{task_id}",
                use_container_width=True
            ):

                delete_task(
                    task_id
                )

                st.rerun()


# =====================================================
# DAILY TASKS
# =====================================================

def show_tasks(selected_date):

    task_date = selected_date.strftime(
        "%Y-%m-%d"
    )

    tasks = get_tasks_by_date(
        task_date
    )

    st.subheader(
        f"📋 Schedule for "
        f"{selected_date.strftime('%d %B %Y')}"
    )

    if not tasks:

        st.info(
            "No tasks planned for this day. "
            "Add your first task above."
        )

        return

    for task in tasks:

        show_task(task)


# =====================================================
# MAIN PLANNER PAGE
# =====================================================

def planner_page():

    show_header()

    selected_date = show_date_selector()

    st.divider()

    show_daily_statistics(
        selected_date
    )

    st.divider()

    show_add_task(
        selected_date
    )

    st.divider()

    show_tasks(
        selected_date
    )