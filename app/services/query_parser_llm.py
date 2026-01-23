from app.utils.llm_client import call_llm
import json

SYSTEM_PROMPT = """
You are an AI that converts user questions into database queries.

Rules:
- If the question does NOT mention invoice number, customer name, date, or amount,
  return intent = FETCH_ALL_INVOICES
- If filters exist, return intent = FETCH_FILTERED_INVOICES
- Output ONLY valid JSON
"""

def parse_invoice_question(question: str) -> dict:
    response = call_llm(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=question
    )

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "match_strategy": "none",
            "filters": {}
        }
