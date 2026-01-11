"""
Flask application factory and server bootstrap.
Industry-standard Flask application setup.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS

from app.utils.logger import get_logger
from app.api import init_api

logger = get_logger("atlus.server")


def create_app(config_name: str = None) -> Flask:
    """
    Application factory pattern.
    
    Args:
        config_name: Configuration name (development, production, testing)
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    config_name = config_name or os.getenv('FLASK_ENV', 'development')
    
    # Import config - use direct import since config.py is in same directory
    import importlib
    config_module = importlib.import_module('app.config')
    
    config_map = {
        'development': config_module.DevelopmentConfig,
        'production': config_module.ProductionConfig,
        'testing': config_module.TestingConfig
    }
    
    app.config.from_object(config_map.get(config_name.lower(), config_module.DevelopmentConfig))
    
    # Initialize CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Request-ID"]
        }
    })
    
    # Initialize API
    init_api(app)
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        """Root endpoint with API information."""
        return jsonify({
            "service": "ATLUS Agent API",
            "version": "1.0.0",
            "status": "operational",
            "endpoints": {
                "chat": "/api/v1/chat",
                "health": "/api/v1/health"
            }
        }), 200
    
    # API documentation endpoint
    @app.route('/api/v1/docs', methods=['GET'])
    def api_docs():
        """API documentation endpoint."""
        return jsonify({
            "title": "ATLUS Agent API",
            "version": "1.0.0",
            "description": "AI Agent API for intelligent task processing",
            "endpoints": {
                "POST /api/v1/chat": {
                    "description": "Process user message and return agent response",
                    "request": {
                        "body": {
                            "message": "string (required)",
                            "session_id": "string (optional)",
                            "metadata": "object (optional)"
                        }
                    },
                    "response": {
                        "success": "boolean",
                        "data": {
                            "response": "string",
                            "session_id": "string",
                            "execution_time": "float",
                            "request_id": "string"
                        },
                        "timestamp": "ISO 8601"
                    }
                },
                "GET /api/v1/health": {
                    "description": "Health check endpoint",
                    "response": {
                        "status": "healthy",
                        "service": "atlus-api",
                        "timestamp": "ISO 8601"
                    }
                }
            }
        }), 200
    
    logger.info("Flask application created successfully")
    return app


def run_server(host: str = '0.0.0.0', port: int = 5000, debug: bool = False):
    """
    Run Flask development server.
    
    Args:
        host: Host to bind to
        port: Port to bind to
        debug: Enable debug mode
    """
    app = create_app()
    
    logger.info(f"Starting ATLUS API server on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )


if __name__ == '__main__':
    run_server(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    )

