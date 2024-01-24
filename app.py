import logging

from fastapi import FastAPI

from src.routes import post

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(post.router)


@app.get("/")
def root():
    logger.info("Hello World")
    return {"message": "root"}
