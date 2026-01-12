# llm/base.py

from abc import ABC, abstractmethod

class BaseLLM(ABC):

    @abstractmethod
    def generate(self, messages: list[dict], **kwargs) -> str:
        """
        messages: OpenAI-style messages
        returns: assistant text
        """
        pass
