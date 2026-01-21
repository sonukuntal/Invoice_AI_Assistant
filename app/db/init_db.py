import sqlite3
from app.config import DB_PATH
from app.utils import get_logger

logger = get_logger(__name__)
Database_Path = DB_PATH

conn = sqlite3.connect(Database_Path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    invoice_number PRIMARY KEY TEXT,
    vendor_name TEXT,
    customer_name TEXT,
    total_amount TEXT,
    product TEXT,
    payment_status TEXT,
    pdf_name TEXT,
    excel_name TEXT,
    processed_at TEXT
)
""")

conn.commit()
conn.close()

logger.info("Invoice database initialized")
