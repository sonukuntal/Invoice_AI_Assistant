from app.services.rag.faiss_store import add_document, search
from app.utils.llm_client import call_llm

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks

def index_invoice(invoice_id, invoice_text, invoice_metadata):
    chunks = chunk_text(invoice_text)

    for i, chunk in enumerate(chunks):
        doc_id = f"{invoice_id}"
        add_document(
            doc_id,
            chunk,
            {
                **invoice_metadata,
                "chunk": chunk
            }
        )

def ask_question(question: str):
    retrieved_docs = search(question)
    if not retrieved_docs:
        return "I couldn't find relevant invoice data."

    context = "\n\n".join(
        f"Invoice {d['invoice_number']}:\n{d['chunk']}"
        for d in retrieved_docs
    )

    prompt = f"""
You are an Invoice AI Assistant.
Answer ONLY using the context.
If not found, say you don't know.

Context:
{context}
"""

    response = call_llm(
        system_prompt=prompt,
        user_prompt=question
    )

    return response
