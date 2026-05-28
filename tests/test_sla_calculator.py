from datetime import date

from compliance_security_dashboard.remediation.sla_calculator import calculate_due_date


def test_calculate_due_date():
    assert calculate_due_date(date(2026, 5, 1), 7) == date(2026, 5, 8)
