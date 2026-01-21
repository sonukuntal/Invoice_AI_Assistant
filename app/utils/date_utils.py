from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%d-%m-%Y",
]

def normalize_date_string(value: str) -> str:
    """
    Cleans OCR/LLM date strings
    """
    value = value.strip()

    # Remove labels like "Date:"
    value = re.sub(r"(?i)date\s*[:\-]?\s*", "", value)

    # Normalize all dash variants to ASCII '-'
    value = value.replace("–", "-").replace("—", "-").replace("-", "-")

    return value

def parse_date(value):
    if not value:
        return None

    if hasattr(value, "year"):
        return value  # already date/datetime

    if not isinstance(value, str):
        logger.error(f"Invalid date type: {type(value)} -> {value}")
        return None

    value = normalize_date_string(value)

    for fmt in SUPPORTED_FORMATS:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    logger.error(f"Invalid date format after cleanup: {repr(value)}")
    return None
