# prompts/planner_prompt.py

def build_planner_prompt(intent_json: str):
    return [
        {
            "role": "system",
            "content": (
                "You are a task planning engine.\n"
                "Break the goal into ordered, actionable steps.\n"
                "Do NOT solve the task - only create the plan.\n\n"
                "CRITICAL: Return ONLY valid JSON. No explanations, no markdown, no text before or after.\n"
                "The output MUST be parseable JSON."
            )
        },
        {
            "role": "user",
            "content": f"Intent:\n{intent_json}"
        },
        {
            "role": "assistant",
            "content": (
                "REQUIRED JSON structure:\n"
                "{\n"
                '  "plan": [\n'
                '    "Step 1 description",\n'
                '    "Step 2 description",\n'
                '    "Step 3 description"\n'
                "  ]\n"
                "}\n\n"
                "Rules:\n"
                "- The 'plan' key MUST contain an array of strings\n"
                "- Each step MUST be a clear, actionable string\n"
                "- Steps MUST be in execution order\n"
                "- Minimum 2 steps, maximum 3 steps\n\n"
                "Example:\n"
                "{\n"
                '  "plan": [\n'
                '    "Set up project structure and dependencies",\n'
                '    "Design database schema",\n'
                '    "Implement authentication endpoints",\n'
                '    "Create frontend login interface"\n'
                "  ]\n"
                "}\n\n"
                "Return ONLY the JSON object. No markdown code blocks, no explanations."
            )
        }
    ]
