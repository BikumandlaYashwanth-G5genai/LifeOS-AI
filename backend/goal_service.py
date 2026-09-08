import sqlite3

DB_NAME = "database/lifeos.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def add_goal(title, description, category, priority, deadline):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO goals
    (title, description, category, priority, deadline)
    VALUES (?, ?, ?, ?, ?)
    """,
    (title, description, category, priority, deadline))

    conn.commit()
    conn.close()


def get_goals():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM goals ORDER BY id DESC")

    goals = cursor.fetchall()

    conn.close()

    return goals