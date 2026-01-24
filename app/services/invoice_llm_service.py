from app.services.query_parser_llm import parse_invoice_question
from app.services.invoice_query_service import fetch_invoice_from_db
from app.services.invoice_answer_llm import generate_invoice_answer
from app.services.invoice_query_service import invoice_to_text

def ask_invoice_question(question: str) -> str:
    parsed = parse_invoice_question(question)
    invoices = fetch_invoice_from_db(parsed["intent"])   
    if not invoices:
        return (
            "I can only answer questions related to the uploaded invoices.\n\n"
            "Please ask something like:\n"
            "- List all invoices\n"
            "- What is the total amount for INV-1001?\n"
            "- Which invoices are unpaid?"
        )

    context = "\n\n".join(invoice_to_text(inv) for inv in invoices)

    return generate_invoice_answer(question, context)
