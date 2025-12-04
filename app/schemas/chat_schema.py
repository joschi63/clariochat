from pydantic import BaseModel
from datetime import datetime

class ChatBase(BaseModel):
    title: str | None = None
    type: str = "dm"  # "dm" or "group"
    

class ChatCreate(ChatBase):
    user_ids: list[int] = []
