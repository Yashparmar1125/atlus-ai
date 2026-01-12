# app/services/health_service.py

import time

class HealthService:
    @staticmethod
    def get_health_status():
        return {
            "status": "healthy",
            "service": "atlus-api",
            "timestamp": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ",
                time.gmtime()
            )
        }
