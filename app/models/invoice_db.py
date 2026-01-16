from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Invoice(Base):
    __tablename__ = "invoices"
    def __init__(self, text):
        self.text = text

    id = Column(Integer, primary_key=True)
    invoice_number = Column(String, unique=True, index=True)
    vendor_name = Column(String)
    customer_name = Column(String)
    invoice_date = Column(Date)
    total_amount = Column(Float)
    risk_score = Column(String)
    payment_status = Column(String)
    due_date = Column(Date)
    shipping_reference = Column(String)
    vendor_category = Column(String)
    currency = Column(String, default="INR")
    status = Column(String, default="NEW")
    
