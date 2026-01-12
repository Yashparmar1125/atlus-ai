"""
Test memory integration.
Verifies that memory system works with the orchestrator.
"""

from app.services.memory_service import MemoryService
from orchestrator.orchestrator import Orchestrator
from utils.logger import get_logger

logger = get_logger("atlus.test")


def test_memory_conversation():
    """Test multi-turn conversation with memory."""
    logger.info("="*80)
    logger.info("Testing Memory Integration")
    logger.info("="*80)
    
    orchestrator = Orchestrator()
    session_id = "test_session_001"
    user_id = "test_user"
    
    # Turn 1: User introduces themselves
    logger.info("--- Turn 1 ---")
    message1 = "Hi, my name is John"
    
    context1 = MemoryService.build_context(
        system_prompt="You are ATLUS, a helpful AI assistant.",
        session_id=session_id,
        user_id=user_id,
        user_message=message1
    )
    
    response1 = orchestrator.run(message1, session_id=session_id, context_messages=context1)
    MemoryService.save_turn(session_id, message1, response1, user_id=user_id)
    
    logger.info(f"User: {message1}")
    logger.info(f"ATLUS: {response1}")
    
    # Turn 2: Ask about name (should remember from Turn 1)
    logger.info("--- Turn 2 ---")
    message2 = "What's my name?"
    
    context2 = MemoryService.build_context(
        system_prompt="You are ATLUS, a helpful AI assistant.",
        session_id=session_id,
        user_id=user_id,
        user_message=message2
    )
    
    response2 = orchestrator.run(message2, session_id=session_id, context_messages=context2)
    MemoryService.save_turn(session_id, message2, response2, user_id=user_id)
    
    logger.info(f"User: {message2}")
    logger.info(f"ATLUS: {response2}")
    
    # Check session stats
    logger.info("--- Session Stats ---")
    stats = MemoryService.get_session_stats(session_id)
    logger.info(f"Session ID: {stats['session_id']}")
    logger.info(f"Conversation Turns: {stats.get('conversation_turns', 0)}")
    logger.info(f"Has Session Memory: {stats['has_session_memory']}")
    logger.info(f"Has Working Memory: {stats['has_working_memory']}")
    logger.info(f"Has Behavior Profile: {stats['has_behavior_profile']}")
    
    # Clear session
    logger.info("--- Cleanup ---")
    MemoryService.clear_session(session_id)
    logger.info(f"Session {session_id} cleared")
    
    logger.info("="*80)
    logger.info("Memory Integration Test Complete!")
    logger.info("="*80)


if __name__ == "__main__":
    test_memory_conversation()
