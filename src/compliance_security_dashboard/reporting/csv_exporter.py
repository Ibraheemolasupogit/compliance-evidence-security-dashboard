"""CSV export placeholder."""

from pathlib import Path

import pandas as pd


def export_csv(frame: pd.DataFrame, path: str | Path) -> None:
    """Export a DataFrame to CSV."""
    frame.to_csv(path, index=False)
