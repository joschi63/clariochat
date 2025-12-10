from pydantic import BaseModel
from datetime import datetime
from app.schemas.message_schema import MessageResponse

class ChatBase(BaseModel):
    title: str | None = None
    type: str = "dm"  # "dm" or "group"
    

class ChatCreate(ChatBase):
    pass

class ChatResponse(ChatBase):
    id: int
    created_at: datetime
    messages: list[MessageResponse]

    class Config:
        orm_mode = True
