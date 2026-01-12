# llm/reasoning_llm.py

from openai import OpenAI
from llm.base import BaseLLM
from llm.config import MODELS, OPENROUTER_BASE_URL
import os
from dotenv import load_dotenv
load_dotenv()

class ReasoningLLM(BaseLLM):
    def __init__(self):
        self.cfg = MODELS["reasoning"]
        self.client = OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=os.getenv("OPENROUTER_API_KEY")
        )

    def generate(self, messages, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.cfg["model"],
            messages=messages,
            temperature=self.cfg["temperature"],
            max_tokens=self.cfg["max_tokens"],
            extra_body={
                "reasoning": {"enabled": self.cfg["reasoning"]}
            }
        )
        return response.choices[0].message.content
