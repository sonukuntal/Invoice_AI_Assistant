# Invoice AI Assistant

Small project to extract and enrich invoice data using a mix of PDF parsing and OCR.

## Native dependencies (Windows)

This project uses `pdf2image` (which needs Poppler) and `pytesseract` (which needs Tesseract). See the full step-by-step instructions in `docs/WINDOWS_NATIVE_DEPENDENCIES.md`.

Quick summary:

- Install Python packages into the project's venv:

```powershell
C:/Users/skyuv/Invoice_AI_Assistant/venv/Scripts/python.exe -m pip install --upgrade pip
C:/Users/skyuv/Invoice_AI_Assistant/venv/Scripts/python.exe -m pip install pdf2image pytesseract
```

- Install Poppler and Tesseract per the docs file. After installation, verify these commands work in PowerShell:

```powershell
pdftoppm -v
tesseract --version
```

If `pdftoppm` or `tesseract` are not found, make sure their `bin` folders are added to your PATH (see `docs/WINDOWS_NATIVE_DEPENDENCIES.md`).

## Quick verification

Use the venv Python to check imports:

```powershell
C:/Users/skyuv/Invoice_AI_Assistant/venv/Scripts/python.exe -c "import pdf2image, pytesseract; print('pdf2image ok', hasattr(pdf2image,'convert_from_path')); print('pytesseract ok')"
```

If you want, I can add these checks to a small `scripts/verify_env.py` and a Make/PowerShell task. Tell me which you'd prefer.
