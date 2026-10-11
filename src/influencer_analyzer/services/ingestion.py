from io import BytesIO

import pandas as pd

from influencer_analyzer.config import REQUIRED_COLUMNS


def read_csv(content: bytes) -> tuple[pd.DataFrame, list[str]]:
    """Validate a complete upload before replacing the current dataset."""
    try:
        data = pd.read_csv(BytesIO(content), dtype=str, encoding="utf-8-sig")
    except (ValueError, UnicodeError, pd.errors.ParserError) as exc:
        raise ValueError(f"Cannot read CSV: {exc}") from exc
    data.columns = data.columns.str.strip().str.lower()
    if data.columns.duplicated().any():
        raise ValueError("Column names must be unique after normalization.")
    missing = set(REQUIRED_COLUMNS) - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    if data.empty:
        raise ValueError("The CSV contains no posts.")
    for column in REQUIRED_COLUMNS:
        data[column] = data[column].str.strip()
        if data[column].isna().any() or data[column].eq("").any():
            raise ValueError(f"Column '{column}' has missing values.")
    for column in ["account_type", "media_type"]:
        data[column] = data[column].str.lower()
    data["follower_count"] = pd.to_numeric(data["follower_count"], errors="coerce")
    counts = data["follower_count"]
    if (counts.isna() | counts.lt(0) | counts.mod(1).ne(0)).any():
        raise ValueError("Follower counts must be non-negative whole numbers.")
    data["follower_count"] = counts.astype("int64")
    cta = pd.to_numeric(data["has_call_to_action"], errors="coerce")
    if not cta.isin([0, 1]).all():
        raise ValueError("has_call_to_action must contain 0 or 1.")
    data["has_call_to_action"] = cta.astype(int)
    for column in ["post_datetime", "post_date"]:
        data[column] = pd.to_datetime(data[column], errors="coerce", utc=True, format="mixed")
        if data[column].isna().any():
            raise ValueError(f"Column '{column}' contains invalid dates.")
    if not data["post_datetime"].dt.normalize().eq(data["post_date"].dt.normalize()).all():
        raise ValueError("post_date must match the date in post_datetime (interpreted as UTC).")
    warnings = []
    duplicates = data.duplicated().sum()
    if duplicates:
        data = data.drop_duplicates().copy()
        warnings.append(f"Removed {duplicates:,} identical duplicate rows.")
    if data["post_id"].duplicated().any():
        raise ValueError("Some post IDs have conflicting rows. Resolve these before uploading.")
    if data.groupby("account_id")["account_type"].nunique().gt(1).any():
        warnings.append("Some accounts have multiple account types. The latest observed type "
                        "is used for account summaries and filtering.")
    return data.reset_index(drop=True), warnings
