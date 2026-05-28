"""CSV loading helpers for offline reference and output files."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load a CSV file from disk."""
    return pd.read_csv(path)
