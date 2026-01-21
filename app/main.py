from anyio import Path
from app.services.excel_loader_service import load_invoice_excel
from app.services.excel_agent_service import execute_excel_query, llm_excel_query_agent
from app.services.final_invoice import build_final_invoice_output
from app.services.detectpdf_service import is_text_pdf
from app.services.extraction_ocr_service import extract_text_ocr
from app.services.extraction_simple_service import extract_text_pdfplumber
from app.services.extraction_invoice_service import extract_invoice_data_llm
from app.db.database import init_db, save_invoice
from datetime import date
from app.utils.logger import get_logger
from app.services.invoice_llm_service import ask_invoice_question

logger = get_logger(__name__)

def process_invoice(pdf_path: str, Excel_PATH: str):
    logger.info("Extracting text...")
    if is_text_pdf(pdf_path):
        text= extract_text_pdfplumber(pdf_path)
    else:
        text= extract_text_ocr(pdf_path)
    logger.info("Extracted text: %s", text)
    logger.info("Extracting invoice data using LLM...")
    invoice_data = extract_invoice_data_llm(text)
    logger.info("Enriching invoice...")
    logger.info("Loading invoice Excel data...")
    excel_df = load_invoice_excel(Excel_PATH)
    logger.info("Querying Excel data with LLM agent...")
    agent_plan = llm_excel_query_agent(invoice_data, excel_df)
    logger.info("Executing Excel query...")
    excel_data = execute_excel_query(agent_plan, excel_df)

    logger.info("Merging invoice data...")
    pdf_name = Path(pdf_path).name if pdf_path else None
    excel_name = Path(Excel_PATH).name if Excel_PATH else None
    final_invoice = build_final_invoice_output(invoice_data, excel_data, pdf_name, excel_name)   

    init_db()
    logger.info("Database initialized successfully") 
    logger.info("Saving invoice to database...")
    save_invoice(final_invoice)
    logger.info("Invoice processed successfully")
    return final_invoice

if __name__ == "__main__":
    logger.info("Starting invoice processing...")