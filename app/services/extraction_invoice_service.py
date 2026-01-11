import json
import ollama
import logging
from config import LLM_MODEL_NAME


def _empty_invoice():
    return {
        "invoice_number": None,
        "account_number": None,
        "customer_name": None,
        "invoice_date": None,
        "total_amount": None,
        "currency": None,
    }


def extract_invoice_data_llm(text: str) -> dict:
    prompt = f"""
You are an invoice extraction engine.

Extract the following fields from the invoice text below:

- invoice_number
- account_number
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
  "account_number": string | null,
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
            return json.loads(content)
        except json.JSONDecodeError:
            logging.warning("LLM did not return valid JSON; falling back to empty invoice")
            return _empty_invoice()

    except Exception as e:
        # Common cause: ollama daemon not running or model not available.
        logging.warning("ollama call failed (%s). Returning empty invoice. To use Ollama, run the Ollama daemon and ensure model 'qwen2.5:1.5b' is installed.", e)
        return _empty_invoice()
