from groq import Groq
from llm.base import BaseLLM
from llm.config import MODELS
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
        # Use streaming and collect chunks (Groq SDK pattern)
        response = self.client.chat.completions.create(
            model=self.cfg["model"],
            messages=messages,
            temperature=self.cfg["temperature"],
            max_completion_tokens=self.cfg["max_tokens"],
            top_p=1,
            stream=True,  # Groq works better with streaming
            stop=None
        )
        
        # Collect all chunks
        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
        
        return full_response