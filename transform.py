# Shared transform logic used by both pipelines.

import pandas as pd

from logger import setup_logger

log = setup_logger(__name__)


def clean_and_enrich(df: pd.DataFrame) -> pd.DataFrame:
    """Clean, validate, and enrich raw MySQL data."""
    n_in = len(df)

    # 1. Normalise column names.
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"[\s\-]+", "_", regex=True)
    )

    # 2. Drop duplicates on primary key if known.
    if "id" in df.columns:
        df = df.drop_duplicates(subset=["id"])
    else:
        df = df.drop_duplicates()

    # 3. Parse date columns.
    date_cols = [c for c in df.columns if "date" in c or "_at" in c]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)

    # 4. Remove rows with null critical fields.
    required = [c for c in ["id", "order_date", "customer_id"] if c in df.columns]
    if required:
        df = df.dropna(subset=required)

    # 5. Type coercions.
    for col in ["quantity", "amount", "unit_price"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 6. Derived columns.
    if {"quantity", "unit_price"}.issubset(df.columns):
        df["total_amount"] = (df["quantity"] * df["unit_price"]).round(2)

    # 7. Filter invalid rows.
    if "quantity" in df.columns:
        df = df[df["quantity"] > 0]
    if "amount" in df.columns:
        df = df[df["amount"] >= 0]

    # 8. Add pipeline metadata.
    df["_etl_loaded_at"] = pd.Timestamp.utcnow()

    dropped = n_in - len(df)
    log.info(f"[TRANSFORM] {len(df):,} rows kept  ({dropped} dropped)")
    return df.reset_index(drop=True)
