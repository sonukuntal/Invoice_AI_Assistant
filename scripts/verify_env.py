#!/usr/bin/env python3
"""scripts/verify_env.py

Quick verifier for the project environment. Checks:
 - pdf2image import and presence of convert_from_path
 - pytesseract import
 - native executables: pdftoppm and tesseract on PATH

Exits with code 0 if all checks pass, non-zero otherwise.
"""
import sys
import shutil
import subprocess


def check_python_packages():
    results = []
    try:
        import pdf2image
        has_convert = hasattr(pdf2image, 'convert_from_path')
        results.append(('pdf2image', True, getattr(pdf2image, '__file__', None), has_convert))
    except Exception as e:
        results.append(('pdf2image', False, str(e), False))

    try:
        import pytesseract
        results.append(('pytesseract', True, getattr(pytesseract, '__file__', None), True))
    except Exception as e:
        results.append(('pytesseract', False, str(e), False))

    return results


def check_executables(names):
    results = []
    for n in names:
        path = shutil.which(n)
        if path:
            try:
                cp = subprocess.run([n, '--version'], capture_output=True, text=True, timeout=5)
                out = (cp.stdout or cp.stderr or '').strip()
            except Exception as e:
                out = f'error running: {e}'
            results.append((n, True, path, out))
        else:
            results.append((n, False, None, None))
    return results


def main():
    ok = True
    print('Python executable:', sys.executable)

    print('\nChecking Python packages:')
    for name, installed, location, extra in check_python_packages():
        if installed:
            print(f' - {name}: OK, location={location}, extra={extra}')
        else:
            print(f' - {name}: MISSING ({location})')
            ok = False

    print('\nChecking native executables:')
    for n, present, path, out in check_executables(['pdftoppm', 'tesseract']):
        if present:
            print(f' - {n}: FOUND at {path}')
            if out:
                first_line = out.splitlines()[0]
                print(f'   -> {first_line}')
        else:
            print(f' - {n}: NOT FOUND on PATH')
            ok = False

    if not ok:
        print('\nOne or more checks failed. See above.')
        sys.exit(2)

    print('\nAll checks passed.')
    sys.exit(0)


if __name__ == '__main__':
    main()
