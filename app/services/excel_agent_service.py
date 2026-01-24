import logging
from app.utils.jsonparse import safe_json_parse
from app.utils.llm_client import call_llm

def llm_excel_query_agent(invoice, df):
    prompt = f"""
You are an information extraction agent.

Given the USER invoice, return a JSON object with ACTUAL VALUES.

RULES:
- Return ONLY JSON
- Do NOT explain the schema
- Do NOT use placeholders like "string | null"
- Use null if value is unknown
- If user asks for all invoices, use match_strategy = "none"

JSON FORMAT:
{{
  "match_strategy": "invoice_number | customer_name | none",
  "filters": {{
    "invoice_number": null,
    "customer_name": null
  }},
  "fields_to_return": ["ALL"]
}}
"""
    response = call_llm(system_prompt=prompt, user_prompt=f"""
Invoice JSON:
{invoice.model_dump_json(indent=2)}
""")
    parsed = safe_json_parse(response)
    if not parsed:
        logging.warning("LLM failed to return valid agent plan. Falling back.")
        return {
            "match_strategy": "none",
            "filters": {},
            "fields_to_return": []
        }
    return parsed

def execute_excel_query(agent_plan, df):
    if not agent_plan or not agent_plan.get("filters"):
        return None

    filtered = df.copy()

    for col, val in agent_plan["filters"].items():
        if col in filtered.columns:
            filtered = filtered[
                filtered[col].astype(str).str.contains(str(val), case=False, na=False)
            ]

    if filtered.empty:
        return None

    return filtered.iloc[0].to_dict()
