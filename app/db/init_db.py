import sqlite3

DB_PATH = "data/invoices.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT,
    vendor_name TEXT,
    invoice_date TEXT,
    total_amount REAL,
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

print("Invoice database initialized")
