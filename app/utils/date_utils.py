from datetime import datetime, date
from typing import Optional

def parse_date(value) -> Optional[date]:
    if value is None:
        return None

    if isinstance(value, date):
        return value

    if isinstance(value, str):
        for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                pass

    raise ValueError(f"Invalid date format: {value}")
