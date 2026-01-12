"""
JSON schema definitions for structured outputs.
These define the required structure for LLM responses.
"""


def get_intent_schema() -> str:
    """JSON schema for intent extraction."""
    return (
        "{\n"
        '  "goal": "string describing the main objective",\n'
        '  "constraints": "string or array of strings describing limitations/requirements",\n'
        '  "expected_output": "string describing what the final result should be"\n'
        "}"
    )


def get_plan_schema() -> str:
    """JSON schema for plan generation."""
    return (
        "{\n"
        '  "plan": [\n'
        '    "Step 1 description",\n'
        '    "Step 2 description",\n'
        '    "Step 3 description"\n'
        "  ]\n"
        "}"
    )


def get_classifier_schema() -> str:
    """JSON schema for intent classification."""
    return (
        "{\n"
        '  "intent_type": "simple" or "complex",\n'
        '  "confidence": 0.0-1.0,\n'
        '  "reasoning": "brief explanation"\n'
        "}"
    )


def get_verifier_schema() -> str:
    """JSON schema for verification output."""
    return (
        "{\n"
        '  "issues": ["Issue 1", "Issue 2", ...],\n'
        '  "suggested_fixes": ["Fix 1", "Fix 2", ...]\n'
        "}"
    )


def get_json_output_instruction() -> str:
    """Standard instruction for JSON-only output."""
    return (
        "CRITICAL: Return ONLY valid JSON. No explanations, no markdown, no text before or after.\n"
        "The output MUST be parseable JSON.\n"
        "Return ONLY the JSON object. No markdown code blocks, no explanations."
    )

