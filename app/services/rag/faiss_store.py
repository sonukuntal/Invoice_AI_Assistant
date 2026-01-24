import faiss
import numpy as np
import ollama
from typing import List
from app.config import DIM_Faiss
from app.utils import logger

logger = logger.get_logger(__name__)

DIM = DIM_Faiss

# FAISS index
index = faiss.IndexIDMap(faiss.IndexFlatL2(DIM))

# Metadata must be ID → metadata
metadata_store= {}

def get_embedding(text: str) -> np.ndarray:
    response = ollama.embed(
        model="nomic-embed-text",
        input=text
    )
    vector = response["embeddings"][0]
    return np.array(vector, dtype="float32")

def add_document(doc_id: int, text: str, metadata: dict):
    vector = get_embedding(text).reshape(1, -1)
    index.add_with_ids(
        vector,
        np.array([doc_id], dtype=np.int64)
    )
    doc_id=int(doc_id)
    metadata_store[doc_id] = metadata
    logger.info(f"ADDING doc_id={doc_id}")
    logger.info(f"FAISS vectors: {index.ntotal}")
    logger.info(f"Metadata rows: {len(metadata_store)}")

def search(query: str, k: int = 5) -> List[dict]:
    query_embedding = get_embedding(query).reshape(1, -1)
    distances, indices = index.search(query_embedding, k)
    results = []

    for doc_id in indices[0]:
        if doc_id == -1:
            continue

        doc_id = int(doc_id)
        if doc_id not in metadata_store:
            logger.warning(f"Metadata missing for doc_id {doc_id}")
            continue

        results.append(metadata_store[doc_id])

    return results
