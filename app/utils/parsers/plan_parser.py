# utils/parsers/plan_parser.py

from app.utils.parsers.json_parser import parse_json


class PlanParseError(Exception):
    pass


def parse_plan(raw_text: str) -> list[str]:
    """
    Parses planner output into a normalized list of steps.
    Supports both detailed objects and string lists.
    """

    data = parse_json(raw_text)

    if "plan" not in data or not isinstance(data["plan"], list):
        raise PlanParseError("Planner output must contain a 'plan' list")

    steps = []

    for item in data["plan"]:
        if isinstance(item, str):
            steps.append(item)

        elif isinstance(item, dict):
            # Accept structured steps
            title = item.get("title")
            description = item.get("description")

            if title and description:
                steps.append(f"{title}: {description}")
            elif title:
                steps.append(title)
            else:
                raise PlanParseError("Invalid plan step object")

        else:
            raise PlanParseError("Plan steps must be strings or objects")

    if not steps:
        raise PlanParseError("Plan cannot be empty")

    return steps
