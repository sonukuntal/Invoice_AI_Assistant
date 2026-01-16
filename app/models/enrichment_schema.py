from pydantic import BaseModel
from app.models.invoice_schema import InvoiceSchema

class InvoiceEnrichmentResult(BaseModel):
    invoice: InvoiceSchema
    risk_score: str
    vendor_category: str | None = None
