from sqlmodel import SQLModel, Field, Column, text, Relationship
from sqlalchemy import TIMESTAMP
from datetime import datetime

class ChatUser(SQLModel, table=True):
    __tablename__ = "chat_users" #type: ignore
    chat_id: int = Field(foreign_key="chats.id", primary_key=True)
    user_id: int = Field(foreign_key="users.id", primary_key=True)

    role: str = Field(default="member")
    joined_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))


class User(SQLModel, table=True):
    __tablename__ = "users" #type: ignore
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
   # email: str = Field(index=True, nullable=False, unique=True)
    phone_number: str = Field(index=True, nullable=False, unique=True)
    password: str = Field(nullable=False)
    created_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")), default="now()")
    chats: list["Chat"] = Relationship(back_populates="users", link_model=ChatUser)
    
class Chat(SQLModel, table=True):
    __tablename__ = "chats" #type: ignore
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=True)
    type: str = Field(default="dm") # "dm" or "group"
    created_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")), default="now()")
    messages: list["Message"] = Relationship(back_populates="chat")
    users: list["User"] = Relationship(back_populates="chats", link_model=ChatUser)

class Message(SQLModel, table=True):
    __tablename__ = "messages" #type: ignore
    id: int | None = Field(default=None, primary_key=True)
    content: str = Field(nullable=False)
    changed: bool = Field(default=False)
    read: bool = Field(default=False)
    deleted: bool = Field(default=False)

    sender_id: int = Field(foreign_key="users.id", nullable=False)
    chat_id: int = Field(foreign_key="chats.id", nullable=False) #in dms its the receiver
    
    sended_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")), default="now()")
    updated_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"), onupdate=text("now()")), default="now()")

    chat: "Chat" = Relationship(back_populates="messages")