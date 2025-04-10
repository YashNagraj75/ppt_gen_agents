from typing import Optional

from pydantic import BaseModel


class PlannerOutput(BaseModel):
    layout: str
    title: str


class Chart(BaseModel):
    type: str
    data: list[dict]
