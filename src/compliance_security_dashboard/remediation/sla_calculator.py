"""Minimal SLA calculation helpers."""

from datetime import date, timedelta


def calculate_due_date(observed_at: date, sla_days: int) -> date:
    """Calculate a due date from an observation date and SLA days."""
    return observed_at + timedelta(days=sla_days)
