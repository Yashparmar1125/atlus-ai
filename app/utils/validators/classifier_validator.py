"""
Validator for intent classifier output.
"""

class ClassifierValidationError(Exception):
    pass


def validate_classifier(data: dict) -> dict:
    """
    Validate classifier output.
    
    Args:
        data: Classifier response dictionary
        
    Returns:
        Validated dictionary
        
    Raises:
        ClassifierValidationError: If validation fails
    """
    if not isinstance(data, dict):
        raise ClassifierValidationError("Classifier output must be a JSON object")
    
    # Check required fields
    if "intent_type" not in data:
        raise ClassifierValidationError("Missing 'intent_type' field")
    
    intent_type = data["intent_type"]
    if intent_type not in ["simple", "complex"]:
        raise ClassifierValidationError(
            f"Invalid intent_type: '{intent_type}'. Must be 'simple' or 'complex'"
        )
    
    # Validate confidence if present
    if "confidence" in data:
        confidence = data["confidence"]
        if not isinstance(confidence, (int, float)):
            raise ClassifierValidationError("confidence must be a number")
        if not 0.0 <= confidence <= 1.0:
            raise ClassifierValidationError("confidence must be between 0.0 and 1.0")
    
    return data

