from fastapi import FastAPI
from .database.database import create_db_and_tables
from .router import users, auth, chats, messages, chatuser

create_db_and_tables()

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router, prefix="/users")
app.include_router(chats.router, prefix="/users")
app.include_router(messages.router, prefix="/users/chats")
app.include_router(chatuser.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
