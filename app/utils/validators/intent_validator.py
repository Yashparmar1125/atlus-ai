# utils/validators/intent_validator.py

class IntentValidationError(Exception):
    pass


REQUIRED_INTENT_KEYS = {
    "goal": str,
    "constraints": (str, list),
    "expected_output": str,
}


def validate_intent(data: dict) -> dict:
    if not isinstance(data, dict):
        raise IntentValidationError("Intent must be a JSON object")

    for key, expected_type in REQUIRED_INTENT_KEYS.items():
        if key not in data:
            raise IntentValidationError(f"Missing key: {key}")

        if not isinstance(data[key], expected_type):
            raise IntentValidationError(
                f"Invalid type for '{key}': expected {expected_type}"
            )

    return data
