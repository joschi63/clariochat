from fastapi import APIRouter, Depends, HTTPException
from ..database.models import Chat, User, ChatUser
from ..database.database import SessionDep
from ..security.token_managing import get_current_user
from ..schemas.chat_schema import ChatCreate, ChatResponse
from sqlmodel import Session, select

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

@router.post("/add/user/{chat_id}/{user_id}")
def add_user_to_chat(chat_id: int, user_id: int, session: SessionDep, current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    chat = session.get(Chat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    chatuser = session.exec(select(ChatUser).where(ChatUser.chat_id == chat_id)).first()
    if not chatuser or chatuser.user_id != current_user.id or chatuser.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden: Only admins can add users to the chat")
    
    chat_user = ChatUser(
        chat_id=chat_id,
        user_id=user_id,
        role="member"  
    ) #type: ignore
    session.add(chat_user)
    session.commit()
    return {"message": "User added to chat successfully"}

@router.get("/get/{chat_id}", response_model=ChatResponse)
def read_chat(chat_id: int, session: SessionDep):
    
    db_chat = session.get(Chat, chat_id)
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    return db_chat