from services.detectpdf_service import is_text_pdf
from services.extraction_ocr_service import extract_text_ocr
from services.extraction_simple_service import extract_text_pdfplumber
from services.validation_service import validate_invoice
from services.enrichment_service import enrich_invoice
from services.extraction_invoice_service import extract_invoice_data_llm
from db.database import save_invoice


def process_invoice(pdf_path: str):
    print("Extracting text...")
    if is_text_pdf(pdf_path):
        text= extract_text_pdfplumber(pdf_path)
    else:
        text= extract_text_ocr(pdf_path)

    print("Extracting invoice data using LLM...")
    invoice_data = extract_invoice_data_llm(text)

    print("Validating invoice...")
    validated_data = validate_invoice(invoice_data)

    print("Enriching invoice...")
    enriched_data = enrich_invoice(validated_data)

    print("Saving invoice to database...")
    save_invoice(enriched_data)

    print("Invoice processed successfully")
    return enriched_data


if __name__ == "__main__":
    result = process_invoice("data/invoices/sample_ocr.pdf")
    print(result)
