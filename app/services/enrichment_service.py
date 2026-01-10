def enrich_invoice(invoice: dict) -> dict:
    # Later: DB / API lookup
    invoice["risk_score"] = "LOW"
    return invoice
