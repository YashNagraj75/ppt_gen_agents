import enum

from pydantic import BaseModel


class SlideLayout(enum.Enum):
    titleSlide = "titleSlide"
    titleContentSlide = "titleContenSlide"
    textLeftMediaRight = "textLeftMediaRight"
    mediaLeftTextRight = "mediaLeftTextRight"
    mediaSlide = "mediaSlide"
    tableSlide = "tableSlide"
    barSlide = "barSlide"


class PlannerOutput(BaseModel):
    layout: SlideLayout
    title: str


class Chart(BaseModel):
    type: str
    data: list[dict]
