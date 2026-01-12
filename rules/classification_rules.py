"""
Rules for intent classification.
Defines criteria for simple vs complex requests.
"""


def get_classification_rules() -> str:
    """Rules for classifying user intent. Default to 'simple' unless clearly a heavy task."""
    return (
        "Classification Rules (STRICT - Default to 'simple' unless clearly a heavy task):\n"
        "- 'simple': DEFAULT for most cases - Greetings, questions, casual conversation, explanations, discussions, drafts, messages, requests for information, thanks, goodbye, follow-ups, clarifications\n"
        "- 'complex': ONLY for heavy tasks requiring multi-step execution - Building/creating applications, implementing systems, complex planning with multiple steps, generating code architectures, designing complex systems\n\n"
        "IMPORTANT: When in doubt, classify as 'simple'. Only use 'complex' for clearly heavy implementation/development tasks."
    )


def get_simple_examples() -> str:
    """Examples of simple requests."""
    return (
        "Examples (simple - DEFAULT):\n"
        "Input: 'Hi'\n"
        "Output: {\"intent_type\": \"simple\", \"confidence\": 0.95, \"reasoning\": \"Greeting\"}\n\n"
        "Input: 'How are you?'\n"
        "Output: {\"intent_type\": \"simple\", \"confidence\": 0.90, \"reasoning\": \"Casual question\"}\n\n"
        "Input: 'Draft a message to my team'\n"
        "Output: {\"intent_type\": \"simple\", \"confidence\": 0.85, \"reasoning\": \"Writing/drafting request, not implementation\"}\n\n"
        "Input: 'Explain how authentication works'\n"
        "Output: {\"intent_type\": \"simple\", \"confidence\": 0.90, \"reasoning\": \"Explanation request\"}\n\n"
        "Input: 'What should I do for this task?'\n"
        "Output: {\"intent_type\": \"simple\", \"confidence\": 0.85, \"reasoning\": \"Question/advice request\"}"
    )


def get_complex_examples() -> str:
    """Examples of complex requests (ONLY for heavy implementation tasks)."""
    return (
        "Examples (complex - ONLY heavy implementation tasks):\n"
        "Input: 'Build a complete web application with database and authentication'\n"
        "Output: {\"intent_type\": \"complex\", \"confidence\": 0.98, \"reasoning\": \"Heavy implementation task requiring multi-step execution\"}\n\n"
        "Input: 'Create and implement a full-stack application with frontend, backend, and database'\n"
        "Output: {\"intent_type\": \"complex\", \"confidence\": 0.95, \"reasoning\": \"Complex multi-step implementation\"}\n\n"
        "Input: 'Design and implement a microservices architecture'\n"
        "Output: {\"intent_type\": \"complex\", \"confidence\": 0.95, \"reasoning\": \"Heavy architectural implementation\"}\n\n"
        "NOTE: Single requests like 'draft a message', 'explain X', 'what is Y', 'write a letter' are SIMPLE, not complex."
    )

