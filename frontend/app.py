import streamlit as st
import requests as req
 
st.title("🤖 My AI Chatbot")


# -----------------------------
# Chat history
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -----------------------------
# User input
# -----------------------------

prompt = st.chat_input("Ask me anything...")


if prompt:

    # -----------------------------
    # Limit query to 100 words
    # -----------------------------

    word_count = len(prompt.split())

    if word_count > 100:
        st.error(
            f"Your query contains {word_count} words. "
            "Please keep it within 100 words."
        )
        st.stop()


    # -----------------------------
    # Save user message
    # -----------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)


    # -----------------------------
    # Call FastAPI
    # -----------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = req.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "message": prompt
                }
            )

            data = response.json()

            answer = data["response"]

            st.markdown(answer)


    # -----------------------------
    # Save assistant response
    # -----------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })