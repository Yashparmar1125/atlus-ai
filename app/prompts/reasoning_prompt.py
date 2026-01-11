# prompts/reasoning_prompt.py

def build_reasoning_prompt(context: str, plan: list[str]):
    steps = "\n".join(f"- {s}" for s in plan)

    return [
        {
            "role": "system",
            "content": (
                "You are a reasoning engine.\n"
                "Follow the plan strictly and execute each step.\n"
                "Think step by step, showing your reasoning process.\n"
                "Do NOT skip steps.\n"
                "Generate a detailed draft solution based on the plan."
            )
        },
        {
            "role": "user",
            "content": (
                f"Context:\n{context}\n\n"
                f"Plan:\n{steps}\n\n"
                "Execute the plan step by step. For each step:\n"
                "1. Explain what you're doing\n"
                "2. Show your reasoning\n"
                "3. Provide the solution or implementation\n\n"
                "Generate a comprehensive draft solution following all steps."
            )
        }
    ]
