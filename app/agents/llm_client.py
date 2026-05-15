from __future__ import annotations

import os


class LLMClient:
    """Optional OpenAI-compatible client for paid model experiments.

    The project remains reproducible without a key because deterministic fallback
    logic is used when this client is disabled or the SDK is unavailable.
    """

    def __init__(self, model: str | None = None, enabled: bool = False) -> None:
        self.model = model or os.getenv("TRADECARE_MODEL", "gpt-4.1-mini")
        self.enabled = enabled and bool(os.getenv("OPENAI_API_KEY"))

    def complete(self, prompt: str) -> str | None:
        if not self.enabled:
            return None
        try:
            from openai import OpenAI
        except ImportError:
            return None

        try:
            client = OpenAI()
            response = client.responses.create(
                model=self.model,
                input=prompt,
                temperature=0.2,
            )
            return response.output_text.strip()
        except Exception:
            return None
