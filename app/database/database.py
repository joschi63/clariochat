from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session, Field
from typing import Annotated
from . import models

postgres_url = f"postgresql+psycopg://postgres:13579@localhost:5432/clariochat"

engine = create_engine(postgres_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]

