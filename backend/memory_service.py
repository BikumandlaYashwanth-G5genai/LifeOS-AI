import sqlite3


DB_NAME = "database/lifeos.db"


# ======================================================
# DATABASE CONNECTION
# ======================================================

def get_connection():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    return conn


# ======================================================
# ADD MEMORY
# ======================================================

def add_memory(content, category):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO memories
        (content, category)
        VALUES (?, ?)
    """, (
        content,
        category
    ))

    conn.commit()
    conn.close()


# ======================================================
# GET ALL MEMORIES
# ======================================================

def get_memories():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM memories
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    memories = [dict(row) for row in rows]

    conn.close()

    return memories


# ======================================================
# SEARCH MEMORIES
# ======================================================

def search_memories(search_text):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM memories
        WHERE content LIKE ?
           OR category LIKE ?
        ORDER BY id DESC
    """, (
        f"%{search_text}%",
        f"%{search_text}%"
    ))

    rows = cursor.fetchall()

    memories = [dict(row) for row in rows]

    conn.close()

    return memories


# ======================================================
# FILTER MEMORIES BY CATEGORY
# ======================================================

def get_memories_by_category(category):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM memories
        WHERE category = ?
        ORDER BY id DESC
    """, (category,))

    rows = cursor.fetchall()

    memories = [dict(row) for row in rows]

    conn.close()

    return memories


# ======================================================
# GET RECENT MEMORIES
# ======================================================

def get_recent_memories(limit=5):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM memories
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    memories = [dict(row) for row in rows]

    conn.close()

    return memories


# ======================================================
# UPDATE MEMORY
# ======================================================

def update_memory(memory_id, content, category):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE memories
        SET
            content = ?,
            category = ?
        WHERE id = ?
    """, (
        content,
        category,
        memory_id
    ))

    conn.commit()
    conn.close()


# ======================================================
# DELETE MEMORY
# ======================================================

def delete_memory(memory_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM memories
        WHERE id = ?
    """, (memory_id,))

    conn.commit()
    conn.close()


# ======================================================
# MEMORY STATISTICS
# ======================================================

def get_memory_statistics():

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------------------
    # TOTAL MEMORIES
    # --------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM memories
    """)

    total = cursor.fetchone()[0]

    # --------------------------------------------------
    # TOTAL CATEGORIES
    # --------------------------------------------------

    cursor.execute("""
        SELECT COUNT(DISTINCT category)
        FROM memories
        WHERE category IS NOT NULL
        AND category != ''
    """)

    categories = cursor.fetchone()[0]

    # --------------------------------------------------
    # RECENT MEMORIES
    # --------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM memories
        WHERE created_at >= datetime('now', '-7 days')
    """)

    recent = cursor.fetchone()[0]

    # --------------------------------------------------
    # MOST USED CATEGORY
    # --------------------------------------------------

    cursor.execute("""
        SELECT category, COUNT(*) AS count
        FROM memories
        WHERE category IS NOT NULL
        AND category != ''
        GROUP BY category
        ORDER BY count DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    if row:

        top_category = row["category"]

    else:

        top_category = "None"

    conn.close()

    return {
        "total": total,
        "categories": categories,
        "recent": recent,
        "top_category": top_category
    }


# ======================================================
# MEMORY RELEVANCE SEARCH
# ======================================================

def find_relevant_memories(query, limit=5):

    if not query or not query.strip():

        return []

    query = query.strip().lower()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM memories
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    memories = [dict(row) for row in rows]

    conn.close()

    # --------------------------------------------------
    # CREATE SEARCH TERMS
    # --------------------------------------------------

    query_words = set(
        word
        for word in query.split()
        if len(word) > 2
    )

    scored_memories = []

    # --------------------------------------------------
    # CALCULATE RELEVANCE
    # --------------------------------------------------

    for memory in memories:

        content = (
            f"{memory.get('content', '')} "
            f"{memory.get('category', '')}"
        ).lower()

        content_words = set(
            word
            for word in content.split()
            if len(word) > 2
        )

        matching_words = query_words.intersection(
            content_words
        )

        score = len(matching_words)

        if score > 0:

            memory["relevance_score"] = score

            memory["matching_terms"] = list(
                matching_words
            )

            scored_memories.append(
                (
                    score,
                    memory
                )
            )

    # --------------------------------------------------
    # SORT BY RELEVANCE
    # --------------------------------------------------

    scored_memories.sort(
        key=lambda item: item[0],
        reverse=True
    )

    # --------------------------------------------------
    # RETURN TOP RESULTS
    # --------------------------------------------------

    return [
        memory
        for score, memory in scored_memories[:limit]
    ]