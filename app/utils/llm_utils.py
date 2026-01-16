import json
import re
from app.utils.logger import get_logger

logging = get_logger(__name__)

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
