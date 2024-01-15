from fastapi import FastAPI
from src.routes import post
from src.psql.db import SessionLocal, engine
from sqlalchemy.orm import Session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

app.include_router(post.router, prefix="")


@app.get("/")
def root():
    return {"message": "root"}