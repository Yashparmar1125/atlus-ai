"""
Writer prompt builder.
Uses rules from rules/writer_rules.py.
"""

from rules.writer_rules import get_writer_rules


def build_writer_prompt(draft: str, feedback: str | None = None):
    """
    Builds the final user-facing prompt.
    Converts internal draft + verifier feedback into clean output.
    """

    return [
        {
            "role": "system",
            "content": (
                "You are a professional technical writer.\n"
                "Your task is to produce a clear, concise, and well-structured response for the user.\n\n"
                f"{get_writer_rules()}"
            )
        },
        {
            "role": "user",
            "content": (
                f"Draft content:\n{draft}\n\n"
                f"Verifier feedback (if any):\n{feedback or 'None'}\n\n"
                "Rewrite the draft into a polished final response."
            )
        }
    ]
