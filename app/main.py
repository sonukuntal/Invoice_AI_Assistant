from services.excel_loader_service import load_invoice_excel
from services.excel_agent_service import execute_excel_query, llm_excel_query_agent
from services.merge_invoice import merge_invoice
from config import INVOICE_PDF_DIR, Excel_PATH
from services.detectpdf_service import is_text_pdf
from services.extraction_ocr_service import extract_text_ocr
from services.extraction_simple_service import extract_text_pdfplumber
from services.validation_service import validate_invoice
from services.enrichment_service import enrich_invoice
from services.extraction_invoice_service import extract_invoice_data_llm
from db.database import init_db, save_invoice
from datetime import date
from db.database import init_db, save_invoice


def process_invoice(pdf_path: str):
    print("Extracting text...")
    if is_text_pdf(pdf_path):
        text= extract_text_pdfplumber(pdf_path)
    else:
        text= extract_text_ocr(pdf_path)

    print("Extracting invoice data using LLM...")
    invoice_data = extract_invoice_data_llm(text)

    print("Validating invoice...")
    validation_result = validate_invoice(invoice_data)
    if validation_result.is_valid:
        print("Enriching invoice...")
        enriched_data = enrich_invoice(validation_result.invoice)
        print("Loading invoice Excel data...")
        excel_df = load_invoice_excel(Excel_PATH)
        print("Querying Excel data with LLM agent...")
        agent_plan = llm_excel_query_agent(enriched_data, excel_df)
        print("Executing Excel query...")
        excel_data = execute_excel_query(agent_plan, excel_df)
        print("Merging invoice data...")
        final_invoice = merge_invoice(enriched_data, excel_data)       
        print("Saving invoice to database...")
        save_invoice(final_invoice)
        print("Invoice processed successfully")
        return final_invoice
    
    else:
        print("Invoice invalid:", validation_result.errors)
        return validation_result.invoice

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully")
    result = process_invoice(INVOICE_PDF_DIR)
    print(result)
