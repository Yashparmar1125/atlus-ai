# llm/writer_llm.py

import os
from openai import OpenAI

from llm.base import BaseLLM
from llm.config import MODELS, OPENROUTER_BASE_URL


class WriterLLM(BaseLLM):
    """
    Final response writer.
    Converts internal reasoning into clean, user-facing text.
    """

    def __init__(self):
        self.cfg = MODELS["writing"]
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
        )

        return response.choices[0].message.content
