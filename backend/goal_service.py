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
    # ======================================================
# DASHBOARD STATISTICS
# ======================================================

def get_dashboard_statistics():
    conn = get_connection()
    cursor = conn.cursor()

    # Total Goals
    cursor.execute("SELECT COUNT(*) FROM goals")
    total = cursor.fetchone()[0]

    # Completed Goals
    cursor.execute("""
        SELECT COUNT(*)
        FROM goals
        WHERE status = 'Completed'
    """)
    completed = cursor.fetchone()[0]

    # Pending Goals
    cursor.execute("""
        SELECT COUNT(*)
        FROM goals
        WHERE status = 'Pending'
    """)
    pending = cursor.fetchone()[0]

    # High Priority Goals
    cursor.execute("""
        SELECT COUNT(*)
        FROM goals
        WHERE priority = 'High'
        AND status = 'Pending'
    """)
    high_priority = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "high_priority": high_priority
    }


# ======================================================
# UPCOMING DEADLINES
# ======================================================

def get_upcoming_deadlines(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM goals
        WHERE status = 'Pending'
        ORDER BY deadline ASC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ======================================================
# HIGH PRIORITY GOALS
# ======================================================

def get_high_priority_goals(limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM goals
        WHERE priority = 'High'
        AND status = 'Pending'
        ORDER BY deadline ASC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]
# ======================================================
# COMPLETION PERCENTAGE
# ======================================================

def get_completion_percentage():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM goals")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM goals
        WHERE status = 'Completed'
    """)

    completed = cursor.fetchone()[0]

    conn.close()

    if total == 0:
        return 0

    return round((completed / total) * 100)

# ======================================================
# MARK GOAL AS PENDING
# ======================================================

def mark_goal_pending(goal_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE goals
        SET status = 'Pending'
        WHERE id = ?
    """, (goal_id,))

    conn.commit()
    conn.close()