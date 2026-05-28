"""CSV loading helpers for offline reference and output files."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a CSV file from disk."""
    source_path = Path(path)
    if not source_path.exists():
        raise FileNotFoundError(f"CSV input file not found: {source_path}")
    return pd.read_csv(source_path)


def load_csv_records(path: str | Path) -> list[dict[str, object]]:
    """Load CSV rows as dictionaries for source routing."""
    return load_csv(path).to_dict(orient="records")
