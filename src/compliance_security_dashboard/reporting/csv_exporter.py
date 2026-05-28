"""CSV export placeholder."""

from pathlib import Path

import pandas as pd


def export_csv(
    records: pd.DataFrame | list[dict[str, object]],
    path: str | Path,
) -> None:
    """Export records or a DataFrame to CSV."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    frame = records if isinstance(records, pd.DataFrame) else pd.DataFrame(records)
    frame.to_csv(output_path, index=False)
