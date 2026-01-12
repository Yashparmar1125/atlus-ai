"""
Rules for verification stage.
"""


def get_verifier_rules() -> str:
    """Rules for verification output."""
    return (
        "Rules:\n"
        "- 'issues' MUST be an array of strings (can be empty [] if no issues found)\n"
        "- 'suggested_fixes' MUST be an array of strings (can be empty [] if no fixes needed)\n"
        "- Both arrays MUST be present, even if empty\n"
        "- Each issue and fix MUST be a clear, actionable string"
    )


def get_verifier_examples() -> str:
    """Examples for verification output."""
    return (
        "Example (with issues):\n"
        "{\n"
        '  "issues": [\n'
        '    "Missing error handling for database connection",\n'
        '    "No validation for user input"\n'
        "  ],\n"
        '  "suggested_fixes": [\n'
        '    "Add try-except blocks around database operations",\n'
        '    "Implement input validation before processing"\n'
        "  ]\n"
        "}\n\n"
        "Example (no issues):\n"
        "{\n"
        '  "issues": [],\n'
        '  "suggested_fixes": []\n'
        "}"
    )

