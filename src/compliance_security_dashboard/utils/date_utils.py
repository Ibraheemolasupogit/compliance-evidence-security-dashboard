"""Date utility helpers."""

from dateutil.parser import isoparse


def parse_date(value: str):
    """Parse an ISO-like date string."""
    return isoparse(value).date()
