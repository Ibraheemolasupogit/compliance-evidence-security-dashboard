"""Finding validation helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any

from compliance_security_dashboard.normalization.field_mapper import (
    map_severity,
    map_status,
)

REQUIRED_FINDING_FIELDS = {
    "finding_id",
    "title",
    "resource_type",
    "resource_name",
    "severity",
    "category",
    "risk_score",
    "recommendation",
}

VALID_SEVERITIES = {"Critical", "High", "Medium", "Low", "Info"}
VALID_STATUSES = {
    "Open",
    "In Progress",
    "Risk Accepted",
    "Remediated",
    "False Positive",
}


@dataclass
class ValidationIssue:
    finding_id: str
    field: str
    issue: str
    severity: str = "error"
    source: str = ""


@dataclass
class ValidationResult:
    checked_count: int = 0
    issue_count: int = 0
    valid_count: int = 0
    issues: list[ValidationIssue] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready validation result."""
        return {
            "checked_count": self.checked_count,
            "valid_count": self.valid_count,
            "issue_count": self.issue_count,
            "issues": [asdict(issue) for issue in self.issues],
        }


def validate_required_fields(finding: dict[str, object]) -> bool:
    """Return True when the finding has the required foundation fields."""
    return not get_missing_required_fields(finding)


def get_missing_required_fields(finding: dict[str, object]) -> list[str]:
    """Return required fields that are missing or blank."""
    return [
        field_name
        for field_name in sorted(REQUIRED_FINDING_FIELDS)
        if finding.get(field_name) in (None, "")
    ]


def is_valid_date(value: object) -> bool:
    """Return True for empty values or ISO date strings."""
    if value in (None, ""):
        return True
    try:
        date.fromisoformat(str(value)[:10])
    except ValueError:
        return False
    return True


def is_valid_risk_score(value: object) -> bool:
    """Return True when risk score is an integer between 0 and 100."""
    try:
        score = int(value)
    except (TypeError, ValueError):
        return False
    return 0 <= score <= 100


def validate_finding(
    finding: dict[str, object],
    source: str = "",
    required_fields: set[str] | None = None,
) -> list[ValidationIssue]:
    """Validate one finding and return structured issues."""
    required = required_fields or REQUIRED_FINDING_FIELDS
    finding_id = str(finding.get("finding_id") or "UNKNOWN")
    issues: list[ValidationIssue] = []

    for field_name in sorted(required):
        if finding.get(field_name) in (None, ""):
            issues.append(
                ValidationIssue(
                    finding_id=finding_id,
                    field=field_name,
                    issue="Missing required field.",
                    source=source,
                )
            )

    severity = finding.get("severity")
    if (
        severity not in (None, "")
        and map_severity(str(severity)) not in VALID_SEVERITIES
    ):
        issues.append(
            ValidationIssue(
                finding_id=finding_id,
                field="severity",
                issue=f"Invalid severity: {severity}",
                source=source,
            )
        )

    status = finding.get("status")
    if status not in (None, "") and map_status(str(status)) not in VALID_STATUSES:
        issues.append(
            ValidationIssue(
                finding_id=finding_id,
                field="status",
                issue=f"Invalid status: {status}",
                source=source,
            )
        )

    risk_score = finding.get("risk_score")
    if risk_score not in (None, "") and not is_valid_risk_score(risk_score):
        issues.append(
            ValidationIssue(
                finding_id=finding_id,
                field="risk_score",
                issue="Risk score must be an integer from 0 to 100.",
                source=source,
            )
        )

    if not is_valid_date(finding.get("due_date")):
        issues.append(
            ValidationIssue(
                finding_id=finding_id,
                field="due_date",
                issue=f"Malformed due_date: {finding.get('due_date')}",
                source=source,
            )
        )

    return issues


def validate_findings(
    findings: list[dict[str, object]],
    source: str = "",
    required_fields: set[str] | None = None,
) -> ValidationResult:
    """Validate many findings and return a structured summary."""
    all_issues = [
        issue
        for finding in findings
        for issue in validate_finding(finding, source, required_fields)
    ]
    checked_count = len(findings)
    invalid_ids = {issue.finding_id for issue in all_issues}
    return ValidationResult(
        checked_count=checked_count,
        valid_count=checked_count - len(invalid_ids),
        issue_count=len(all_issues),
        issues=all_issues,
    )


def merge_validation_results(results: list[ValidationResult]) -> dict[str, Any]:
    """Merge validation results into a portfolio-level summary."""
    checked_count = sum(result.checked_count for result in results)
    issues = [issue for result in results for issue in result.issues]
    invalid_ids = {issue.finding_id for issue in issues}
    return {
        "checked_count": checked_count,
        "valid_count": checked_count - len(invalid_ids),
        "issue_count": len(issues),
        "issues": [asdict(issue) for issue in issues],
    }
