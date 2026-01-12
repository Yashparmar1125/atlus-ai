"""
Reasoning prompt builder.
Uses rules from rules/reasoning_rules.py.
"""

from rules.reasoning_rules import get_reasoning_instructions, get_memory_context_instruction


def build_reasoning_prompt(context: str, plan: list[str]):
    """Build prompt for reasoning stage."""
    steps = "\n".join(f"- {s}" for s in plan)

    return [
        {
            "role": "system",
            "content": (
                "You are a reasoning engine.\n"
                "Follow the plan strictly and execute each step.\n"
                "Think step by step, showing your reasoning process.\n"
                "Do NOT skip steps.\n"
                "Generate a detailed draft solution based on the plan.\n\n"
                f"{get_memory_context_instruction()}"
            )
        },
        {
            "role": "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"Plan:\n{steps}\n\n"
                f"{get_reasoning_instructions()}"
            )
        }
    ]
