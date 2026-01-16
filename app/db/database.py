from app.utils.date_utils import parse_date
from app.models.invoice_schema import InvoiceSchema
from app.config import DB_PATH
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.invoice_db import Base, Invoice
from app.utils.logger import get_logger

logger = get_logger(__name__)

Database_Path = f"sqlite:///{DB_PATH}"
engine = create_engine(Database_Path, echo=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_invoice(invoice_data: InvoiceSchema) -> Invoice:
    session = SessionLocal()
    logger.info("Saving invoice to database")

    try:
        invoice_dict = (
            invoice_data if isinstance(invoice_data, dict)
            else invoice_data.model_dump()
        )

        base_invoice = invoice_dict.pop("invoice")

        final_data = {**base_invoice, **invoice_dict}

        # Normalize dates
        final_data["invoice_date"] = parse_date(final_data.get("invoice_date"))
        final_data["due_date"] = parse_date(final_data.get("due_date"))

        invoice_number = final_data["invoice_number"]

        # 🔍 Check if invoice already exists
        existing_invoice = (
            session.query(Invoice)
            .filter(Invoice.invoice_number == invoice_number)
            .one_or_none()
        )

        if existing_invoice:
            logger.info(f"Updating existing invoice {invoice_number}")

            for key, value in final_data.items():
                setattr(existing_invoice, key, value)

            invoice = existing_invoice

        else:
            logger.info(f"Inserting new invoice {invoice_number}")
            invoice = Invoice(**final_data)
            session.add(invoice)

        session.commit()
        session.refresh(invoice)
        return invoice

    except Exception:
        session.rollback()
        logger.exception("Database upsert failed")
        raise

    finally:
        session.close()
