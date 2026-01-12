"""
Session endpoint.
Handles session creation and management.
"""

from flask import Blueprint, request, jsonify
import time
from datetime import datetime

from app.api.v1.schemas import (
    SessionCreateRequestSchema,
    SessionCreateResponseSchema,
    SessionCreateData,
    SessionInfoResponseSchema,
    SessionInfoData,
    ContinueSessionResponseSchema,
    ContinueSessionData
)
from app.api.v1.validators import validate_request
from app.api.v1.errors import APIError, handle_api_error
from app.core.middleware import rate_limit
from app.services.session_service import SessionService
from app.utils.logger import get_logger

session_bp = Blueprint("session", __name__)
logger = get_logger("atlus.api.v1.session")


@session_bp.route("/sessions", methods=["POST"])
@rate_limit(max_requests=50, window=60)
def create_session():
    """
    Create a new session.
    
    Request:
        POST /api/v1/sessions
        {
            "user_id": "string (optional, default: 'default_user')",
            "metadata": "object (optional)"
        }
    
    Response:
        {
            "success": true,
            "data": {
                "session_id": "session_abc123...",
                "user_id": "user_123",
                "created_at": "2024-01-01T12:00:00Z",
                "metadata": {}
            },
            "timestamp": "2024-01-01T12:00:00Z"
        }
    """
    request_id = request.headers.get(
        "X-Request-ID",
        f"req_{int(time.time() * 1000)}"
    )

    logger.info(f"[{request_id}] Session creation request received")

    try:
        # Validate request
        payload = validate_request(SessionCreateRequestSchema, request)

        # Create session
        user_id = payload.get("user_id", "default_user")
        metadata = payload.get("metadata", {})

        session_data = SessionService.create_session(
            user_id=user_id,
            metadata=metadata
        )

        # Build response
        response_schema = SessionCreateResponseSchema(
            success=True,
            data=SessionCreateData(**session_data)
        )

        # Return JSON (handle Pydantic v1/v2 compatibility)
        try:
            return jsonify(response_schema.model_dump()), 201
        except AttributeError:
            return jsonify(response_schema.dict()), 201

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


@session_bp.route("/sessions/<session_id>", methods=["GET"])
@rate_limit(max_requests=100, window=60)
def get_session_info(session_id: str):
    """
    Get session information.
    
    Request:
        GET /api/v1/sessions/{session_id}
    
    Response:
        {
            "success": true,
            "data": {
                "session_id": "session_abc123...",
                "user_id": "user_123",
                "created_at": "2024-01-01T12:00:00Z",
                "last_activity": "2024-01-01T12:30:00Z",
                "is_active": true,
                "metadata": {},
                "memory": {
                    "conversation_turns": 5,
                    "has_session_memory": true,
                    ...
                }
            },
            "timestamp": "2024-01-01T12:30:00Z"
        }
    """
    request_id = request.headers.get(
        "X-Request-ID",
        f"req_{int(time.time() * 1000)}"
    )

    logger.info(f"[{request_id}] Session info request for: {session_id}")

    try:
        # Get session info
        session_info = SessionService.get_session_info(session_id)

        # Build response
        response_schema = SessionInfoResponseSchema(
            success=True,
            data=SessionInfoData(**session_info)
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


@session_bp.route("/sessions/<session_id>", methods=["DELETE"])
@rate_limit(max_requests=50, window=60)
def delete_session(session_id: str):
    """
    Delete/terminate a session.
    
    Request:
        DELETE /api/v1/sessions/{session_id}
    
    Response:
        {
            "success": true,
            "message": "Session deleted successfully",
            "timestamp": "2024-01-01T12:30:00Z"
        }
    """
    request_id = request.headers.get(
        "X-Request-ID",
        f"req_{int(time.time() * 1000)}"
    )

    logger.info(f"[{request_id}] Session deletion request for: {session_id}")

    try:
        # Delete session
        deleted = SessionService.delete_session(session_id)

        if not deleted:
            raise APIError(
                f"Session {session_id} not found",
                status_code=404,
                error_code="SESSION_NOT_FOUND"
            )

        # Return success response
        return jsonify({
            "success": True,
            "message": "Session deleted successfully",
            "session_id": session_id,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 200

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




@session_bp.route("/sessions/continue", methods=["GET"])
@rate_limit(max_requests=100, window=60)
def continue_last_session():
    """
    Get the last active session for a user to continue conversation.
    
    Request:
        GET /api/v1/sessions/continue?user_id=user_123
    
    Query Parameters:
        user_id (optional): User identifier, default: "default_user"
    
    Response:
        {
            "success": true,
            "data": {
                "session_id": "session_abc123...",
                "user_id": "user_123",
                "created_at": "2024-01-01T12:00:00Z",
                "last_activity": "2024-01-01T12:30:00Z",
                "is_active": true,
                "metadata": {}
            },
            "timestamp": "2024-01-01T12:35:00Z"
        }
    
    If no session found:
        {
            "success": false,
            "error": {
                "code": "NO_SESSION_FOUND",
                "message": "No active session found for user"
            },
            "timestamp": "2024-01-01T12:35:00Z"
        }
    """
    request_id = request.headers.get(
        "X-Request-ID",
        f"req_{int(time.time() * 1000)}"
    )

    # Get user_id from query parameters
    user_id = request.args.get("user_id", "default_user")
    
    logger.info(f"[{request_id}] Continue session request for user: {user_id}")

    try:
        # Get last session
        last_session = SessionService.get_last_session(user_id=user_id)

        if not last_session:
            raise APIError(
                f"No active session found for user: {user_id}",
                status_code=404,
                error_code="NO_SESSION_FOUND"
            )

        # Build response
        response_schema = ContinueSessionResponseSchema(
            success=True,
            data=ContinueSessionData(**last_session)
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
