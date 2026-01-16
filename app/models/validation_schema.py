from pydantic import BaseModel
from app.models.invoice_schema import InvoiceSchema

class InvoiceValidationResult(BaseModel):
    invoice: InvoiceSchema
    is_valid: bool
    errors: list[str] = []
