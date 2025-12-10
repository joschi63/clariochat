from fastapi import APIRouter, Depends, HTTPException
from ..database.models import Chat, User, ChatUser
from ..database.database import SessionDep
from sqlmodel import Session, select

router = APIRouter(prefix="/chatuser", tags=["chatuser"])

@router.get("/get/user/{id}")
def get_chats_for_user(id: int, session: SessionDep):
    db_user = session.exec(select(ChatUser).where(ChatUser.user_id == id)).all() # type: ignore
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/get/chat/{id}")
def get_users_for_chat(id: int, session: SessionDep):
    db_chat = session.exec(select(ChatUser).where(ChatUser.chat_id == id)).all() # type: ignore
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat