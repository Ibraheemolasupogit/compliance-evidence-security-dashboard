"""Shared helpers for the offline Streamlit dashboard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

try:
    import streamlit as st
except ModuleNotFoundError:
    st = None

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = PROJECT_ROOT / "reports"


def output_path(filename: str) -> Path:
    """Return an output file path."""
    return OUTPUTS_DIR / filename


def load_csv_output(path: str | Path) -> pd.DataFrame:
    """Load a CSV output, returning an empty dataframe when missing or empty."""
    source_path = Path(path)
    if not source_path.exists() or source_path.stat().st_size == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(source_path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def load_json_output(path: str | Path) -> dict[str, Any] | list[Any]:
    """Load a JSON output, returning an empty dictionary when missing."""
    source_path = Path(path)
    if not source_path.exists() or source_path.stat().st_size == 0:
        return {}
    return json.loads(source_path.read_text(encoding="utf-8"))


def render_missing_output_warning(required_paths: list[Path]) -> bool:
    """Warn when required outputs are missing and return whether all exist."""
    missing = [path for path in required_paths if not path.exists()]
    if not missing:
        return True
    if st is None:
        return False
    missing_list = ", ".join(path.name for path in missing)
    st.warning(
        f"Missing generated output files: {missing_list}. "
        "Run the offline pipeline first."
    )
    return False


def safe_metric_value(value: Any, default: str = "0") -> str:
    """Format a metric value safely for display."""
    if value in (None, ""):
        return default
    if isinstance(value, float):
        return f"{value:.2f}".rstrip("0").rstrip(".")
    return str(value)


def format_percentage(value: Any) -> str:
    """Format a percentage value."""
    try:
        return f"{float(value):.1f}%"
    except (TypeError, ValueError):
        return "0.0%"


def format_risk_score(value: Any) -> str:
    """Format a risk score."""
    try:
        return f"{float(value):.1f}".rstrip("0").rstrip(".")
    except (TypeError, ValueError):
        return "0"


def first_record(frame: pd.DataFrame) -> dict[str, Any]:
    """Return the first dataframe record or an empty dictionary."""
    if frame.empty:
        return {}
    return frame.iloc[0].to_dict()


def apply_sidebar_filters(
    frame: pd.DataFrame,
    filter_columns: list[str],
    search_columns: list[str] | None = None,
) -> pd.DataFrame:
    """Apply sidebar multi-select filters and optional search."""
    filtered = frame.copy()
    if st is None:
        return filtered
    for column in filter_columns:
        if column not in filtered.columns:
            continue
        values = sorted(str(value) for value in filtered[column].dropna().unique())
        selected = st.sidebar.multiselect(column.replace("_", " ").title(), values)
        if selected:
            filtered = filtered[filtered[column].astype(str).isin(selected)]

    if search_columns:
        query = st.sidebar.text_input("Search findings").strip().lower()
        if query:
            mask = pd.Series(False, index=filtered.index)
            for column in search_columns:
                if column in filtered.columns:
                    column_values = filtered[column].fillna("").astype(str)
                    mask = mask | column_values.str.lower().str.contains(
                        query, regex=False
                    )
            filtered = filtered[mask]
    return filtered


def render_bar_chart(
    frame: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color: str | None = None,
) -> None:
    """Render a bar chart if data is available."""
    if frame.empty or x not in frame.columns or y not in frame.columns:
        if st is None:
            return
        st.info(f"No data available for {title.lower()}.")
        return
    try:
        import plotly.express as px
    except ModuleNotFoundError:
        if st is None:
            return
        st.subheader(title)
        st.bar_chart(frame.set_index(x)[y])
        return

    chart = px.bar(frame, x=x, y=y, color=color, title=title)
    chart.update_layout(margin={"l": 10, "r": 10, "t": 50, "b": 10})
    if st is not None:
        st.plotly_chart(chart, width="stretch")


def value_counts_frame(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    """Return value counts as a dataframe for charts."""
    if frame.empty or column not in frame.columns:
        return pd.DataFrame(columns=[column, "finding_count"])
    return (
        frame[column]
        .fillna("Unknown")
        .astype(str)
        .value_counts()
        .rename_axis(column)
        .reset_index(name="finding_count")
    )
