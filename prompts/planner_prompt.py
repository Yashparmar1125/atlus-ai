"""
Planner prompt builder.
Uses rules from rules/plan_constraints.py and rules/json_schemas.py.
"""

from rules.json_schemas import get_plan_schema, get_json_output_instruction
from rules.plan_constraints import get_plan_constraints, get_plan_example


def build_planner_prompt(intent_json: str):
    """Build prompt for plan generation."""
    return [
        {
            "role": "system",
            "content": (
                "You are a task planning engine.\n"
                "Break the goal into ordered, actionable steps.\n"
                "Do NOT solve the task - only create the plan.\n\n"
                f"{get_json_output_instruction()}"
            )
        },
        {
            "role": "user",
            "content": f"Intent:\n{intent_json}"
        },
        {
            "role": "assistant",
            "content": (
                f"REQUIRED JSON structure:\n{get_plan_schema()}\n\n"
                f"{get_plan_constraints()}\n\n"
                f"{get_plan_example()}\n\n"
                f"{get_json_output_instruction()}"
            )
        }
    ]
