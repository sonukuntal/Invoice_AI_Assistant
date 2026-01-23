from app.services.query_parser_llm import parse_invoice_question
from app.services.invoice_query_service import fetch_invoice_from_db
from app.services.invoice_answer_llm import generate_invoice_answer
from app.services.invoice_query_service import invoice_to_text

def ask_invoice_question(question: str) -> str:
    parsed = parse_invoice_question(question)
    print(f"Parsed Question: {parsed}")
    

    invoices = fetch_invoice_from_db(parsed["intent"])   
    if not invoices:
        return "⚠️ No invoice found matching your query."

    context = "\n\n".join(invoice_to_text(inv) for inv in invoices)

    return generate_invoice_answer(question, context)
