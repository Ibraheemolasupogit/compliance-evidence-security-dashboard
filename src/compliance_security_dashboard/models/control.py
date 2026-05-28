"""Control data model."""

from pydantic import BaseModel


class Control(BaseModel):
    control_id: str
    control_name: str
    framework: str
    control_family: str = ""
    cis_control: str = ""
    nist_category: str = ""
    iso_domain: str = ""
    evidence_expectation: str = ""


class CategoryControlMapping(BaseModel):
    source_category: str
    normalized_category: str
    default_control_id: str
    cis_control: str = ""
    nist_category: str = ""
    iso_domain: str = ""
    control_theme: str = ""
