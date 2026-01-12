"""
Memory service for managing user memories across sessions.
"""

from typing import Dict, Optional
from memory import (
    SessionMemory,
    WorkingMemory,
    LongTermMemory,
    BehaviorProfile,
    ContextAssembler
)
from app.utils.logger import get_logger

logger = get_logger("atlus.service.memory")


class MemoryService:
    """
    Manages memory instances for users and sessions.
    """

    # In-memory storage (use Redis in production)
    _sessions: Dict[str, SessionMemory] = {}
    _working: Dict[str, WorkingMemory] = {}
    _long_term: Dict[str, LongTermMemory] = {}
    _behavior: Dict[str, BehaviorProfile] = {}

    @classmethod
    def get_session_memory(cls, session_id: str) -> SessionMemory:
        """Get or create session memory."""
        if session_id not in cls._sessions:
            logger.info(f"Creating new session memory: {session_id}")
            cls._sessions[session_id] = SessionMemory(session_id)
        return cls._sessions[session_id]

    @classmethod
    def get_working_memory(cls, session_id: str) -> WorkingMemory:
        """Get or create working memory."""
        if session_id not in cls._working:
            logger.info(f"Creating new working memory: {session_id}")
            cls._working[session_id] = WorkingMemory(session_id)
        return cls._working[session_id]

    @classmethod
    def get_long_term_memory(cls, user_id: str = "default_user") -> LongTermMemory:
        """Get or create long-term memory."""
        if user_id not in cls._long_term:
            logger.info(f"Loading long-term memory: {user_id}")
            cls._long_term[user_id] = LongTermMemory(user_id)
        return cls._long_term[user_id]

    @classmethod
    def get_behavior_profile(cls, session_id: str) -> BehaviorProfile:
        """Get or create behavior profile."""
        if session_id not in cls._behavior:
            logger.info(f"Creating new behavior profile: {session_id}")
            cls._behavior[session_id] = BehaviorProfile()
        return cls._behavior[session_id]

    @classmethod
    def build_context(
        cls,
        system_prompt: str,
        session_id: str,
        user_id: str = "default_user",
        user_message: str = None
    ) -> list:
        """
        Build context with memory.
        
        Args:
            system_prompt: Base system prompt
            session_id: Session identifier
            user_id: User identifier
            user_message: Current user message (for behavior adaptation)
            
        Returns:
            List of messages for LLM
        """
        session = cls.get_session_memory(session_id)
        working = cls.get_working_memory(session_id)
        long_term = cls.get_long_term_memory(user_id)
        behavior = cls.get_behavior_profile(session_id)

        context = ContextAssembler.build_context(
            system_prompt=system_prompt,
            session=session,
            working=working,
            long_term=long_term,
            behavior=behavior,
            last_user_message=user_message
        )

        logger.debug(f"Built context with {len(context)} messages for session {session_id}")
        return context

    @classmethod
    def save_turn(
        cls,
        session_id: str,
        user_message: str,
        agent_response: str,
        user_id: str = "default_user"
    ):
        """
        Save a conversation turn to session memory.
        Also extracts and saves preferences to long-term memory.
        """
        from memory.memory_logger import MemoryLogger
        
        session = cls.get_session_memory(session_id)
        session.add_turn(user_message, agent_response)
        logger.debug(f"Saved turn to session {session_id}")
        MemoryLogger.log_write(
            "session",
            key="turn_saved",
            value=f"user: {user_message[:50]}...",
            session_id=session_id
        )
        
        # Extract and save preferences to long-term memory
        cls._extract_and_save_preferences(session_id, user_message, user_id)

    @classmethod
    def clear_session(cls, session_id: str):
        """Clear session memory."""
        if session_id in cls._sessions:
            # Clear the session memory file
            session_memory = cls._sessions[session_id]
            if hasattr(session_memory, 'clear'):
                session_memory.clear()
            del cls._sessions[session_id]
            logger.info(f"Cleared session memory: {session_id}")
        
        if session_id in cls._working:
            del cls._working[session_id]
            logger.info(f"Cleared working memory: {session_id}")
        
        if session_id in cls._behavior:
            del cls._behavior[session_id]
            logger.info(f"Cleared behavior profile: {session_id}")

    @classmethod
    def _extract_and_save_preferences(cls, session_id: str, user_message: str, user_id: str):
        """
        Extract preferences from user message and save to long-term memory.
        """
        try:
            from app.services.preference_extractor import PreferenceExtractor
            
            # Get conversation history
            session = cls.get_session_memory(session_id)
            conversation_history = session.get_context()
            
            # Extract preferences
            preferences = PreferenceExtractor.extract_preferences(
                user_message, 
                conversation_history
            )
            
            if preferences:
                # Save to long-term memory
                long_term = cls.get_long_term_memory(user_id)
                for key, value in preferences.items():
                    long_term.update(key, value)
                    logger.info(f"Saved preference to long-term memory: {key} = {value} (user: {user_id})")
            
        except Exception as e:
            # Don't fail the whole request if preference extraction fails
            logger.warning(f"Failed to extract preferences: {str(e)}", exc_info=True)

    @classmethod
    def get_session_stats(cls, session_id: str) -> Dict:
        """Get session statistics."""
        stats = {
            "session_id": session_id,
            "has_session_memory": session_id in cls._sessions,
            "has_working_memory": session_id in cls._working,
            "has_behavior_profile": session_id in cls._behavior,
        }

        if session_id in cls._sessions:
            stats["conversation_turns"] = len(cls._sessions[session_id].history) // 2

        return stats


