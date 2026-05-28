from datetime import date

from compliance_security_dashboard.remediation.sla_calculator import (
    calculate_due_date,
    calculate_sla_status,
)


def test_calculate_due_date():
    assert calculate_due_date(date(2026, 5, 1), 7) == date(2026, 5, 8)


def test_sla_status_closed():
    assert (
        calculate_sla_status("2026-05-20", "Remediated", today=date(2026, 5, 28))
        == "Closed"
    )
    assert (
        calculate_sla_status("2026-05-20", "False Positive", today=date(2026, 5, 28))
        == "Closed"
    )


def test_sla_status_no_due_date():
    assert calculate_sla_status("", "Open", today=date(2026, 5, 28)) == "No Due Date"


def test_sla_status_overdue():
    assert (
        calculate_sla_status("2026-05-27", "Open", today=date(2026, 5, 28)) == "Overdue"
    )


def test_sla_status_due_soon():
    assert (
        calculate_sla_status("2026-06-04", "Open", today=date(2026, 5, 28))
        == "Due Soon"
    )


def test_sla_status_within_sla():
    assert (
        calculate_sla_status("2026-06-10", "Open", today=date(2026, 5, 28))
        == "Within SLA"
    )
