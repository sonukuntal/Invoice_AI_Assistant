from datetime import datetime, date
from typing import Optional

from app.utils import get_logger

logger = get_logger(__name__)
SUPPORTED_FORMATS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%d/%m/%Y",
    "%d-%m-%Y"
]

def parse_date(value) -> Optional[date]:
    if value is None:
        return None

    if isinstance(value, date):
        return value

    if isinstance(value, str):
        for fmt in SUPPORTED_FORMATS:
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                logger.error(f"Invalid date format: {value}")
        raise ValueError(f"Invalid date format: {value}")

    logger.error(f"Unsupported date type: {type(value)}")
    raise TypeError(f"Invalid date type: {type(value)}")
