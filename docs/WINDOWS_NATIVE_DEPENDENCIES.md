# Windows native dependencies: Poppler and Tesseract

This short guide explains how to install the native binaries that `pdf2image` and `pytesseract` rely on when running on Windows. It includes manual download instructions and PowerShell commands to add the binaries to your PATH.

## Why
- `pdf2image` uses Poppler's `pdftoppm`/`pdftocairo` to convert PDF pages to images.
- `pytesseract` is a Python wrapper around the Tesseract OCR executable (`tesseract.exe`).

Both executables must be installed and available on your PATH for conversion and OCR to work.

## Option A — Use winget (if available)
1. Check winget is present:

```powershell
winget --version
```

2. Search and install (IDs may vary; run `winget search <name>` first):

```powershell
winget search poppler
winget install <poppler-id>
winget search tesseract
winget install <tesseract-id>
```

## Option B — Manual install (recommended if winget/Chocolatey not present)

### 1) Poppler for Windows
1. Download a Poppler Windows release (example):
   - GitHub releases: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract the ZIP to a permanent location, for example:

```
C:\Program Files\poppler-24.08.0\Library\bin
```

3. Add the Poppler `bin` folder to your user PATH for the current session (adjust the path to match where you extracted Poppler):

```powershell
$popplerBin = 'C:\Program Files\poppler-24.08.0\Library\bin'  # adjust to your extracted path
$env:Path = "$popplerBin;" + $env:Path
```

4. Make the change permanent (per-user PATH):

```powershell
$popplerBin = 'C:\Program Files\poppler-24.08.0\Library\bin'  # adjust as needed
$old = [Environment]::GetEnvironmentVariable('Path','User')
$new = "$popplerBin;" + $old
[Environment]::SetEnvironmentVariable('Path',$new,'User')
```

5. Verify Poppler is available:

```powershell
pdftoppm -v
```

### 2) Tesseract OCR
1. Download the Windows installer (recommended builds):
   - UB Mannheim builds: https://github.com/UB-Mannheim/tesseract/wiki
   - Or official Tesseract releases
2. Run the installer and accept the defaults. Note the installation directory (usually `C:\Program Files\Tesseract-OCR`).
3. Add Tesseract folder to PATH if the installer didn't:

```powershell
$tessPath = 'C:\Program Files\Tesseract-OCR'  # adjust if different
$env:Path = "$tessPath;" + $env:Path
[Environment]::SetEnvironmentVariable('Path', $env:Path, 'User')
```

4. Verify the installation:

```powershell
tesseract --version
```

## Quick Python checks (use your venv python)
Replace the python path below with your virtualenv's python if needed.

```powershell
# verify pdf2image import and convert function
C:/Users/skyuv/Invoice_AI_Assistant/venv/Scripts/python.exe -c "import pdf2image; print('pdf2image ok', hasattr(pdf2image,'convert_from_path'))"

# verify pytesseract import
C:/Users/skyuv/Invoice_AI_Assistant/venv/Scripts/python.exe -c "import pytesseract; print('pytesseract ok')"

# verify native binaries
pdftoppm -v
tesseract --version
```

## Notes & troubleshooting
- After updating the user PATH you may need to restart your editor/terminal for changes to take effect.
- If `pdf2image.convert_from_path` raises an error about the executable not found, confirm `pdftoppm` is on PATH.
- If `pytesseract` can't find `tesseract.exe`, either add it to PATH or set `pytesseract.pytesseract.tesseract_cmd = r"C:\Path\to\tesseract.exe"` in your code.
- On Windows, prefer 64-bit builds of Poppler/Tesseract that match your Python/OS architecture.

If you'd like, I can add these steps to the project `README.md` instead or create a short `CONTRIBUTING.md` with this snippet. Let me know where you'd like it committed.
