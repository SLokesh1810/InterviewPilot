import json
import re


def extract_json(text):
    try:
        return json.loads(text)

    except Exception:
        match = re.search(
            r"\{.*\}",
            text,
            re.DOTALL
        )

        if match:
            return json.loads(match.group())

        raise ValueError("No valid JSON found.")