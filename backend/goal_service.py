import sqlite3

DB_NAME = "database/lifeos.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ======================================================
# ADD GOAL
# ======================================================

def add_goal(title, description, category, priority, deadline):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO goals
        (title, description, category, priority, deadline)
        VALUES (?, ?, ?, ?, ?)
    """, (
        title,
        description,
        category,
        priority,
        deadline
    ))

    conn.commit()
    conn.close()


# ======================================================
# GET ALL GOALS
# ======================================================

def get_goals():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM goals
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    goals = [dict(row) for row in rows]

    conn.close()

    return goals


# ======================================================
# DELETE GOAL
# ======================================================

def delete_goal(goal_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM goals WHERE id = ?",
        (goal_id,)
    )

    conn.commit()
    conn.close()


# ======================================================
# COMPLETE GOAL
# ======================================================

def complete_goal(goal_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE goals
        SET status = 'Completed'
        WHERE id = ?
    """, (goal_id,))

    conn.commit()
    conn.close()


# ======================================================
# UPDATE GOAL
# ======================================================

def update_goal(goal_id, title, description, category, priority, deadline):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE goals
        SET
            title = ?,
            description = ?,
            category = ?,
            priority = ?,
            deadline = ?
        WHERE id = ?
    """, (
        title,
        description,
        category,
        priority,
        deadline,
        goal_id
    ))

    conn.commit()
    conn.close()