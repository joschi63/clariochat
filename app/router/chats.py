from fastapi import APIRouter, Depends, HTTPException
from ..database.models import Chat, User, ChatUser
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

    chat_user = ChatUser(
        chat_id=new_chat.id,
        user_id=current_user.id,
        role="admin"  
    ) #type: ignore
    
    session.add(chat_user)
    session.commit()
    return new_chat

@router.get("/get/{chat_id}", response_model=ChatResponse)
def read_chat(chat_id: int, session: SessionDep):
    
    db_chat = session.get(Chat, chat_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return db_chat