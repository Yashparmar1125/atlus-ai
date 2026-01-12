"""
Intent classification prompt.
Classifies user requests to route to appropriate agent.
"""

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
                '  "intent_type": "simple" or "complex",\n'
                '  "confidence": 0.0-1.0,\n'
                '  "reasoning": "brief explanation"\n'
                "}\n\n"
                "Classification Rules:\n"
                "- 'simple': Greetings (hi, hello, hey), simple questions, casual conversation, thanks, goodbye\n"
                "- 'complex': Task requests, implementation requests, planning requests, problem-solving, multi-step tasks\n\n"
                "Examples:\n"
                "Input: 'Hi'\n"
                "Output: {\"intent_type\": \"simple\", \"confidence\": 0.95, \"reasoning\": \"Greeting\"}\n\n"
                "Input: 'Build a web app'\n"
                "Output: {\"intent_type\": \"complex\", \"confidence\": 0.98, \"reasoning\": \"Task requiring planning and implementation\"}\n\n"
                "Return ONLY the JSON object. No markdown code blocks, no explanations."
            )
        }
    ]


