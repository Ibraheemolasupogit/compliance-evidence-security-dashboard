"""Finding data model."""

from typing import Any

from pydantic import BaseModel, Field


class Finding(BaseModel):
    finding_id: str
    source_system: str
    title: str
    severity: str
    category: str
    owner: str
    status: str


class UnifiedFinding(BaseModel):
    finding_id: str
    source_system: str
    source_repo: str
    title: str
    description: str = ""
    resource_type: str = ""
    resource_name: str = ""
    resource_id: str = ""
    category: str
    severity: str
    risk_score: int = Field(ge=0, le=100)
    control_mapping: str = ""
    cis_control: str = ""
    nist_category: str = ""
    iso_domain: str = ""
    evidence: str = ""
    recommendation: str = ""
    remediation_owner: str = ""
    status: str
    created_at: str = ""
    updated_at: str = ""
    due_date: str = ""
    sla_status: str = "not_evaluated"
    evidence_completeness_score: int = Field(default=0, ge=0, le=100)

    def to_dict(self) -> dict[str, Any]:
        """Return a pydantic-version-agnostic dictionary."""
        if hasattr(self, "model_dump"):
            return self.model_dump()
        return self.dict()
