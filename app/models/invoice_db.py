from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Invoice(Base):
    __tablename__ = "invoices"

    invoice_number = Column(String, primary_key=True)
    vendor_name = Column(String)
    customer_name = Column(String)
    total_amount = Column(String)
    product = Column(String)
    payment_status = Column(String)
    pdf_name = Column(String)
    excel_name = Column(String)
    processed_at = Column(String)
    
