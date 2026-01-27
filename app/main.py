import json
from anyio import Path
from app.services.excel_loader_service import load_invoice_excel
from app.services.excel_agent_service import execute_excel_query, llm_excel_query_agent
from app.services.final_invoice import build_final_invoice_output
from app.services.detectpdf_service import is_text_pdf
from app.services.extraction_ocr_service import extract_text_ocr
from app.services.extraction_simple_service import extract_text_pdfplumber
from app.services.extraction_invoice_service import extract_invoice_data_llm
from app.services.rag.rag_pipeline import index_invoice
from app.utils.logger import get_logger
from app.utils.metadata_id import invoice_to_id

logger = get_logger(__name__)

def process_invoice(pdf_path: str, Excel_PATH: str,p_name: str, e_name: str):
    logger.info("Extracting text...")
    if is_text_pdf(pdf_path):
        text= extract_text_pdfplumber(pdf_path)
    else:
        text= extract_text_ocr(pdf_path)

    logger.info("Extracting invoice data using LLM...")
    invoice_data = extract_invoice_data_llm(text)
    logger.info("Loading invoice Excel data...")
    excel_df = load_invoice_excel(Excel_PATH)
    logger.info("Querying Excel data with LLM agent...")
    agent_plan = llm_excel_query_agent(invoice_data, excel_df)
    logger.info("Executing Excel query...")
    excel_data = execute_excel_query(agent_plan, excel_df)
    logger.info("Merging invoice data...")
    final_invoice = build_final_invoice_output(invoice_data, excel_data, p_name, e_name)
    logger.info("Invoice processed successfully")
    meta_id = invoice_to_id(final_invoice.get("invoice_number"))
    if(meta_id is not None):
        index_invoice(
        invoice_id=meta_id,
        invoice_text=json.dumps(final_invoice),
        invoice_metadata={
        "invoice_number": final_invoice.get("invoice_number"),
        "customer": final_invoice.get("customer_name"),
        "total": final_invoice.get("total_amount")
    }
    )
    else:
        logger.warning("I couldn't identify a valid invoice number.")

if __name__ == "__main__":
    logger.info("Starting invoice processing...")