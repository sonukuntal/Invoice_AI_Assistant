from app.db.database import SessionLocal
from app.models import Invoice
from app.utils.llm_client import call_llm
from app.utils import get_logger

logger = get_logger(__name__)


def ask_invoice_question(invoice_number: str, question: str) -> str:
    session = SessionLocal()
    try:
        invoice = session.query(Invoice).filter(
            Invoice.invoice_number == invoice_number
        ).first()

        if not invoice:
            return f"Invoice {invoice_number} not found."

        invoice_context = f"""
Invoice Number: {invoice.invoice_number}
Customer: {invoice.customer_name}
Vendor: {invoice.vendor_name}
Invoice Date: {invoice.invoice_date}
Due Date: {invoice.due_date}
Total Amount: {invoice.total_amount}
Currency: {invoice.currency}
Payment Status: {invoice.payment_status}
Risk Score: {invoice.risk_score}
Shipping Ref: {invoice.shipping_reference}
Status: {invoice.status}
"""

        prompt = f"""
You are an invoice assistant.

Invoice details:
{invoice_context}

Question:
{question}

Answer clearly and precisely.
"""

        return call_llm(system_prompt="You are an assistant that answers questions about invoices.", user_prompt=prompt)

    except Exception:
        logger.exception("Invoice LLM query failed")
        return "Error while answering invoice question."
    finally:
        session.close()
