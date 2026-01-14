import os
from pathlib import Path

# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent

# DATABASE CONFIG
DB_NAME = "invoices.db"
DB_PATH = BASE_DIR / "data" / DB_NAME

# INVOICE FILE STORAGE
INVOICE_PDF_DIR = BASE_DIR / "data" / "invoices" / "sample_invoice_2.pdf"

# LLM / AI CONFIG
LLM_MODEL_NAME = "qwen2.5:1.5b"  # tinyllama / phi-3 / mistral

# OCR / EXTRACTION SETTINGS
DPI = 300

# LOGGING
LOG_LEVEL = "INFO"
LOG_FILE = BASE_DIR / "logs" / "app.log"
