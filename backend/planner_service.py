import sqlite3

from backend.database import get_connection


# ======================================================
# ADD PLANNER TASK
# ======================================================

def add_task(
    title,
    description,
    task_date,
    start_time,
    end_time,
    goal_id,
    priority
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO planner_tasks
        (
            title,
            description,
            task_date,
            start_time,
            end_time,
            goal_id,
            priority
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        description,
        task_date,
        start_time,
        end_time,
        goal_id,
        priority
    ))

    conn.commit()
    conn.close()


# ======================================================
# GET TASKS FOR A DATE
# ======================================================

def get_tasks_by_date(task_date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            planner_tasks.*,
            goals.title AS goal_title
        FROM planner_tasks
        LEFT JOIN goals
            ON planner_tasks.goal_id = goals.id
        WHERE planner_tasks.task_date = ?
        ORDER BY
            CASE
                WHEN start_time IS NULL
                OR start_time = '' THEN 1
                ELSE 0
            END,
            start_time ASC,
            id ASC
    """, (task_date,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ======================================================
# GET ALL TASKS
# ======================================================

def get_all_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            planner_tasks.*,
            goals.title AS goal_title
        FROM planner_tasks
        LEFT JOIN goals
            ON planner_tasks.goal_id = goals.id
        ORDER BY
            task_date DESC,
            start_time ASC,
            id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ======================================================
# GET TASK
# ======================================================

def get_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            planner_tasks.*,
            goals.title AS goal_title
        FROM planner_tasks
        LEFT JOIN goals
            ON planner_tasks.goal_id = goals.id
        WHERE planner_tasks.id = ?
    """, (task_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


# ======================================================
# UPDATE TASK
# ======================================================

def update_task(
    task_id,
    title,
    description,
    task_date,
    start_time,
    end_time,
    goal_id,
    priority
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE planner_tasks
        SET
            title = ?,
            description = ?,
            task_date = ?,
            start_time = ?,
            end_time = ?,
            goal_id = ?,
            priority = ?
        WHERE id = ?
    """, (
        title,
        description,
        task_date,
        start_time,
        end_time,
        goal_id,
        priority,
        task_id
    ))

    conn.commit()
    conn.close()


# ======================================================
# COMPLETE TASK
# ======================================================

def complete_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE planner_tasks
        SET status = 'Completed'
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


# ======================================================
# MARK TASK AS PENDING
# ======================================================

def mark_task_pending(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE planner_tasks
        SET status = 'Pending'
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


# ======================================================
# DELETE TASK
# ======================================================

def delete_task(task_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM planner_tasks
        WHERE id = ?
    """, (task_id,))

    conn.commit()
    conn.close()


# ======================================================
# DAILY STATISTICS
# ======================================================

def get_daily_statistics(task_date):

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------
    # TOTAL TASKS
    # --------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM planner_tasks
        WHERE task_date = ?
    """, (task_date,))

    total = cursor.fetchone()[0]

    # --------------------------------------------------
    # COMPLETED TASKS
    # --------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM planner_tasks
        WHERE task_date = ?
        AND status = 'Completed'
    """, (task_date,))

    completed = cursor.fetchone()[0]

    # --------------------------------------------------
    # PENDING TASKS
    # --------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM planner_tasks
        WHERE task_date = ?
        AND status = 'Pending'
    """, (task_date,))

    pending = cursor.fetchone()[0]

    # --------------------------------------------------
    # HIGH PRIORITY TASKS
    # --------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM planner_tasks
        WHERE task_date = ?
        AND priority = 'High'
        AND status = 'Pending'
    """, (task_date,))

    high_priority = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        completion = 0
    else:
        completion = round(
            (completed / total) * 100
        )

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "high_priority": high_priority,
        "completion": completion
    }


# ======================================================
# GET TASKS LINKED TO A GOAL
# ======================================================

def get_tasks_for_goal(goal_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM planner_tasks
        WHERE goal_id = ?
        ORDER BY
            task_date ASC,
            start_time ASC
    """, (goal_id,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ======================================================
# GET PENDING TASKS
# ======================================================

def get_pending_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            planner_tasks.*,
            goals.title AS goal_title
        FROM planner_tasks
        LEFT JOIN goals
            ON planner_tasks.goal_id = goals.id
        WHERE planner_tasks.status = 'Pending'
        ORDER BY
            task_date ASC,
            start_time ASC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]