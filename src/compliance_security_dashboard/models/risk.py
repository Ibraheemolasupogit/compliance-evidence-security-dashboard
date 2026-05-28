"""Risk score data model."""

from pydantic import BaseModel, Field


class RiskScore(BaseModel):
    finding_id: str
    score: int = Field(ge=0, le=100)
    band: str
