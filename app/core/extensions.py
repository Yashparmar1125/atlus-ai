"""
Flask extensions initialization.
Centralized place for extension instances (CORS, etc.).
"""

from flask_cors import CORS

# Initialize extensions (don't bind to app yet)
cors = CORS()


def init_extensions(app):
    """
    Initialize Flask extensions.
    
    Args:
        app: Flask application instance
    """
    # Configure CORS
    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": "*",
                "methods": ["GET", "POST", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "X-Request-ID"]
            }
        }
    )

