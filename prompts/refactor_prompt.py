# prompts/refactor_prompt.py

def build_refactor_prompt(
    previous_draft: str,
    verifier_feedback: dict
):
    """
    Refines an existing reasoning draft using verifier feedback.
    Does NOT re-plan or restart reasoning.
    """

    issues = verifier_feedback.get("issues", [])
    fixes = verifier_feedback.get("suggested_fixes", [])

    return [
        {
            "role": "system",
            "content": (
                "You are a refinement reasoning engine.\n"
                "You are given a draft solution and verifier feedback.\n\n"
                "Rules:\n"
                "- Do NOT restate the entire solution unnecessarily.\n"
                "- Do NOT mention the verifier or verification process.\n"
                "- Do NOT expose internal reasoning instructions.\n"
                "- Only improve or fix the draft where required.\n"
                "- Preserve correct sections as-is.\n"
            )
        },
        {
            "role": "user",
            "content": (
                f"EXISTING DRAFT:\n"
                f"{previous_draft}\n\n"
                f"IDENTIFIED ISSUES:\n"
                f"{issues}\n\n"
                f"SUGGESTED FIXES:\n"
                f"{fixes}\n\n"
                "Refine the draft to address the issues above.\n"
                "Return the full improved draft."
            )
        }
    ]
