"""JSON export placeholder."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def export_json(records: Any, path: str | Path) -> None:
    """Export records to a pretty-printed JSON file."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(records, indent=2), encoding="utf-8")
