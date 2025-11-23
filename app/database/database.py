from sqlmodel import SQLModel, create_engine, Session, Field
from . import models

postgres_url = f"postgresql+psycopg://postgres:13579@localhost:5432/clariochat"

engine = create_engine(postgres_url, echo=True)

with Session(engine) as session:
    SQLModel.metadata.create_all(engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


