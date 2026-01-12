"""
Rules for reasoning stage.
"""


def get_reasoning_instructions() -> str:
    """Instructions for reasoning execution."""
    return (
        "Execute the plan step by step. For each step:\n"
        "1. Explain what you're doing\n"
        "2. Show your reasoning\n"
        "3. Provide the solution or implementation\n\n"
        "Generate a comprehensive draft solution following all steps."
    )


def get_memory_context_instruction() -> str:
    """Instruction for using memory context in reasoning."""
    return (
        "Use information from context if provided:\n"
        "- Reference previous decisions and constraints\n"
        "- Continue from any existing task state\n"
        "- Maintain consistency with established facts\n"
        "- Build upon previous work when applicable"
    )

