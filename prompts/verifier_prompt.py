"""
Verifier prompt builder.
Uses rules from rules/verifier_rules.py and rules/json_schemas.py.
"""

from rules.json_schemas import get_verifier_schema, get_json_output_instruction
from rules.verifier_rules import get_verifier_rules, get_verifier_examples


def build_verifier_prompt(draft_answer: str):
    """Build prompt for verification."""
    return [
        {
            "role": "system",
            "content": (
                "You are a critical reviewer.\n"
                "Find errors, missing steps, incorrect assumptions, or gaps in logic.\n"
                "Be strict and precise.\n\n"
                f"{get_json_output_instruction()}"
            )
        },
        {
            "role": "user",
            "content": draft_answer
        },
        {
            "role": "assistant",
            "content": (
                f"REQUIRED JSON structure:\n{get_verifier_schema()}\n\n"
                f"{get_verifier_rules()}\n\n"
                f"{get_verifier_examples()}\n\n"
                f"{get_json_output_instruction()}"
            )
        }
    ]
