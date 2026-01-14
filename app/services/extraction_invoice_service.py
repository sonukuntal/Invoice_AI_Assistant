import json
import logging
import ollama
from datetime import date,datetime
from utils.date_utils import parse_date
from config import LLM_MODEL_NAME
from models.invoice_schema import InvoiceSchema


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
        response = ollama.chat(
            model=LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": "Extract structured invoice data."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response["message"]["content"]

        try:
            raw_data = json.loads(content)

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
        logging.warning("Ollama call failed: %s", e)
        return _empty_invoice_schema()
