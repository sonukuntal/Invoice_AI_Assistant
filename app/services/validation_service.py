from app.models.validation_schema import InvoiceValidationResult
from app.models.invoice_schema import InvoiceSchema

def validate_invoice(invoice: InvoiceSchema) -> InvoiceValidationResult:
    errors = []

    if not invoice.invoice_number:
        errors.append("Missing invoice_number")

    if not invoice.total_amount or invoice.total_amount <= 0:
        errors.append("Invalid total_amount")

    return InvoiceValidationResult(
        invoice=invoice,
        is_valid=len(errors) == 0,
        errors=errors
    )
