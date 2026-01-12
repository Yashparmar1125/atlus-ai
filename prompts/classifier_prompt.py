"""
Intent classification prompt.
Classifies user requests to route to appropriate agent.
Uses rules from rules/classification_rules.py and rules/json_schemas.py.
"""

from rules.json_schemas import get_classifier_schema, get_json_output_instruction
from rules.classification_rules import get_classification_rules, get_simple_examples, get_complex_examples


def build_classifier_prompt(user_message: str):
    """
    Build prompt for intent classification.
    
    Classifies requests into:
    - "simple": Greetings, simple questions, casual conversation
    - "complex": Tasks requiring planning, reasoning, implementation
    """
    return [
        {
            "role": "system",
            "content": (
                "You are an intent classifier.\n"
                "Classify user messages to determine if they need simple response or complex task processing.\n\n"
                "CRITICAL: Default to 'simple' unless the request clearly requires heavy multi-step implementation.\n"
                "Simple conversations, questions, drafts, explanations, and advice requests should be 'simple'.\n"
                "Only classify as 'complex' for heavy implementation/development tasks.\n\n"
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
                f"REQUIRED JSON structure:\n{get_classifier_schema()}\n\n"
                f"{get_classification_rules()}\n\n"
                f"{get_simple_examples()}\n\n"
                f"{get_complex_examples()}\n\n"
                f"{get_json_output_instruction()}"
            )
        }
    ]


