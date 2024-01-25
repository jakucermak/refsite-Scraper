import logging

from fastapi import APIRouter, Depends

from dependencies.async_iterator import AsyncListIterator
from dependencies.deps import get_webprocessor
from src.services.web_processor import WebProcessor
from .serializers.posts_serializer import PostsSerializer, PostsModelSerializer

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/posts")
async def get_page_parsed_posts(web_processor: WebProcessor = Depends(get_webprocessor)):
    dropped_ids = [id async for id in await web_processor.get_dropped_posts()]
    current_page = await web_processor.get_current_page()
    current_post = await web_processor.get_current_post()
    post_model = PostsModelSerializer(current_post=current_post, current_page=current_page)

    if len(dropped_ids) == 0:
        return post_model
    post_model.dropped_posts = dropped_ids
    return post_model


@router.get("/start")
async def start_scrape(web_processor: WebProcessor = Depends(get_webprocessor)):
    await web_processor.start_scrape()


@router.post("/posts/")
async def retry_scrape(posts: PostsSerializer, web_processor: WebProcessor = Depends(get_webprocessor)):
    async for dropped_post_id in AsyncListIterator(posts.post_ids):
        await web_processor.retry_post(dropped_post_id)
