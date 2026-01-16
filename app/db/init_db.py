import sqlite3
from app.config import DB_PATH
from app.utils import get_logger

logger = get_logger(__name__)
Database_Path = DB_PATH

conn = sqlite3.connect(Database_Path)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT,
    vendor_name TEXT,
    customer_name TEXT,
    invoice_date TEXT,
    total_amount REAL,
    payment_status TEXT,
    due_date TEXT,
    shipping_reference TEXT,
    vendor_category TEXT,
    currency TEXT,
    status TEXT,
    is_duplicate BOOLEAN,
    risk_score TEXT,
    raw_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

logger.info("Invoice database initialized")
