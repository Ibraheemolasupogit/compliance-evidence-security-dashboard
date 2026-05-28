"""JSON loading helpers for offline sample findings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> list[dict[str, Any]]:
    """Load findings from a JSON list or a dictionary with a findings key."""
    source_path = Path(path)
    if not source_path.exists():
        raise FileNotFoundError(f"JSON input file not found: {source_path}")

    with source_path.open(encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, dict) and "findings" in data:
        data = data["findings"]

    if not isinstance(data, list):
        raise ValueError(
            f"Unsupported JSON format in {source_path}. Expected a list of findings "
            'or an object with a "findings" list.'
        )

    if not all(isinstance(item, dict) for item in data):
        raise ValueError(
            f"Unsupported JSON records in {source_path}. Expected objects."
        )

    return data
