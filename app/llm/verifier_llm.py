# llm/verifier_llm.py

import os
from openai import OpenAI

from app.llm.base import BaseLLM
from app.llm.config import MODELS, OPENROUTER_BASE_URL


class VerifierLLM(BaseLLM):
    """
    Critique / verification LLM.
    Returns structured feedback about errors, gaps, or risks.
    """

    def __init__(self):
        self.cfg = MODELS["verification"]
        self.client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    def generate(self, messages, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.cfg["model"],
            messages=messages,
            temperature=self.cfg["temperature"],
            max_tokens=self.cfg["max_tokens"],
            extra_body={
                "reasoning": {"enabled": self.cfg.get("reasoning", False)}
            },
        )

        return response.choices[0].message.content
