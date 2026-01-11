"""
API package initialization.
"""

from flask import Flask

from app.api.chat import chat_bp
from app.api.errors import register_error_handlers
from app.api.middleware import register_middleware


def register_blueprints(app: Flask):
    """Register all API blueprints."""
    app.register_blueprint(chat_bp, url_prefix='/api/v1')


def init_api(app: Flask):
    """Initialize API components."""
    register_blueprints(app)
    register_error_handlers(app)
    register_middleware(app)
