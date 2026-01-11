"""
Chat API endpoint for ATLUS agent.
Handles user requests and returns agent responses.
"""

from flask import Blueprint, request, jsonify
from typing import Dict, Any
import time

from app.agent.agent import Agent
from app.utils.logger import get_logger
from app.api.schemas import ChatRequestSchema, ChatResponseSchema, ChatResponseData, ErrorResponseSchema
from app.api.validators import validate_request
from app.api.errors import APIError, handle_api_error
from app.api.middleware import rate_limit

# Create blueprint
chat_bp = Blueprint('chat', __name__)

# Initialize logger
logger = get_logger("atlus.api.chat")

# Initialize agent (singleton pattern)
_agent_instance = None


def get_agent() -> Agent:
    """Get or create agent instance (singleton)."""
    global _agent_instance
    if _agent_instance is None:
        logger.info("Creating new Agent instance")
        _agent_instance = Agent()
    return _agent_instance


@chat_bp.route('/chat', methods=['POST'])
@rate_limit(max_requests=100, window=60)  # 100 requests per minute
def chat():
    """
    Main chat endpoint.
    
    Accepts user messages and returns agent-generated responses.
    
    Request Body:
        {
            "message": "string (required)",
            "session_id": "string (optional)",
            "metadata": {} (optional)
        }
    
    Response:
        {
            "success": true,
            "data": {
                "response": "string",
                "session_id": "string",
                "execution_time": float
            },
            "timestamp": "ISO 8601"
        }
    """
    start_time = time.time()
    request_id = request.headers.get('X-Request-ID', f"req_{int(time.time() * 1000)}")
    
    logger.info(f"[{request_id}] Chat request received")
    
    try:
        # Validate request
        data = validate_request(ChatRequestSchema, request)
        message = data.get('message', '').strip()
        
        if not message:
            raise APIError(
                "message field is required and cannot be empty",
                status_code=400,
                error_code="INVALID_REQUEST"
            )
        
        # Check message length
        max_length = 5000  # Configurable
        if len(message) > max_length:
            raise APIError(
                f"Message exceeds maximum length of {max_length} characters",
                status_code=400,
                error_code="MESSAGE_TOO_LONG"
            )
        
        logger.info(f"[{request_id}] Processing message: {message[:100]}...")
        
        # Get agent instance
        agent = get_agent()
        
        # Process request
        response_text = agent.run(message)
        
        execution_time = time.time() - start_time
        
        logger.info(f"[{request_id}] Request completed in {execution_time:.2f}s")
        
        # Build response
        response_data = {
            "response": response_text,
            "session_id": data.get('session_id'),
            "execution_time": round(execution_time, 2),
            "request_id": request_id
        }
        
        # Create response schema
        response_schema = ChatResponseSchema(
            success=True,
            data=ChatResponseData(**response_data)
        )
        
        # Use model_dump for Pydantic v2, fallback to dict for v1
        try:
            return jsonify(response_schema.model_dump()), 200
        except AttributeError:
            return jsonify(response_schema.dict()), 200
        
    except APIError as e:
        logger.warning(f"[{request_id}] API Error: {str(e)}")
        return handle_api_error(e, request_id)
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"[{request_id}] Unexpected error: {str(e)}", exc_info=True)
        return handle_api_error(
            APIError(
                "An internal server error occurred",
                status_code=500,
                error_code="INTERNAL_ERROR"
            ),
            request_id
        ), 500


@chat_bp.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint.
    
    Returns:
        {
            "status": "healthy",
            "service": "atlus-api",
            "timestamp": "ISO 8601"
        }
    """
    return jsonify({
        "status": "healthy",
        "service": "atlus-api",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }), 200

