"""Control data model."""

from pydantic import BaseModel


class Control(BaseModel):
    control_id: str
    control_name: str
    framework: str
