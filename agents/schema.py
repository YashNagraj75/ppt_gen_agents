import enum

from pydantic import BaseModel


class SlideLayout(enum.Enum):
    TITLE_SLIDE = "titleSlide"
    CONTENT_FULL = "contentFull"
    CONTENT_TWO_COL = "contentTwoCol"
    CONTENT_THREE_COL = "contentThreeCol"
    CONTENT_FOUR_COL = "contentFourCol"
    CONTENT_WITH_MEDIA_RIGHT = "contentWithMediaRight"
    CONTENT_WITH_MEDIA_LEFT = "contentWithMediaLeft"
    IMAGE_WITH_CAPTION = "imageWithCaption"
    VIDEO_WITH_CAPTION = "videoWithCaption"
    IMAGE_GRID = "imageGrid"
    TABLE = "table"
    CHART_SINGLE = "chartSingle"
    CHART_DUAL = "chartDual"
    DASHBOARD = "dashboard"
    PROCESS_HORIZONTAL = "processHorizontal"
    PROCESS_VERTICAL = "processVertical"
    TIMELINE_HORIZONTAL = "timelineHorizontal"
    TIMELINE_VERTICAL = "timelineVertical"
    CONTACT_INFO = "contactInfo"


class PlannerOutput(BaseModel):
    layout: SlideLayout
    title: str


class Chart(BaseModel):
    type: str
    data: list[dict]
