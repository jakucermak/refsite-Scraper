from fastapi import FastAPI
from src.routes import post


app = FastAPI()

app.include_router(post.router, prefix="")


@app.get("/")
def root():
    return {"message": "root"}