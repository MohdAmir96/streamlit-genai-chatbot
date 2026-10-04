import pytest

from genai_chatbot.app import build_prompt_messages, validate_api_key


def test_build_prompt_messages_includes_history_and_user_prompt() -> None:
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ]

    messages = build_prompt_messages(history, "How are you?")

    assert messages[0] == {"role": "system", "content": "You are a helpful assistant."}
    assert messages[1:] == [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
        {"role": "user", "content": "How are you?"},
    ]


def test_validate_api_key_requires_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(ValueError):
        validate_api_key()

    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    validate_api_key()
