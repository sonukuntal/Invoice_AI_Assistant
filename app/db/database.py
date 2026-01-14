from models.invoice_schema import InvoiceSchema
from config import DB_PATH
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.invoice_db import Base, Invoice

Database_Path = f"sqlite:///{DB_PATH}"
engine = create_engine(Database_Path, echo=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_invoice(invoice_data: InvoiceSchema) -> Invoice:
    session = SessionLocal()
    try:
        invoice_dict = (
        invoice_data if isinstance(invoice_data, dict)
        else invoice_data.model_dump())

        # Extract nested invoice fields
        base_invoice = invoice_dict.pop("invoice")

        # Merge all fields
        final_data = {**base_invoice, **invoice_dict}
        invoice = Invoice(**final_data)
        session.add(invoice)
        session.commit()
        session.refresh(invoice)
        return invoice
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()