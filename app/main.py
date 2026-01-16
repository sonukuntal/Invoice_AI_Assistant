from app.services.excel_loader_service import load_invoice_excel
from app.services.excel_agent_service import execute_excel_query, llm_excel_query_agent
from app.services.merge_invoice import merge_invoice
from app.config import INVOICE_PDF_DIR, Excel_PATH
from app.services.detectpdf_service import is_text_pdf
from app.services.extraction_ocr_service import extract_text_ocr
from app.services.extraction_simple_service import extract_text_pdfplumber
from app.services.validation_service import validate_invoice
from app.services.enrichment_service import enrich_invoice
from app.services.extraction_invoice_service import extract_invoice_data_llm
from app.db.database import init_db, save_invoice
from datetime import date
from app.utils.logger import get_logger



def process_invoice(pdf_path: str):
    logger.info("Extracting text...")
    if is_text_pdf(pdf_path):
        text= extract_text_pdfplumber(pdf_path)
    else:
        text= extract_text_ocr(pdf_path)

    logger.info("Extracting invoice data using LLM...")
    invoice_data = extract_invoice_data_llm(text)

    logger.info("Validating invoice...")
    validation_result = validate_invoice(invoice_data)
    if validation_result.is_valid:
        logger.info("Enriching invoice...")
        enriched_data = enrich_invoice(validation_result.invoice)
        logger.info("Loading invoice Excel data...")
        excel_df = load_invoice_excel(Excel_PATH)
        logger.info("Querying Excel data with LLM agent...")
        agent_plan = llm_excel_query_agent(enriched_data, excel_df)
        logger.info("Executing Excel query...")
        excel_data = execute_excel_query(agent_plan, excel_df)
        logger.info("Merging invoice data...")
        final_invoice = merge_invoice(enriched_data, excel_data)       
        logger.info("Saving invoice to database...")
        save_invoice(final_invoice)
        logger.info("Invoice processed successfully")
        return final_invoice
    
    else:
        logger.exception("Invoice invalid:%s", validation_result.errors)
        return validation_result.invoice

if __name__ == "__main__":
    logger = get_logger(__name__)
    init_db()
    logger.info("Database initialized successfully")
    result = process_invoice(INVOICE_PDF_DIR)
    print(result)
