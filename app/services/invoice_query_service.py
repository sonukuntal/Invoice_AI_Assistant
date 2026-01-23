from app.db.database import SessionLocal
from app.models import Invoice

def fetch_invoice_from_db(intent):
    session = SessionLocal()
    try:
        if intent == "FETCH_ALL_INVOICES":
            return session.query(Invoice).all()

        query = session.query(Invoice)

        results = query.all()
        return results

    finally:
        session.close()
def invoice_to_text(invoice: Invoice) -> str:
    return (
        f"Invoice Number: {invoice.invoice_number}\n"
        f"Customer Name: {invoice.customer_name}\n"
        f"Vendor Name: {invoice.vendor_name}\n"
        f"total_amount: {invoice.total_amount}\n"
        f"product: {invoice.product}\n"
        f"payment_status: {invoice.payment_status}\n"
        f"Processed At: {invoice.processed_at}\n"
    )
