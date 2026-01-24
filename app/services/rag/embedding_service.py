import ollama

from app.config import EMBEDDING_MODEL_NAME

EMBED_MODEL = EMBEDDING_MODEL_NAME

def get_embedding(text: str) -> list:
    response = ollama.embeddings(
        model=EMBED_MODEL,
        prompt=text
    )
    return response["embedding"]
