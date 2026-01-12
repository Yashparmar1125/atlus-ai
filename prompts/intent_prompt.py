"""
Intent extraction prompt.
Uses rules from rules/json_schemas.py.
"""

from rules.json_schemas import get_intent_schema, get_json_output_instruction


def build_intent_prompt(user_message: str):
    """Build prompt for intent extraction."""
    return [
        {
            "role": "system",
            "content": (
                "You are an intent extraction engine.\n"
                "Do NOT answer the user's question.\n"
                "ONLY extract structured intent as JSON.\n\n"
                f"{get_json_output_instruction()}"
            )
        },
        {
            "role": "user",
            "content": user_message
        },
        {
            "role": "assistant",
            "content": (
                f"REQUIRED JSON structure:\n{get_intent_schema()}\n\n"
                "Example:\n"
                "{\n"
                '  "goal": "Build a web application with authentication",\n'
                '  "constraints": ["Must use Python", "Must be secure"],\n'
                '  "expected_output": "A working web app with user login"\n'
                "}\n\n"
                f"{get_json_output_instruction()}"
            )
        }
    ]
