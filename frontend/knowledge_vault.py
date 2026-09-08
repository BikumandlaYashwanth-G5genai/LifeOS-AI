import streamlit as st

from backend.knowledge_service import (
    add_knowledge,
    get_all_knowledge,
    search_knowledge,
    update_knowledge,
    delete_knowledge,
    get_knowledge_statistics,
    get_knowledge_categories
)


# =====================================================
# HEADER
# =====================================================

def show_header():

    st.title("📚 Knowledge Vault")

    st.markdown(
        "Store, organize, search, and manage useful "
        "knowledge for your projects, studies, and future reference."
    )

    st.divider()


# =====================================================
# STATISTICS
# =====================================================

def show_statistics():

    stats = get_knowledge_statistics()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "📚 Knowledge Items",
            stats["total"]
        )

    with col2:

        st.metric(
            "🗂️ Categories",
            stats["categories"]
        )


# =====================================================
# ADD KNOWLEDGE
# =====================================================

def show_add_knowledge():

    st.subheader("➕ Add New Knowledge")

    title = st.text_input(
        "Knowledge Title",
        placeholder=(
            "Example: Cloud Computing - Virtualization"
        ),
        key="kv_add_title"
    )

    content = st.text_area(
        "Knowledge / Notes",
        placeholder=(
            "Write the information you want "
            "to store for future reference..."
        ),
        height=180,
        key="kv_add_content"
    )

    col1, col2 = st.columns(2)

    with col1:

        category = st.text_input(
            "🗂️ Category",
            placeholder=(
                "Study, Project, Programming..."
            ),
            key="kv_add_category"
        )

    with col2:

        tags = st.text_input(
            "🏷️ Tags",
            placeholder=(
                "python, ai, cloud, exam"
            ),
            key="kv_add_tags"
        )

    source = st.text_input(
        "🔗 Source",
        placeholder=(
            "Book, website, class, personal notes..."
        ),
        key="kv_add_source"
    )

    if st.button(
        "💾 Save Knowledge",
        type="primary",
        use_container_width=True,
        key="kv_save_knowledge"
    ):

        if not title.strip():

            st.warning(
                "Please enter a knowledge title."
            )

            return

        if not content.strip():

            st.warning(
                "Please enter some knowledge or notes."
            )

            return

        success = add_knowledge(
            title=title.strip(),
            content=content.strip(),
            category=category.strip() or "General",
            tags=tags.strip(),
            source=source.strip()
        )

        if success:

            st.success(
                "✅ Knowledge saved successfully."
            )

            # Clear all input fields
            st.session_state["kv_add_title"] = ""
            st.session_state["kv_add_content"] = ""
            st.session_state["kv_add_category"] = ""
            st.session_state["kv_add_tags"] = ""
            st.session_state["kv_add_source"] = ""

            st.rerun()

        else:

            st.error(
                "❌ Unable to save the knowledge."
            )


# =====================================================
# EDIT KNOWLEDGE
# =====================================================

def show_edit_knowledge(item):

    item_id = item["id"]

    st.markdown(
        "### ✏️ Edit Knowledge"
    )

    title = st.text_input(
        "Knowledge Title",
        value=item.get(
            "title",
            ""
        ),
        key=f"kv_edit_title_{item_id}"
    )

    content = st.text_area(
        "Knowledge / Notes",
        value=item.get(
            "content",
            ""
        ),
        height=200,
        key=f"kv_edit_content_{item_id}"
    )

    col1, col2 = st.columns(2)

    with col1:

        category = st.text_input(
            "🗂️ Category",
            value=item.get(
                "category",
                ""
            ),
            key=f"kv_edit_category_{item_id}"
        )

    with col2:

        tags = st.text_input(
            "🏷️ Tags",
            value=item.get(
                "tags",
                ""
            ),
            key=f"kv_edit_tags_{item_id}"
        )

    source = st.text_input(
        "🔗 Source",
        value=item.get(
            "source",
            ""
        ),
        key=f"kv_edit_source_{item_id}"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "💾 Save Changes",
            type="primary",
            use_container_width=True,
            key=f"kv_save_edit_{item_id}"
        ):

            if not title.strip():

                st.warning(
                    "Title cannot be empty."
                )

                return

            if not content.strip():

                st.warning(
                    "Knowledge content cannot be empty."
                )

                return

            success = update_knowledge(
                knowledge_id=item_id,
                title=title.strip(),
                content=content.strip(),
                category=category.strip() or "General",
                tags=tags.strip(),
                source=source.strip()
            )

            if success:

                st.session_state[
                    f"kv_editing_{item_id}"
                ] = False

                st.success(
                    "✅ Knowledge updated successfully."
                )

                st.rerun()

            else:

                st.error(
                    "❌ Unable to update knowledge."
                )

    with col2:

        if st.button(
            "❌ Cancel",
            use_container_width=True,
            key=f"kv_cancel_edit_{item_id}"
        ):

            st.session_state[
                f"kv_editing_{item_id}"
            ] = False

            st.rerun()


