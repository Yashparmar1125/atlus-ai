"""
Run ATLUS orchestrator directly (CLI mode).
"""

from orchestrator.orchestrator import Orchestrator
from app.services.memory_service import MemoryService
from utils.logger import get_logger

logger = get_logger("atlus.cli")


def main():
    """Run orchestrator with memory support."""
    orchestrator = Orchestrator()
    session_id = "cli_session"
    
    # Build context with memory
    system_prompt = (
        "You are ATLUS, an intelligent AI assistant.\n"
        "You help users with tasks, questions, and conversations."
    )
    
    user_message = "I want to build a web application with a database and a user authentication system and a chatbot"
    
    context_messages = MemoryService.build_context(
        system_prompt=system_prompt,
        session_id=session_id,
        user_id="cli_user",
        user_message=user_message
    )
    
    # Run orchestrator
    response = orchestrator.run(user_message, session_id=session_id, context_messages=context_messages)
    
    # Save to memory
    MemoryService.save_turn(session_id, user_message, response, user_id="cli_user")
    
    logger.info("="*80)
    logger.info("RESPONSE:")
    logger.info("="*80)
    logger.info(response)
    logger.info("="*80)


if __name__ == "__main__":
    main()