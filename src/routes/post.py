import logging

from fastapi import APIRouter, Depends

from dependencies.async_iterator import AsyncListIterator
from dependencies.deps import get_webprocessor
from serializers.posts_serializer import PostsSerializer
from src.services.web_processor import WebProcessor

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/posts")
async def get_page_parsed_posts(web_processor: WebProcessor = Depends(get_webprocessor)):
    return {
        "current_post_parsing": await web_processor.get_current_post(),
        "current_page_parsing": await web_processor.get_current_page(),
        "dropped_ids": [id async for id in await web_processor.get_dropped_posts()]
    }


@router.get("/start")
async def start_scrape(web_processor: WebProcessor = Depends(get_webprocessor)):
    await web_processor.start_scrape()


@router.post("/posts/")
async def retry_scrape(posts: PostsSerializer, web_processor: WebProcessor = Depends(get_webprocessor)):
    async for dropped_post_id in AsyncListIterator(posts.post_ids):
        await web_processor.retry_post(dropped_post_id)
