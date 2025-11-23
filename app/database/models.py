from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users" #type: ignore
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
