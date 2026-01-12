"""
API package initialization.
Registers all API versions and their blueprints.
"""

from flask import Flask

from app.api.v1 import register_v1_api


def init_api(app: Flask):
    """
    Initialize all API versions.
    
    Args:
        app: Flask application instance
    """
    register_v1_api(app)


