"""Minimal async adapter for the Google Gemini generateContent API."""

import os

import httpx
from dotenv import load_dotenv

load_dotenv()


DEFAULT_MODEL = "gemini-3-flash-preview"
API_BASE = "https://generativelanguage.googleapis.com/v1beta"


class GeminiError(RuntimeError):
    """A Gemini request failed or returned no usable text."""


async def generate_content_with_usage(
    prompt: str,
    model: str = "",
    timeout: float = 300,
) -> tuple[str, int, int]:
    """Return generated text and Gemini input/output token counts."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise GeminiError(
            "GEMINI_API_KEY is missing. Add it to your local .env file."
        )

    model = (model or DEFAULT_MODEL).strip()
    if not model:
        raise GeminiError("A Gemini model name is required.")

    url = f"{API_BASE}/models/{model}:generateContent"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                url,
                params={"key": api_key},
                json=payload,
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        status = exc.response.status_code
        # Show Google's explanation, never the request URL or API key.
        try:
            body = exc.response.json()
            message = body.get("error", {}).get("message", "")
        except (ValueError, AttributeError):
            message = ""
        if not isinstance(message, str):
            message = ""
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if api_key:
            message = message.replace(api_key, "[REDACTED]")
        message = message[:500]
        detail = f": {message}" if message else ""
        raise GeminiError(
            f"Gemini API returned HTTP {status}{detail}"
        ) from None
    except httpx.RequestError as exc:
        raise GeminiError(
            f"Gemini request failed ({type(exc).__name__})."
        ) from None

    try:
        data = response.json()
        candidates = data.get("candidates", [])
        parts = candidates[0]["content"]["parts"]
        result = "".join(
            part.get("text", "")
            for part in parts
            if isinstance(part, dict)
        ).strip()
    except (ValueError, KeyError, IndexError, TypeError):
        raise GeminiError(
            "Gemini returned an unexpected response format."
        ) from None

    if not result:
        raise GeminiError("Gemini returned no text.")
    usage = data.get("usageMetadata", {})
    input_tokens = int(usage.get("promptTokenCount", 0) or 0)
    output_tokens = int(usage.get("candidatesTokenCount", 0) or 0)
    return result, input_tokens, output_tokens



async def generate_content(
    prompt: str,
    model: str = "",
    timeout: float = 300,
) -> str:
    """Backward-compatible text-only Gemini call."""
    result, _, _ = await generate_content_with_usage(
        prompt, model=model, timeout=timeout
    )
    return result
