from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    chat_id: int
    sender_id: int

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    changed: bool
    read: bool
    deleted: bool
    sended_at: datetime
    updated_at: datetime

    sender_id: int

    class Config:
        orm_mode = True