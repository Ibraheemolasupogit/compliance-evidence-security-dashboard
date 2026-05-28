"""Remediation data model."""

from pydantic import BaseModel


class RemediationItem(BaseModel):
    finding_id: str
    title: str = ""
    remediation_owner: str
    severity: str
    risk_score: int
    status: str
    due_date: str = ""
    sla_status: str
    recommendation: str = ""
    evidence_completeness_score: int = 0


class RemediationOwnerSummary(BaseModel):
    remediation_owner: str
    total_findings: int
    open_findings: int
    overdue_findings: int
    due_soon_findings: int
    high_or_critical_findings: int
    average_risk_score: float
    average_evidence_completeness_score: float
    status: str
    sla_status: str
