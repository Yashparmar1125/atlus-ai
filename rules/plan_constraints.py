"""
Constraints and rules for plan generation.
"""


def get_plan_constraints() -> str:
    """Constraints for plan generation."""
    return (
        "Rules:\n"
        "- The 'plan' key MUST contain an array of strings\n"
        "- Each step MUST be a clear, actionable string\n"
        "- Steps MUST be in execution order\n"
        "- Minimum 2 steps, maximum 3 steps"
    )


def get_plan_example() -> str:
    """Example plan output."""
    return (
        "Example:\n"
        "{\n"
        '  "plan": [\n'
        '    "Set up project structure and dependencies",\n'
        '    "Design database schema",\n'
        '    "Implement authentication endpoints"\n'
        "  ]\n"
        "}"
    )

