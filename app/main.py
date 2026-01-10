from services.ocr_service import extract_text
from services.extraction_service import extract_invoice_data
from services.validation_service import validate_invoice
from services.enrichment_service import enrich_invoice


def process_invoice(pdf_path: str):
    print("Step 1: Extracting text...")
    text = extract_text(pdf_path)

    print("Step 2: Extracting invoice data...")
    invoice_data = extract_invoice_data(text)

    print("Step 3: Validating invoice...")
    validated_data = validate_invoice(invoice_data)

    print("Step 4: Enriching invoice...")
    enriched_data = enrich_invoice(validated_data)

    print("Invoice processed successfully")
    return enriched_data


if __name__ == "__main__":
    result = process_invoice("data/invoices/sample_invoice_1.pdf")
    print(result)
