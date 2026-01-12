"""
Refactor prompt builder.
Uses rules from rules/refactor_rules.py.
"""

from rules.refactor_rules import get_refactor_rules


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
                f"{get_refactor_rules()}"
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
