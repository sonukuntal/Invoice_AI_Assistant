import json
import ollama
import logging


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
You are an invoice data extraction engine.

Extract the following fields and return ONLY valid JSON.

Fields:
- invoice_number
- account_number
- customer_name
- invoice_date
- total_amount
- currency

Rules:
- Use null if a field is missing
- Do NOT explain anything
- JSON keys must be snake_case

Invoice text:
{text}
"""

    try:
        response = ollama.chat(
            model="qwen2.5:1.5b",
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
        logging.warning("ollama call failed (%s). Returning empty invoice. To use Ollama, run the Ollama daemon and ensure model 'phi3' is installed.", e)
        return _empty_invoice()
