"""CSV export placeholder."""

from pathlib import Path

import pandas as pd


def export_csv(
    records: pd.DataFrame | dict[str, object] | list[dict[str, object]],
    path: str | Path,
) -> None:
    """Export records or a DataFrame to CSV."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(records, pd.DataFrame):
        frame = records
    elif isinstance(records, dict):
        frame = pd.DataFrame([records])
    else:
        frame = pd.DataFrame(records)
    frame.to_csv(output_path, index=False)
