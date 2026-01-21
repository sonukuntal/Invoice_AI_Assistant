import logging
import json
from app.utils.jsonparse import safe_json_parse
from app.utils.llm_client import call_llm

def llm_excel_query_agent(invoice, df):
    prompt = f"""
You are an intelligent data assistant.

You are given:
1. Extracted invoice data
2. Excel column names
3. Sample rows from the Excel file

Your task:
- Decide which Excel row best matches the invoice
- Identify relevant fields to extract

Invoice Data:
{invoice.model_dump()}

Excel Columns:
{list(df.columns)}

Sample Excel Rows:
{df.head(5).to_dict(orient="records")}

Rules:
- Match using Invoice Number, Account Number, or Customer Name
- You must return ONLY valid JSON
- Do NOT include markdown, explanations, or code fences.
- Do NOT explain
- If no match found, return null values

Return JSON:
{{
  "match_strategy": "invoice_number | account_number | customer_name | none",
  "filters": {{
      "column": "value"
  }},
  "fields_to_return": ["All"]
}}
"""
    response = call_llm(system_prompt="Analyze Excel data and extract relevant fields.", user_prompt=prompt)
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
