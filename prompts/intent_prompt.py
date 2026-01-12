# prompts/intent_prompt.py

def build_intent_prompt(user_message: str):
    return [
        {
            "role": "system",
            "content": (
                "You are an intent extraction engine.\n"
                "Do NOT answer the user's question.\n"
                "ONLY extract structured intent as JSON.\n\n"
                "CRITICAL: Return ONLY valid JSON. No explanations, no markdown, no text before or after.\n"
                "The output MUST be parseable JSON."
            )
        },
        {
            "role": "user",
            "content": user_message
        },
        {
            "role": "assistant",
            "content": (
                "REQUIRED JSON structure:\n"
                "{\n"
                '  "goal": "string describing the main objective",\n'
                '  "constraints": "string or array of strings describing limitations/requirements",\n'
                '  "expected_output": "string describing what the final result should be"\n'
                "}\n\n"
                "Example:\n"
                "{\n"
                '  "goal": "Build a web application with authentication",\n'
                '  "constraints": ["Must use Python", "Must be secure"],\n'
                '  "expected_output": "A working web app with user login"\n'
                "}\n\n"
                "Return ONLY the JSON object. No markdown code blocks, no explanations."
            )
        }
    ]
