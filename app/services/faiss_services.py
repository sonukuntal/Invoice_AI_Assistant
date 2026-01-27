import faiss
import numpy as np
from app.utils import get_embedding
from app.services.invoice_query_service import invoice_to_text

DIMENSION = 768  # nomic-embed-text

index = faiss.IndexFlatL2(DIMENSION)
faiss_metadata = []

def add_invoice_to_faiss(invoice: dict):
    text = invoice_to_text(invoice)
    embedding = get_embedding(text)

    vector = np.array([embedding]).astype("float32")
    index.add(vector)

    faiss_metadata.append({
        "invoice_number": invoice["invoice_number"],
        "text": text
    })
def search_faiss(query: str, top_k=3):
    if index.ntotal == 0:
        return []

    query_embedding = get_embedding(query)
    vector = np.array([query_embedding]).astype("float32")

    distances, indices = index.search(vector, top_k)

    results = []
    for idx in indices[0]:
        # IMPORTANT safety checks
        if idx == -1:
            continue
        if idx >= len(faiss_metadata):
            continue

        results.append(faiss_metadata[idx])

    return results
def build_rag_prompt(context_docs, user_question):
    context = "\n\n".join(doc["text"] for doc in context_docs)

    return f"""
You are an Invoice AI Assistant.

Use ONLY the information below to answer.

INVOICE DATA:
{context}

QUESTION:
{user_question}

Answer in clear, natural language.
"""
