from typing import Dict, Optional

from pydantic import BaseModel


class PubSubMessage(BaseModel):
    data: str  # base64-encoded string
    attributes: Optional[Dict[str, str]]
    messageId: Optional[str]
    publishTime: Optional[str]


class PubSubPush(BaseModel):
    message: PubSubMessage
    subscription: str
