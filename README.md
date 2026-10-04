# GenAI Chatbot

A simple Streamlit-based chatbot project powered by Groq's LLM API.

## Project structure

- `chatbot.py` — application entry point
- `src/genai_chatbot/app.py` — chatbot logic
- `tests/` — unit tests

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .[dev]
cp .env.example .env
```

Then add your Groq API key to `.env`.

## Run the app

```bash
streamlit run chatbot.py
```

## Run tests

```bash
pytest
```
# streamlit-genai-chatbot
