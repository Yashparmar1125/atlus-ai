"""
API middleware for request processing.
"""

from flask import request, g
import time
from functools import wraps

from app.utils.logger import get_logger

logger = get_logger("atlus.api.middleware")


def register_middleware(app):
    """Register middleware functions."""
    
    @app.before_request
    def before_request():
        """Execute before each request."""
        g.start_time = time.time()
        g.request_id = request.headers.get('X-Request-ID', f"req_{int(time.time() * 1000)}")
        
        # Log request
        logger.info(
            f"[{g.request_id}] {request.method} {request.path} - "
            f"IP: {request.remote_addr}"
        )
    
    @app.after_request
    def after_request(response):
        """Execute after each request."""
        # Calculate processing time
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            response.headers['X-Process-Time'] = str(round(duration, 3))
        
        # Add request ID to response
        if hasattr(g, 'request_id'):
            response.headers['X-Request-ID'] = g.request_id
        
        # Add CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Request-ID'
        
        # Log response
        if hasattr(g, 'request_id'):
            logger.info(
                f"[{g.request_id}] {request.method} {request.path} - "
                f"Status: {response.status_code} - "
                f"Time: {duration:.3f}s"
            )
        
        return response
    
    @app.after_request
    def add_security_headers(response):
        """Add security headers."""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response


def rate_limit(max_requests: int = 100, window: int = 60):
    """
    Simple rate limiting decorator.
    
    Args:
        max_requests: Maximum requests per window
        window: Time window in seconds
    """
    # In production, use Redis or similar for distributed rate limiting
    request_counts = {}
    
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            client_id = request.remote_addr
            current_time = time.time()
            
            # Clean old entries
            request_counts[client_id] = [
                req_time for req_time in request_counts.get(client_id, [])
                if current_time - req_time < window
            ]
            
            # Check rate limit
            if len(request_counts.get(client_id, [])) >= max_requests:
                from app.api.errors import APIError
                raise APIError(
                    "Rate limit exceeded",
                    status_code=429,
                    error_code="RATE_LIMIT_EXCEEDED"
                )
            
            # Record request
            if client_id not in request_counts:
                request_counts[client_id] = []
            request_counts[client_id].append(current_time)
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

