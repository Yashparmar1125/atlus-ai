# utils/parsers/json_parser.py

import json

class JSONParseError(Exception):
    pass


def parse_json(raw_text: str) -> dict:
    """
    Strict JSON parser.
    Removes common markdown wrappers and parses JSON.
    """
    if not raw_text or not isinstance(raw_text, str):
        raise JSONParseError("Empty or non-string JSON output")

    cleaned = raw_text.strip()

    # Remove markdown fences if present
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.replace("json", "", 1).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise JSONParseError(f"Invalid JSON: {e}")
