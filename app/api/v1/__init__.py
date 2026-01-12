"""
API v1 package.
Contains all v1 endpoints, schemas, and utilities.
"""

from flask import Flask

from app.api.v1.routes import register_routes
from app.api.v1.errors import register_error_handlers
from app.core.middleware import register_middleware


def register_v1_api(app: Flask):
    """
    Register API v1 components.
    
    Args:
        app: Flask application instance
    """
    register_routes(app)
    register_error_handlers(app)
    register_middleware(app)


__all__ = ["register_v1_api"]
