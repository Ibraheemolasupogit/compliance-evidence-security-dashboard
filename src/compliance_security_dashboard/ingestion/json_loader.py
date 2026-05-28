"""JSON loading helpers for offline sample findings."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> list[dict[str, Any]]:
    """Load a JSON array from disk."""
    with Path(path).open(encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("Expected a JSON array of finding records.")
    return data
