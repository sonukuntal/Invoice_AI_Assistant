from app.db.database import SessionLocal
from app.models import Invoice

def fetch_invoice_by_number(invoice_number: str) -> dict | None:
    session = SessionLocal()
    try:
        invoice = (
            session.query(Invoice)
            .filter(Invoice.invoice_number == invoice_number)
            .one_or_none()
        )

        if not invoice:
            return None

        return {
            "invoice_number": invoice.invoice_number,
            "vendor_name": invoice.vendor_name,
            "customer_name": invoice.customer_name,
            "invoice_date": str(invoice.invoice_date),
            "due_date": str(invoice.due_date),
            "payment_status": invoice.payment_status,
            "total_amount": invoice.total_amount,
            "currency": invoice.currency,
            "risk_score": invoice.risk_score,
            "vendor_category": invoice.vendor_category,
            "shipping_reference": invoice.shipping_reference,
            "status": invoice.status
        }
    finally:
        session.close()
