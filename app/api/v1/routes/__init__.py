"""
API v1 routes package.
Contains all v1 endpoint blueprints.
"""

from flask import Flask

from app.api.v1.routes.chat import chat_bp
from app.api.v1.routes.health import health_bp
from app.api.v1.routes.session import session_bp


def register_routes(app: Flask):
    """
    Register all v1 route blueprints.
    
    Args:
        app: Flask application instance
    """
    app.register_blueprint(chat_bp, url_prefix="/api/v1")
    app.register_blueprint(health_bp, url_prefix="/api/v1")
    app.register_blueprint(session_bp, url_prefix="/api/v1")


__all__ = ["register_routes", "chat_bp", "health_bp", "session_bp"]


