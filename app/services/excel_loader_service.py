import pandas as pd

def load_invoice_excel(path: str) -> pd.DataFrame:
    return pd.read_excel(path)
