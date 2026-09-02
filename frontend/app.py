import streamlit as st
import requests as req
import os


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 My AI Chatbot")


# -----------------------------
# Backend URL
# -----------------------------

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


# -----------------------------
# Chat history
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
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

            try:
                response = req.post(
                    f"{BACKEND_URL}/chat",
                    json={
                        "message": prompt
                    },
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()

                answer = data["response"]

                st.markdown(answer)

            except req.exceptions.RequestException as e:
                st.error("Unable to connect to the backend.")

            except (ValueError, KeyError):
                st.error("Invalid response received from the backend.")


    # -----------------------------
    # Save assistant response
    # -----------------------------

    if "answer" in locals():
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })