from fastapi import APIRouter, Depends, HTTPException
from ..database.models import Chat, User, Message
from ..database.database import SessionDep
from ..security.token_managing import get_current_user
from ..schemas.message_schema import MessageCreate

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/create")
def create_message(message: MessageCreate, session: SessionDep, current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    new_message = Message.model_validate(message)
    session.add(new_message)
    session.commit()
    session.refresh(new_message)
    return new_message