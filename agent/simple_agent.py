"""
Simple Agent for basic interactions.
Handles greetings, simple questions, and casual conversation.
Uses minimal processing for quick responses.
"""

from llm.chat_llm import ChatLLM
from prompts.chat_prompt import build_simple_prompt
from utils.logger import get_logger
import time


class SimpleAgent:
    """
    Simple agent for basic interactions.
    
    Use cases:
    - Greetings (hi, hello, hey)
    - Simple questions
    - Casual conversation
    - Thanks/goodbye
    
    This agent uses a single LLM call for quick responses.
    """
    
    def __init__(self):
        self.logger = get_logger("atlus.agent.simple")
        self.chat_llm = ChatLLM()
        self.logger.debug("SimpleAgent initialized")
    
    def run(self, user_message: str, context_messages: list = None) -> str:
        """
        Process simple user message with minimal processing.
        
        Args:
            user_message: User's input message
            context_messages: Pre-built context with memory (optional)
            
        Returns:
            Response string
        """
        start_time = time.time()
        self.logger.info(f"SimpleAgent processing: {user_message[:50]}...")
        
        try:
            # Use context if provided, otherwise build simple prompt
            if context_messages:
                self.logger.debug("Using context messages with memory")
                prompt = context_messages
                # Add current user message
                prompt.append({"role": "user", "content": user_message})
            else:
                # Build simple prompt without memory
                prompt = build_simple_prompt(user_message)
            
            # Single LLM call for quick response
            response = self.chat_llm.generate(prompt)
            
            execution_time = time.time() - start_time
            self.logger.info(f"SimpleAgent completed in {execution_time:.2f}s")
            
            return response
            
        except Exception as e:
            self.logger.error(f"SimpleAgent error: {str(e)}", exc_info=True)
            # Fallback response
            return "Hello! How can I help you today?"
    

