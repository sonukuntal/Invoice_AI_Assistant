from datetime import datetime

def build_final_invoice_output(
    invoice_data,
    excel_data: dict,
    pdf_name: str,
    excel_name: str
):
    return {
        "invoice_number": invoice_data.invoice_number,
        "vendor_name": excel_data.get("Vendor_Name"),
        "customer_name": invoice_data.customer_name,
        "payment_status": excel_data.get("Payment_Status"),
        "product": excel_data.get("Product"),
        "total_amount": invoice_data.total_amount,
        "pdf_name": pdf_name,
        "excel_name": excel_name,
        "processed_at": datetime.utcnow().isoformat(),
    }
    