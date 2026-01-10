import pytesseract
from pdf2image import convert_from_path

def extract_text_ocr(pdf_path: str) -> str:
    pages = convert_from_path(pdf_path)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text
