"""
ATLUS Flask Application Package.

Industry-standard Flask application structure with:
- Application factory pattern
- Blueprint-based routing
- Service layer for business logic
- Proper error handling and middleware
"""

__version__ = "1.0.0"
__author__ = "ATLUS Team"

from app.server import create_app

__all__ = ["create_app"]


