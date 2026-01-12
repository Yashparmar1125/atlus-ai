"""
API error handling and custom exceptions.
"""

from flask import jsonify
from typing import Optional, Dict, Any, List
from datetime import datetime


class APIError(Exception):
    """Custom API exception."""
    
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: Optional[str] = None,
        details: Optional[List[Dict[str, Any]]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or "API_ERROR"
        self.details = details or []
        super().__init__(self.message)


def handle_api_error(error: APIError, request_id: Optional[str] = None) -> tuple:
    """
    Convert APIError to JSON response.
    
    Args:
        error: APIError instance
        request_id: Optional request identifier
        
    Returns:
        Tuple of (JSON response, status code)
    """
    error_response = {
        "success": False,
        "error": {
            "message": error.message,
            "code": error.error_code,
            "status": error.status_code
        },
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "request_id": request_id
    }
    
    if error.details:
        error_response["error"]["details"] = error.details
    
    return jsonify(error_response), error.status_code


def register_error_handlers(app):
    """Register global error handlers for Flask app."""
    
    @app.errorhandler(APIError)
    def handle_api_error_exception(error: APIError):
        """Handle APIError exceptions."""
        request_id = request.headers.get('X-Request-ID')
        return handle_api_error(error, request_id)
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 errors."""
        return jsonify({
            "success": False,
            "error": {
                "message": "Endpoint not found",
                "code": "NOT_FOUND",
                "status": 404
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle 405 errors."""
        return jsonify({
            "success": False,
            "error": {
                "message": "Method not allowed",
                "code": "METHOD_NOT_ALLOWED",
                "status": 405
            },
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 errors."""
        request_id = request.headers.get('X-Request-ID')
        return jsonify({
            "success": False,
            "error": {
                "message": "Internal server error",
                "code": "INTERNAL_ERROR",
                "status": 500
            },
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "request_id": request_id
        }), 500


