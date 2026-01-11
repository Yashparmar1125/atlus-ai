# llm/intent_llm.py

from openai import OpenAI
from app.llm.base import BaseLLM
from app.llm.config import MODELS, OPENROUTER_BASE_URL
import os
from dotenv import load_dotenv
load_dotenv()

class IntentLLM(BaseLLM):
    def __init__(self):
        self.cfg = MODELS["intent"]
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
                "reasoning": {"enabled": self.cfg.get("reasoning", False)}
            }
        )
        return response.choices[0].message.content
