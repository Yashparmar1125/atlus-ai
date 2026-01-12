"""
Chat endpoint.
Handles chat interactions with the ATLUS agent.
"""

from flask import Blueprint, request, jsonify
import time

from app.api.v1.schemas import ChatRequestSchema, ChatResponseSchema, ChatResponseData
from app.api.v1.validators import validate_request
from app.api.v1.errors import APIError, handle_api_error
from app.core.middleware import rate_limit
from app.services.chat_service import ChatService
from app.utils.logger import get_logger

chat_bp = Blueprint("chat", __name__)
logger = get_logger("atlus.api.v1.chat")


@chat_bp.route("/chat", methods=["POST"])
@rate_limit(max_requests=100, window=60)
def chat():
    """
    Process chat message.
    
    Request:
        POST /api/v1/chat
        {
            "message": "string (required)",
            "session_id": "string (optional, recommended - use /sessions endpoint to create)",
            "user_id": "string (optional, default: 'default_user')",
            "metadata": "object (optional)"
        }
    
    Response:
        {
            "success": true,
            "data": {
                "response": "string",
                "session_id": "string",
                "execution_time": 1.23,
                "request_id": "string"
            },
            "timestamp": "ISO 8601"
        }
    
    Note:
        - It's recommended to create a session first using POST /api/v1/sessions
        - If session_id is not provided, a temporary session will be created using request_id
        - Session validation is performed if session_id is provided
    """
    request_id = request.headers.get(
        "X-Request-ID",
        f"req_{int(time.time() * 1000)}"
    )

    logger.info(f"[{request_id}] Chat request received")

    try:
        # Validate request
        payload = validate_request(ChatRequestSchema, request)

        # Process chat
        result = ChatService.process_chat(
            payload=payload,
            request_id=request_id
        )

        # Build response
        response_schema = ChatResponseSchema(
            success=True,
            data=ChatResponseData(**result)
        )

        # Return JSON (handle Pydantic v1/v2 compatibility)
        try:
            return jsonify(response_schema.model_dump()), 200
        except AttributeError:
            return jsonify(response_schema.dict()), 200

    except APIError as e:
        logger.warning(f"[{request_id}] API Error: {str(e)}")
        return handle_api_error(e, request_id)

    except Exception as e:
        logger.error(
            f"[{request_id}] Unexpected error: {str(e)}",
            exc_info=True
        )
        return handle_api_error(
            APIError(
                "An internal server error occurred",
                status_code=500,
                error_code="INTERNAL_ERROR"
            ),
            request_id
        )


