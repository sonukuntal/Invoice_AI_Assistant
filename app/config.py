from pathlib import Path

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent


# LLM / AI CONFIG
LLM_MODEL_NAME = "qwen2.5:1.5b"  # tinyllama / phi-3 / mistral
LLM_Host = "http://127.0.0.1:11434"

# RAG / EMBEDDING CONFIG
EMBEDDING_MODEL_NAME = "nomic-embed-text"

#Faiss config
FAISS_INDEX_PATH = BASE_DIR / "data" / "faiss_index.index"
METADATA_STORE_PATH = BASE_DIR / "data" / "metadata_store.json"
DIM_Faiss = 768

# OCR / EXTRACTION SETTINGS
DPI = 300

# LOGGING
LOG_LEVEL = "INFO"
LOG_FILE = BASE_DIR / "logs" / "app.log"
