"""SLA calculation helpers."""

from datetime import date, timedelta

CLOSED_STATUSES = {"Remediated", "False Positive"}
SLA_STATUS_CLOSED = "Closed"
SLA_STATUS_OVERDUE = "Overdue"
SLA_STATUS_DUE_SOON = "Due Soon"
SLA_STATUS_WITHIN_SLA = "Within SLA"
SLA_STATUS_NO_DUE_DATE = "No Due Date"


def calculate_due_date(observed_at: date, sla_days: int) -> date:
    """Calculate a due date from an observation date and SLA days."""
    return observed_at + timedelta(days=sla_days)


def calculate_sla_status(
    due_date: str | None,
    status: str,
    severity: str | None = None,
    today: date | None = None,
    due_soon_days: int = 7,
) -> str:
    """Calculate SLA status from due date and remediation status."""
    del severity
    current_date = today or date.today()

    if status in CLOSED_STATUSES:
        return SLA_STATUS_CLOSED

    if due_date in (None, ""):
        return SLA_STATUS_NO_DUE_DATE

    parsed_due_date = parse_due_date(str(due_date))
    if parsed_due_date < current_date:
        return SLA_STATUS_OVERDUE
    if parsed_due_date <= current_date + timedelta(days=due_soon_days):
        return SLA_STATUS_DUE_SOON
    return SLA_STATUS_WITHIN_SLA


def parse_due_date(value: str) -> date:
    """Parse an ISO date string for SLA calculations."""
    return date.fromisoformat(value[:10])
