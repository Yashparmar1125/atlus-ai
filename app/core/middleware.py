"""
Application middleware.
Handles cross-cutting concerns: logging, rate limiting, security, etc.
"""

import time
import uuid
from functools import wraps
from collections import defaultdict
from datetime import datetime, timedelta

from flask import Flask, request, g
from app.utils.logger import get_logger

logger = get_logger("atlus.middleware")

# Rate limiting storage (in-memory, use Redis in production)
_rate_limit_storage = defaultdict(list)


def register_middleware(app: Flask):
    """
    Register all middleware with the Flask app.
    
    Args:
        app: Flask application instance
    """
    _register_request_logging(app)
    _register_request_id(app)
    _register_security_headers(app)
    _register_response_time(app)
    
    logger.info("Middleware registered successfully")


def _register_request_logging(app: Flask):
    """Log all incoming requests."""
    @app.before_request
    def log_request():
        logger.info(f"{request.method} {request.path} - {request.remote_addr}")


def _register_request_id(app: Flask):
    """Add unique request ID to each request."""
    @app.before_request
    def add_request_id():
        g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))


def _register_security_headers(app: Flask):
    """Add security headers to all responses."""
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response


def _register_response_time(app: Flask):
    """Add response time tracking."""
    @app.before_request
    def start_timer():
        g.start_time = time.time()

    @app.after_request
    def add_response_time(response):
        if hasattr(g, 'start_time'):
            elapsed = time.time() - g.start_time
            response.headers['X-Response-Time'] = f"{elapsed:.3f}s"
        return response


def rate_limit(max_requests: int = 100, window: int = 60):
    """
    Rate limiting decorator.
    
    Args:
        max_requests: Maximum requests allowed in window
        window: Time window in seconds
        
    Usage:
        @rate_limit(max_requests=10, window=60)
        def my_endpoint():
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Get client identifier
            client_id = request.remote_addr
            endpoint = request.endpoint
            key = f"{client_id}:{endpoint}"
            
            # Get current time
            now = datetime.now()
            cutoff = now - timedelta(seconds=window)
            
            # Clean old requests
            _rate_limit_storage[key] = [
                req_time for req_time in _rate_limit_storage[key]
                if req_time > cutoff
            ]
            
            # Check rate limit
            if len(_rate_limit_storage[key]) >= max_requests:
                logger.warning(f"Rate limit exceeded for {client_id} on {endpoint}")
                from app.api.v1.errors import APIError
                raise APIError(
                    f"Rate limit exceeded. Maximum {max_requests} requests per {window} seconds.",
                    status_code=429,
                    error_code="RATE_LIMIT_EXCEEDED"
                )
            
            # Add current request
            _rate_limit_storage[key].append(now)
            
            return f(*args, **kwargs)
        
        return wrapped
    return decorator