# =====================================================
# KNOWLEDGE CARD
# =====================================================

def show_knowledge_card(item):

    item_id = item["id"]

    editing_key = (
        f"kv_editing_{item_id}"
    )

    # -------------------------------------------------
    # EDIT MODE
    # -------------------------------------------------

    if st.session_state.get(
        editing_key,
        False
    ):

        with st.container(
            border=True
        ):

            show_edit_knowledge(
                item
            )

        return

    # -------------------------------------------------
    # NORMAL VIEW
    # -------------------------------------------------

    with st.container(
        border=True
    ):

        st.markdown(
            f"### 📖 {item.get('title', '')}"
        )

        category = item.get(
            "category",
            "General"
        )

        if category:

            st.caption(
                f"🗂️ Category: {category}"
            )

        st.write(
            item.get(
                "content",
                ""
            )
        )

        tags = item.get(
            "tags",
            ""
        )

        if tags:

            st.caption(
                f"🏷️ Tags: {tags}"
            )

        source = item.get(
            "source",
            ""
        )

        if source:

            st.caption(
                f"🔗 Source: {source}"
            )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "✏️ Edit",
                use_container_width=True,
                key=f"kv_edit_button_{item_id}"
            ):

                st.session_state[
                    editing_key
                ] = True

                st.rerun()

        with col2:

            if st.button(
                "🗑️ Delete",
                use_container_width=True,
                key=f"kv_delete_button_{item_id}"
            ):

                success = delete_knowledge(
                    item_id
                )

                if success:

                    st.success(
                        "✅ Knowledge deleted successfully."
                    )

                else:

                    st.error(
                        "❌ Unable to delete knowledge."
                    )

                st.rerun()


# =====================================================
# SEARCH AND FILTER
# =====================================================

def show_search():

    st.subheader(
        "🔎 Search Knowledge"
    )

    col1, col2 = st.columns(
        [2, 1]
    )

    with col1:

        query = st.text_input(
            "Search",
            placeholder=(
                "Search title, content, tags, "
                "category or source..."
            ),
            key="kv_search"
        )

    with col2:

        categories = get_knowledge_categories()

        category_options = [
            "All Categories"
        ] + categories

        selected_category = st.selectbox(
            "Category",
            category_options,
            key="kv_category_filter"
        )

    # -------------------------------------------------
    # GET KNOWLEDGE
    # -------------------------------------------------

    if query.strip():

        items = search_knowledge(
            query.strip()
        )

    else:

        items = get_all_knowledge()

    # -------------------------------------------------
    # CATEGORY FILTER
    # -------------------------------------------------

    if selected_category != "All Categories":

        items = [
            item
            for item in items
            if item.get("category")
            == selected_category
        ]

    return items


# =====================================================
# KNOWLEDGE LIST
# =====================================================

def show_knowledge_list(items):

    st.subheader(
        "📖 Stored Knowledge"
    )

    if not items:

        st.info(
            "No knowledge found. "
            "Add your first knowledge item above."
        )

        return

    st.caption(
        f"{len(items)} knowledge item(s) found."
    )

    for item in items:

        show_knowledge_card(
            item
        )


# =====================================================
# MAIN KNOWLEDGE VAULT PAGE
# =====================================================

def knowledge_vault_page():

    show_header()

    show_statistics()

    st.divider()

    # -------------------------------------------------
    # ADD KNOWLEDGE
    # -------------------------------------------------

    show_add_knowledge()

    st.divider()

    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------

    items = show_search()

    st.divider()

    # -------------------------------------------------
    # STORED KNOWLEDGE
    # -------------------------------------------------

    show_knowledge_list(
        items
    )