"""Remediation data model."""

from pydantic import BaseModel


class RemediationItem(BaseModel):
    finding_id: str
    owner: str
    status: str
    sla_status: str
