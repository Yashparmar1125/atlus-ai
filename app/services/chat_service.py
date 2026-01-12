# app/services/chat_service.py

import time
from typing import Dict, Any

from orchestrator.orchestrator import Orchestrator
from app.api.v1.errors import APIError
from app.utils.logger import get_logger

logger = get_logger("atlus.service.chat")


class ChatService:
    """
    Business logic for chat interactions.
    """

    _orchestrator_instance: Orchestrator | None = None
    MAX_MESSAGE_LENGTH = 5000

    @classmethod
    def _get_orchestrator(cls) -> Orchestrator:
        """Singleton orchestrator instance."""
        if cls._orchestrator_instance is None:
            logger.info("Creating new Orchestrator instance")
            cls._orchestrator_instance = Orchestrator()
        return cls._orchestrator_instance

    @classmethod
    def process_chat(cls, payload: Dict[str, Any], request_id: str) -> Dict[str, Any]:
        """
        Process chat request.

        Args:
            payload: validated request payload
            request_id: request identifier

        Returns:
            Dict with response data
        """
        start_time = time.time()

        message = payload.get("message", "").strip()
        session_id = payload.get("session_id")

        # Business validations
        if not message:
            raise APIError(
                "message field is required and cannot be empty",
                status_code=400,
                error_code="INVALID_REQUEST"
            )

        if len(message) > cls.MAX_MESSAGE_LENGTH:
            raise APIError(
                f"Message exceeds maximum length of {cls.MAX_MESSAGE_LENGTH} characters",
                status_code=400,
                error_code="MESSAGE_TOO_LONG"
            )

        logger.info(f"[{request_id}] Processing message: {message[:100]}...")

        orchestrator = cls._get_orchestrator()
        response_text = orchestrator.run(message)

        execution_time = round(time.time() - start_time, 2)

        logger.info(f"[{request_id}] Completed in {execution_time}s")

        return {
            "response": response_text,
            "session_id": session_id,
            "execution_time": execution_time,
            "request_id": request_id,
        }
