# utils/validators/plan_validator.py

class PlanValidationError(Exception):
    pass


def validate_plan(plan: list[str]) -> list[str]:
    if not isinstance(plan, list):
        raise PlanValidationError("Plan must be a list")

    if len(plan) == 0:
        raise PlanValidationError("Plan cannot be empty")

    for idx, step in enumerate(plan):
        if not isinstance(step, str):
            raise PlanValidationError(
                f"Plan step {idx} must be a string"
            )

        if len(step.strip()) < 5:
            raise PlanValidationError(
                f"Plan step {idx} is too short or vague"
            )

    return plan
