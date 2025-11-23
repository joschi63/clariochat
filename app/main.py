from fastapi import FastAPI
from .database.database import create_db_and_tables

create_db_and_tables()

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}
