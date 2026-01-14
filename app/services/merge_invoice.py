def merge_invoice(extracted, excel_data):
    return {
        **extracted.model_dump(),
        "payment_status": excel_data.get("Payment Status") if excel_data else None,
        "due_date": excel_data.get("Due Date") if excel_data else None,
        "shipping_reference": excel_data.get("Shipping Ref") if excel_data else None
    }
