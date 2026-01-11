from pdf2image import convert_from_path
import pytesseract
from config import DPI

def extract_text_ocr(pdf_path):
    pages = convert_from_path(
        pdf_path,
        dpi=DPI
    )

    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)

    return text
