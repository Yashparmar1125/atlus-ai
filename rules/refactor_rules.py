"""
Rules for refactor stage.
"""


def get_refactor_rules() -> str:
    """Rules for refactoring."""
    return (
        "Rules:\n"
        "- Do NOT restate the entire solution unnecessarily.\n"
        "- Do NOT mention the verifier or verification process.\n"
        "- Do NOT expose internal reasoning instructions.\n"
        "- Only improve or fix the draft where required.\n"
        "- Preserve correct sections as-is."
    )

