import json
from app.utils import get_logger
from datetime import date,datetime
from app.utils.date_utils import parse_date
from app.models.invoice_schema import InvoiceSchema
from app.utils.llm_client import call_llm

logging = get_logger(__name__)


def _empty_invoice_schema() -> InvoiceSchema:
    return InvoiceSchema()


def extract_invoice_data_llm(text: str) -> InvoiceSchema:
    prompt = f"""
You are an invoice extraction engine.

Extract the following fields from the invoice text below:

- invoice_number
- customer_name
- invoice_date
- total_amount
- currency

RULES:
1. Return ONLY valid JSON
2. Do NOT add explanations
3. Do NOT use markdown
4. If a field is missing, use null

JSON format:
{{
  "invoice_number": string | null,
  "customer_name": string | null,
  "invoice_date": string | null,
  "total_amount": number | null,
  "currency": string | null
}}

Invoice text:
\"\"\"
{text}
\"\"\"
"""

    try:
        response = call_llm(system_prompt="Extract structured invoice data.", user_prompt=prompt)
        try:
            raw_data = json.loads(response)

            # Convert string date → date object (important)
            if raw_data.get("invoice_date"):
                raw_data["invoice_date"] = parse_date(
                raw_data.get("invoice_date")
                )
                if raw_data.get("due_date"):
                    raw_data["due_date"] = parse_date(
                    raw_data.get("due_date")
                )

            #Return validated schema
            return InvoiceSchema(**raw_data)

        except (json.JSONDecodeError, ValueError) as e:
            logging.warning("Invalid LLM response format: %s", e)
            return _empty_invoice_schema()

    except Exception as e:
        logging.warning(f"Ollama call failed: {e}", exc_info=True)
        return _empty_invoice_schema()
