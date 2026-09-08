import sqlite3

from backend.database import get_connection


# ======================================================
# ADD KNOWLEDGE
# ======================================================

def add_knowledge(
    title,
    content,
    category="General",
    tags="",
    source=""
):
    """
    Add a new knowledge item to the Knowledge Vault.
    """

    if not title or not title.strip():
        return False

    if not content or not content.strip():
        return False

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO knowledge_items
        (
            title,
            content,
            category,
            tags,
            source
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        title.strip(),
        content.strip(),
        category.strip(),
        tags.strip(),
        source.strip()
    ))

    conn.commit()
    conn.close()

    return True


# ======================================================
# GET ALL KNOWLEDGE
# ======================================================

def get_all_knowledge():
    """
    Return all Knowledge Vault entries.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM knowledge_items
        ORDER BY updated_at DESC, id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ======================================================
# GET SINGLE KNOWLEDGE ITEM
# ======================================================

def get_knowledge_by_id(knowledge_id):
    """
    Return one Knowledge Vault entry by ID.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM knowledge_items
        WHERE id = ?
    """, (knowledge_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return dict(row)

    return None


# ======================================================
# SEARCH KNOWLEDGE
# ======================================================

def search_knowledge(query):
    """
    Search Knowledge Vault using title,
    content, category, tags and source.
    """

    if not query or not query.strip():

        return get_all_knowledge()

    search_term = f"%{query.strip()}%"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM knowledge_items
        WHERE
            title LIKE ?
            OR content LIKE ?
            OR category LIKE ?
            OR tags LIKE ?
            OR source LIKE ?
        ORDER BY updated_at DESC, id DESC
    """, (
        search_term,
        search_term,
        search_term,
        search_term,
        search_term
    ))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ======================================================
# GET KNOWLEDGE BY CATEGORY
# ======================================================

def get_knowledge_by_category(category):
    """
    Return Knowledge Vault entries
    belonging to a specific category.
    """

    if not category:

        return get_all_knowledge()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM knowledge_items
        WHERE category = ?
        ORDER BY updated_at DESC, id DESC
    """, (category,))

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


# ======================================================
# UPDATE KNOWLEDGE
# ======================================================

def update_knowledge(
    knowledge_id,
    title,
    content,
    category="General",
    tags="",
    source=""
):
    """
    Update an existing Knowledge Vault entry.
    """

    if not title or not title.strip():
        return False

    if not content or not content.strip():
        return False

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE knowledge_items
        SET
            title = ?,
            content = ?,
            category = ?,
            tags = ?,
            source = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (
        title.strip(),
        content.strip(),
        category.strip(),
        tags.strip(),
        source.strip(),
        knowledge_id
    ))

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated


# ======================================================
# DELETE KNOWLEDGE
# ======================================================

def delete_knowledge(knowledge_id):
    """
    Delete a Knowledge Vault entry.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM knowledge_items
        WHERE id = ?
    """, (knowledge_id,))

    conn.commit()

    deleted = cursor.rowcount > 0

    conn.close()

    return deleted


# ======================================================
# GET KNOWLEDGE STATISTICS
# ======================================================

def get_knowledge_statistics():
    """
    Return basic Knowledge Vault statistics.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM knowledge_items
    """)

    total = cursor.fetchone()["total"]

    cursor.execute("""
        SELECT COUNT(DISTINCT category) AS categories
        FROM knowledge_items
        WHERE category IS NOT NULL
        AND category != ''
    """)

    categories = cursor.fetchone()["categories"]

    conn.close()

    return {
        "total": total,
        "categories": categories
    }


# ======================================================
# GET CATEGORIES
# ======================================================

def get_knowledge_categories():
    """
    Return all unique Knowledge Vault categories.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DISTINCT category
        FROM knowledge_items
        WHERE category IS NOT NULL
        AND category != ''
        ORDER BY category
    """)

    rows = cursor.fetchall()

    conn.close()

    return [
        row["category"]
        for row in rows
    ]