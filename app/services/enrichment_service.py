from models.enrichment_schema import InvoiceEnrichmentResult
from models.invoice_schema import InvoiceSchema

def enrich_invoice(invoice: InvoiceSchema) -> InvoiceEnrichmentResult:
    # Simple rule-based enrichment (replace later with DB/API)
    risk_score = "LOW"

    if invoice.total_amount and invoice.total_amount > 100000:
        risk_score = "HIGH"

    return InvoiceEnrichmentResult(
        invoice=invoice,
        risk_score=risk_score,
        vendor_category="STANDARD"
    )
