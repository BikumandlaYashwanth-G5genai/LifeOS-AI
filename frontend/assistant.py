import streamlit as st

from backend.ai_service import (
    ask_gemini,
    get_ai_context
)


# ======================================================
# PAGE HEADER
# ======================================================

def show_header():

    st.title("🤖 LifeOS AI Assistant")

    st.markdown(
        "Ask questions naturally and let LifeOS "
        "use your goals and memories to help you."
    )

    st.divider()


# ======================================================
# INITIALIZE CHAT
# ======================================================

def initialize_chat():

    if "assistant_messages" not in st.session_state:
        st.session_state["assistant_messages"] = []


# ======================================================
# SHOW EXAMPLE QUESTIONS
# ======================================================

def show_example_questions():

    st.markdown("### 💡 Try asking")

    examples = [
        "What are my current goals?",
        "What are my high priority goals?",
        "What should I focus on?",
        "What do you remember about me?",
        "What are my study related goals?"
    ]

    columns = st.columns(2)

    for index, example in enumerate(examples):

        with columns[index % 2]:

            if st.button(
                example,
                key=f"assistant_example_{index}",
                use_container_width=True
            ):

                st.session_state[
                    "assistant_pending_query"
                ] = example

                st.rerun()


# ======================================================
# SHOW CHAT HISTORY
# ======================================================

def show_chat_history():

    messages = st.session_state.get(
        "assistant_messages",
        []
    )

    if not messages:

        st.info(
            "👋 Start a conversation with LifeOS AI. "
            "Ask about your goals, memories, priorities, "
            "or anything you want help with."
        )

        return

    for message in messages:

        role = message.get(
            "role",
            "assistant"
        )

        content = message.get(
            "content",
            ""
        )

        with st.chat_message(role):

            st.markdown(content)

            # ------------------------------------------
            # CONTEXT USED
            # ------------------------------------------

            context = message.get(
                "context"
            )

            if role == "assistant" and context:

                goals = context.get(
                    "goals",
                    []
                )

                memories = context.get(
                    "memories",
                    []
                )

                with st.expander(
                    "🔎 View context used by LifeOS"
                ):

                    # ----------------------------------
                    # GOALS
                    # ----------------------------------

                    st.markdown(
                        "#### 🎯 Relevant Goals"
                    )

                    if goals:

                        for goal in goals:

                            st.write(
                                f"• **{goal.get('title', '')}** "
                                f"— {goal.get('status', '')}"
                            )

                    else:

                        st.caption(
                            "No relevant goals found."
                        )

                    # ----------------------------------
                    # MEMORIES
                    # ----------------------------------

                    st.markdown(
                        "#### 🧠 Relevant Memories"
                    )

                    if memories:

                        for memory in memories:

                            st.write(
                                f"• {memory.get('content', '')}"
                            )

                    else:

                        st.caption(
                            "No relevant memories found."
                        )


# ======================================================
# PROCESS QUESTION
# ======================================================

def process_question(query):

    clean_query = query.strip()

    if not clean_query:
        return

    # --------------------------------------------------
    # SHOW USER MESSAGE IMMEDIATELY
    # --------------------------------------------------

    st.session_state[
        "assistant_messages"
    ].append(
        {
            "role": "user",
            "content": clean_query
        }
    )

    # --------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------

    with st.spinner("🧠 LifeOS is thinking..."):

        response = ask_gemini(
            clean_query
        )

    # --------------------------------------------------
    # GET CONTEXT
    # --------------------------------------------------

    context = get_ai_context(
        clean_query,
        limit=5
    )

    # --------------------------------------------------
    # SAVE AI RESPONSE
    # --------------------------------------------------

    st.session_state[
        "assistant_messages"
    ].append(
        {
            "role": "assistant",
            "content": response,
            "context": context
        }
    )


# ======================================================
# MAIN ASSISTANT PAGE
# ======================================================

def assistant_page():

    initialize_chat()

    show_header()

    # --------------------------------------------------
    # EXAMPLE QUESTIONS
    # --------------------------------------------------

    if not st.session_state[
        "assistant_messages"
    ]:

        show_example_questions()

        st.divider()

    # --------------------------------------------------
    # CHAT HISTORY
    # --------------------------------------------------

    show_chat_history()

    # --------------------------------------------------
    # PENDING EXAMPLE QUESTION
    # --------------------------------------------------

    pending_query = st.session_state.pop(
        "assistant_pending_query",
        None
    )

    if pending_query:

        process_question(
            pending_query
        )

        st.rerun()

    # --------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------

    query = st.chat_input(
        "💬 Ask LifeOS anything..."
    )

    if query:

        process_question(
            query
        )

        st.rerun()