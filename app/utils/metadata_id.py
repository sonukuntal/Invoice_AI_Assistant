def invoice_to_id(invoice_number: str) -> int:
    return int(invoice_number.replace("INV-", ""))
