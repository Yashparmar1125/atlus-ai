from groq import Groq
from app.llm.base import BaseLLM
from app.llm.config import MODELS
import os
from dotenv import load_dotenv
load_dotenv()

class ChatLLM(BaseLLM):
    def __init__(self):
        self.cfg = MODELS["chatting"]
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def generate(self, messages, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.cfg["model"],
            messages=messages,
            temperature=self.cfg["temperature"],
            max_completion_tokens=self.cfg["max_tokens"],
            top_p=1,
            stream=True,
            stop=None
        )
        return response.choices[0].message.content