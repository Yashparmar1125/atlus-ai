"""
Session service for managing user sessions.
Handles session creation, validation, and lifecycle.
Persists sessions to JSON files for recovery.
"""

import uuid
import time
import json
from typing import Dict, Optional
from datetime import datetime, timedelta
from pathlib import Path

from app.services.memory_service import MemoryService
from app.api.v1.errors import APIError
from app.utils.logger import get_logger

logger = get_logger("atlus.service.session")


class SessionService:
    """
    Business logic for session management.
    """

    # In-memory session storage (use Redis/DB in production)
    _sessions: Dict[str, Dict] = {}
    
    # Session storage file
    SESSIONS_FILE = Path("data/sessions.json")

    # Session configuration
    SESSION_ID_PREFIX = "session_"
    DEFAULT_TTL_HOURS = 24  # Sessions expire after 24 hours of inactivity
    
    @classmethod
    def _ensure_storage(cls):
        """Ensure data directory and sessions file exist."""
        cls.SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not cls.SESSIONS_FILE.exists():
            cls.SESSIONS_FILE.write_text(json.dumps({}, indent=2), encoding='utf-8')
            logger.debug(f"Created sessions file: {cls.SESSIONS_FILE}")
    
    @classmethod
    def _load_sessions(cls) -> Dict[str, Dict]:
        """Load sessions from JSON file."""
        cls._ensure_storage()
        if cls.SESSIONS_FILE.exists():
            try:
                data = json.loads(cls.SESSIONS_FILE.read_text(encoding='utf-8'))
                logger.debug(f"Loaded {len(data)} sessions from {cls.SESSIONS_FILE}")
                return data
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Failed to load sessions: {e}, starting fresh")
                return {}
        return {}
    
    @classmethod
    def _save_sessions(cls):
        """Save sessions to JSON file."""
        cls._ensure_storage()
        cls.SESSIONS_FILE.write_text(json.dumps(cls._sessions, indent=2), encoding='utf-8')
        logger.debug(f"Saved {len(cls._sessions)} sessions to {cls.SESSIONS_FILE}")
    
    @classmethod
    def _init_sessions(cls):
        """Initialize sessions from file on first access."""
        if not hasattr(cls, '_initialized'):
            cls._sessions = cls._load_sessions()
            cls._initialized = True
            logger.info(f"Initialized SessionService with {len(cls._sessions)} sessions from disk")

    @classmethod
    def create_session(cls, user_id: str = "default_user", metadata: Optional[Dict] = None) -> Dict:
        """
        Create a new session.
        
        Args:
            user_id: User identifier
            metadata: Optional session metadata
            
        Returns:
            Dict with session_id and creation info
        """
        cls._init_sessions()
        
        # Generate unique session ID
        session_id = f"{cls.SESSION_ID_PREFIX}{uuid.uuid4().hex[:16]}"
        
        # Create session data
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "last_activity": datetime.utcnow().isoformat() + "Z",
            "metadata": metadata or {},
            "is_active": True
        }
        
        # Store session
        cls._sessions[session_id] = session_data
        
        # Save to file
        cls._save_sessions()
        
        # Initialize memory components for this session
        # This ensures session memory is ready
        MemoryService.get_session_memory(session_id)
        MemoryService.get_working_memory(session_id)
        MemoryService.get_behavior_profile(session_id)
        
        logger.info(f"Created new session: {session_id} for user: {user_id}")
        
        return {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": session_data["created_at"],
            "metadata": session_data["metadata"]
        }

    @classmethod
    def get_session(cls, session_id: str) -> Optional[Dict]:
        """
        Get session information.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session data or None if not found
        """
        cls._init_sessions()
        return cls._sessions.get(session_id)

    @classmethod
    def validate_session(cls, session_id: str) -> bool:
        """
        Validate if session exists and is active.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if session is valid, False otherwise
        """
        if not session_id:
            return False
        
        session = cls._sessions.get(session_id)
        
        if not session:
            return False
        
        if not session.get("is_active", True):
            return False
        
        # Check if session expired (optional - for production)
        # last_activity = datetime.fromisoformat(session["last_activity"].replace("Z", "+00:00"))
        # if datetime.utcnow() - last_activity > timedelta(hours=cls.DEFAULT_TTL_HOURS):
        #     session["is_active"] = False
        #     return False
        
        return True

    @classmethod
    def update_session_activity(cls, session_id: str):
        """
        Update session last activity timestamp.
        
        Args:
            session_id: Session identifier
        """
        cls._init_sessions()
        if session_id in cls._sessions:
            cls._sessions[session_id]["last_activity"] = datetime.utcnow().isoformat() + "Z"
            cls._save_sessions()  # Persist to file
            logger.debug(f"Updated activity for session: {session_id}")

    @classmethod
    def delete_session(cls, session_id: str) -> bool:
        """
        Delete/terminate a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if deleted, False if not found
        """
        cls._init_sessions()
        if session_id not in cls._sessions:
            return False
        
        # Clear memory (including session memory file)
        MemoryService.clear_session(session_id)
        
        # Remove session
        del cls._sessions[session_id]
        
        # Save to file
        cls._save_sessions()
        
        logger.info(f"Deleted session: {session_id}")
        return True

    @classmethod
    def get_session_info(cls, session_id: str) -> Dict:
        """
        Get comprehensive session information including memory stats.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Dict with session and memory information
        """
        session = cls.get_session(session_id)
        
        if not session:
            raise APIError(
                f"Session {session_id} not found",
                status_code=404,
                error_code="SESSION_NOT_FOUND"
            )
        
        # Get memory stats
        memory_stats = MemoryService.get_session_stats(session_id)
        
        return {
            "session_id": session_id,
            "user_id": session["user_id"],
            "created_at": session["created_at"],
            "last_activity": session["last_activity"],
            "is_active": session["is_active"],
            "metadata": session["metadata"],
            "memory": memory_stats
        }

    @classmethod
    def get_last_session(cls, user_id: str = "default_user") -> Optional[Dict]:
        """
        Get the last active session for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Session data of the last active session, or None if no sessions found
        """
        cls._init_sessions()
        
        # Find all sessions for this user
        user_sessions = [
            (session_id, session_data)
            for session_id, session_data in cls._sessions.items()
            if session_data.get("user_id") == user_id and session_data.get("is_active", True)
        ]
        
        if not user_sessions:
            return None
        
        # Sort by last_activity (most recent first)
        user_sessions.sort(
            key=lambda x: x[1].get("last_activity", ""),
            reverse=True
        )
        
        # Return the most recent session
        session_id, session_data = user_sessions[0]
        
        logger.info(f"Found last session for user {user_id}: {session_id}")
        
        return {
            "session_id": session_id,
            "user_id": session_data["user_id"],
            "created_at": session_data["created_at"],
            "last_activity": session_data["last_activity"],
            "is_active": session_data["is_active"],
            "metadata": session_data["metadata"]
        }

