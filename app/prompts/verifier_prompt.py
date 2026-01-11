# prompts/verifier_prompt.py

def build_verifier_prompt(draft_answer: str):
    return [
        {
            "role": "system",
            "content": (
                "You are a critical reviewer.\n"
                "Find errors, missing steps, incorrect assumptions, or gaps in logic.\n"
                "Be strict and precise.\n\n"
                "CRITICAL: Return ONLY valid JSON. No explanations, no markdown, no text before or after.\n"
                "The output MUST be parseable JSON."
            )
        },
        {
            "role": "user",
            "content": draft_answer
        },
        {
            "role": "assistant",
            "content": (
                "REQUIRED JSON structure:\n"
                "{\n"
                '  "issues": ["Issue 1", "Issue 2", ...],\n'
                '  "suggested_fixes": ["Fix 1", "Fix 2", ...]\n'
                "}\n\n"
                "Rules:\n"
                "- 'issues' MUST be an array of strings (can be empty [] if no issues found)\n"
                "- 'suggested_fixes' MUST be an array of strings (can be empty [] if no fixes needed)\n"
                "- Both arrays MUST be present, even if empty\n"
                "- Each issue and fix MUST be a clear, actionable string\n\n"
                "Example:\n"
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
                "If no issues found:\n"
                "{\n"
                '  "issues": [],\n'
                '  "suggested_fixes": []\n'
                "}\n\n"
                "Return ONLY the JSON object. No markdown code blocks, no explanations."
            )
        }
    ]
