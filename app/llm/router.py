# llm/router.py

from app.llm.intent_llm import IntentLLM
from app.llm.planner_llm import PlannerLLM
from app.llm.reasoning_llm import ReasoningLLM
from app.llm.verifier_llm import VerifierLLM
from app.llm.writer_llm import WriterLLM

def get_llm(role: str):
    """
    Factory function to get LLM instances by role.
    
    Args:
        role: One of "intent", "planning", "reasoning", "verification", "writing"
        
    Returns:
        Appropriate LLM instance
        
    Raises:
        ValueError: If role is not recognized
    """
    if role == "intent":
        return IntentLLM()
    if role == "planning":
        return PlannerLLM()
    if role == "reasoning":
        return ReasoningLLM()
    if role == "verification":
        return VerifierLLM()
    if role == "writing":
        return WriterLLM()
    raise ValueError(f"Unknown LLM role: {role}. Valid roles: intent, planning, reasoning, verification, writing")
