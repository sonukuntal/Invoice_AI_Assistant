from pydantic import BaseModel
from models.invoice_schema import InvoiceSchema

class InvoiceValidationResult(BaseModel):
    invoice: InvoiceSchema
    is_valid: bool
    errors: list[str] = []
