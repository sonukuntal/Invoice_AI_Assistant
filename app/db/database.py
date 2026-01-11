import sqlite3
import json
from config import DB_PATH

Database_Path = DB_PATH


def save_invoice(invoice: dict):
    conn = sqlite3.connect(Database_Path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO invoices (
            invoice_number,
            vendor_name,
            invoice_date,
            total_amount,
            currency,
            status,
            is_duplicate,
            risk_score,
            raw_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        invoice.get("invoice_number"),
        invoice.get("vendor_name"),
        invoice.get("invoice_date"),
        invoice.get("total_amount"),
        invoice.get("currency"),
        invoice.get("status", "REVIEW"),
        invoice.get("is_duplicate"),
        invoice.get("risk_score"),
        json.dumps(invoice)
    ))

    conn.commit()
    conn.close()
