import json
import re
import logging

def safe_json_parse(text: str):
    if not text:
        return None

    # Remove ```json and ``` wrappers
    cleaned = re.sub(r"```json|```", "", text).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        logging.warning("Invalid JSON from LLM:\n%s", text)
        return None
