from fastapi import APIRouter, Depends, HTTPException
from ..database.models import Chat, User
from ..database.database import SessionDep
from ..security.token_managing import get_current_user
from ..schemas.chat_schema import ChatCreate, ChatResponse

router = APIRouter(prefix="/chats", tags=["chats"])

@router.post("/create", response_model=ChatResponse)
def create_chat(chat_create: ChatCreate, session: SessionDep, current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    new_chat = Chat.model_validate(chat_create)
    session.add(new_chat)
    session.commit()
    session.refresh(new_chat)
    return new_chat