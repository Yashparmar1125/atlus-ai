"""
Request validation utilities.
"""

from flask import request
from typing import Dict, Any, Type
from pydantic import BaseModel, ValidationError

from app.api.v1.errors import APIError


def validate_request(schema: Type[BaseModel], flask_request) -> Dict[str, Any]:
    """
    Validate Flask request against Pydantic schema.
    
    Args:
        schema: Pydantic model class
        flask_request: Flask request object
        
    Returns:
        Validated data dictionary
        
    Raises:
        APIError: If validation fails
    """
    # Get JSON data
    if not flask_request.is_json:
        raise APIError(
            "Request must be JSON",
            status_code=400,
            error_code="INVALID_CONTENT_TYPE"
        )
    
    data = flask_request.get_json(silent=True)
    
    if data is None:
        raise APIError(
            "Invalid JSON in request body",
            status_code=400,
            error_code="INVALID_JSON"
        )
    
    # Validate against schema
    try:
        validated = schema(**data)
        return validated.dict()
    except ValidationError as e:
        errors = []
        for error in e.errors():
            field = ".".join(str(x) for x in error["loc"])
            errors.append({
                "field": field,
                "message": error["msg"],
                "type": error["type"]
            })
        
        raise APIError(
            "Validation failed",
            status_code=400,
            error_code="VALIDATION_ERROR",
            details=errors
        )


