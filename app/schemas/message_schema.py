from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    content: str
    chat_id: int
    sender_id: int

class MessageCreate(MessageBase):
    pass