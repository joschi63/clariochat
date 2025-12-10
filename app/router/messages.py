from fastapi import APIRouter, Depends, HTTPException
from ..database.models import Chat, User, Message
from ..database.database import SessionDep
from ..security.token_managing import get_current_user
from ..schemas.message_schema import MessageCreate, MessageResponse

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/create/{id}", response_model=MessageResponse)
def create_message(id: int, message: MessageCreate, session: SessionDep, current_user: User = Depends(get_current_user)):
    if not current_user or not current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if not id:
        raise HTTPException(status_code=400, detail="chat_id is required")

    new_message = Message(**message.model_dump(), sender_id=current_user.id, chat_id=id)
    session.add(new_message)
    session.commit()
    session.refresh(new_message)
    return new_message