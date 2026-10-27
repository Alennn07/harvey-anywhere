import pytest

from harvey.brain import Brain
from harvey.config import BrainConfig


class FakeState:
    def __init__(self):
        self.incremented = []
        self.events = []

    async def increment_usage(self, provider="claude"):
        self.incremented.append(provider)

    async def record_usage_event(self, **kwargs):
        self.events.append(kwargs)
        return True


@pytest.mark.asyncio
async def test_gemini_think_records_usage(monkeypatch):
    from harvey import gemini

    async def fake_generate_content(prompt, model="", timeout=300):
        assert prompt == "hello"
        assert model == "gemini-test-model"
        return "world"

    async def fake_generate_content_with_usage(prompt, model="", timeout=300):
        text = await fake_generate_content(prompt, model=model, timeout=timeout)
        return text, 12, 5

    monkeypatch.setattr(
        gemini, "generate_content_with_usage", fake_generate_content_with_usage
    )
    state = FakeState()
    brain = Brain(state, BrainConfig(provider="gemini", model="gemini-test-model"))

    result = await brain.think(
        "hello", session_id="harvey-analyst-123", agent="analyst", task="summary"
    )

    assert result == "world"
    assert state.incremented == ["gemini"]
    assert len(state.events) == 1
    event = state.events[0]
    assert event["provider"] == "gemini"
    assert event["model"] == "gemini-test-model"
    assert event["agent"] == "analyst"
    assert event["task"] == "summary"
    assert event["source"] == "gemini_api"
    assert event["input_tokens"] == 12
    assert event["output_tokens"] == 5
    assert event["duration_ms"] >= 0


@pytest.mark.asyncio
async def test_gemini_preflight_requires_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    brain = Brain(FakeState(), BrainConfig(provider="gemini", model="gemini-test-model"))
    reason = await brain.preflight()
    assert "GEMINI_API_KEY is missing" in reason


@pytest.mark.asyncio
async def test_gemini_preflight_accepts_configured_key(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-not-real")
    brain = Brain(FakeState(), BrainConfig(provider="gemini", model="gemini-test-model"))
    assert await brain.preflight() == ""



@pytest.mark.asyncio
async def test_gemini_generate_content_with_usage_parses_token_metadata(monkeypatch):
    import httpx
    from harvey import gemini

    monkeypatch.setenv("GEMINI_API_KEY", "test-key-not-real")

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "candidates": [{"content": {"parts": [{"text": "hello"}]}}],
                "usageMetadata": {
                    "promptTokenCount": 12,
                    "candidatesTokenCount": 5,
                },
            }

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            pass

        async def post(self, *args, **kwargs):
            return FakeResponse()

    monkeypatch.setattr(httpx, "AsyncClient", FakeClient)

    result = await gemini.generate_content_with_usage("test", model="test-model")
    assert result == ("hello", 12, 5)
