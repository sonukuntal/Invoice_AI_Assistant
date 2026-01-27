import re
from typing import Optional

def invoice_to_id(invoice_number: Optional[str]) -> Optional[int]:
    try:
        if not invoice_number:
            return None

        # Extract digits safely (supports INV-1001, INV1001, 1001)
        match = re.search(r"\d+", invoice_number)
        if not match:
            return None

        return int(match.group())
    except Exception:
        return None
