"""Finding data model."""

from pydantic import BaseModel


class Finding(BaseModel):
    finding_id: str
    source_system: str
    title: str
    severity: str
    category: str
    owner: str
    status: str
