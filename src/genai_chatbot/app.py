from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv

SYSTEM_MESSAGE = "You are a helpful assistant."


def load_environment() -> None:
    """Load environment variables from a local .env file when available."""
    load_dotenv()


def build_prompt_messages(
    chat_history: list[dict[str, str]],
    user_prompt: str,
) -> list[dict[str, str]]:
    """Create the final prompt payload sent to the language model."""
    return [
        {"role": "system", "content": SYSTEM_MESSAGE},
        *chat_history,
        {"role": "user", "content": user_prompt},
    ]


def get_api_key() -> str:
    """Return the configured Groq API key."""
    return os.getenv("GROQ_API_KEY", "").strip()


def validate_api_key() -> None:
    """Ensure the required API key is available before creating the client."""
    if not get_api_key():
        raise ValueError(
            "Missing GROQ_API_KEY. Copy .env.example to .env and add your Groq API key."
        )


def create_llm() -> Any:
    """Create and return the Groq chat model client."""
    validate_api_key()
    from langchain_groq import ChatGroq

    return ChatGroq(model="openai/gpt-oss-120b", temperature=0.0)


def main() -> None:
    """Run the Streamlit chatbot UI."""
    load_environment()

    import streamlit as st

    st.set_page_config(
        page_title="Chatbot",
        page_icon="🤖",
        layout="centered",
    )
    st.title("💬Chatbot")

    if not get_api_key():
        st.warning(
            "Missing GROQ_API_KEY. Create a .env file from .env.example and add your Groq API key."
        )
        return
    print(">>>>>>>>",st.session_state)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    llm = create_llm()
    user_prompt = st.chat_input("Ask Chatbot...")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)
        existing_history = st.session_state.chat_history.copy()
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        prompt_messages = build_prompt_messages(existing_history, user_prompt)
        response = llm.invoke(input=prompt_messages)
        assistant_response = response.content
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

        with st.chat_message("assistant"):
            st.markdown(assistant_response)
