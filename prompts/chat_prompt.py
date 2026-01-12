"""
Chat prompt builder for simple interactions.
Uses rules from rules/behavior_rules.py for maintainability.
"""

from rules.behavior_rules import (
    get_brand_identity_rules,
    get_behavior_rules,
    get_interaction_guidelines,
    get_restrictions,
    get_memory_usage_instructions
)


def build_simple_prompt(user_message: str):
    """
    Build prompt for simple interactions (greetings, short questions).
    Uses rules from rules/behavior_rules.py.
    """

    return [
        {
            "role": "system",
            "content": (
                "You are ATLUS.\n"
                "ATLUS is a calm, intelligent, and friendly AI assistant.\n"
                "Your responses should sound natural and confident.\n\n"

                f"Brand & identity rules:\n{get_brand_identity_rules()}\n\n"

                f"Behavior rules:\n{get_behavior_rules()}\n\n"

                f"Interaction guidelines:\n{get_interaction_guidelines()}\n\n"

                f"Restrictions:\n{get_restrictions()}\n\n"

                f"Memory usage:\n{get_memory_usage_instructions()}"
            )
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
