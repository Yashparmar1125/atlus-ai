"""
Health check endpoint.
Provides system health and status information.
"""

from flask import Blueprint, jsonify

from app.services.health_service import HealthService
from app.utils.logger import get_logger

health_bp = Blueprint("health", __name__)
logger = get_logger("atlus.api.v1.health")


@health_bp.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    
    Response:
        {
            "status": "healthy",
            "service": "atlus-api",
            "version": "1.0.0",
            "timestamp": "ISO 8601"
        }
    """
    logger.debug("Health check requested")
    return jsonify(HealthService.get_health_status()), 200

