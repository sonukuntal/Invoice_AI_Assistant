from app.utils.llm_client import call_llm

ANSWER_SYSTEM_PROMPT = """
You are an invoice assistant.
Answer the user's question using ONLY the provided invoice data.
If information is missing, say so clearly.
"""

def generate_invoice_answer(question: str, invoice_text: str) -> str:
    prompt = f"""
Invoice Data:
{invoice_text}

User Question:
{question}
"""
    return call_llm(
        system_prompt=ANSWER_SYSTEM_PROMPT,
        user_prompt=prompt
    )
