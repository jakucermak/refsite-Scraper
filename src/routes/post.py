import logging

from fastapi import APIRouter, Depends

from dependencies.deps import get_webprocessor
from src.services.web_processor import WebProcessor

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/posts")
async def get_page_parsed_posts(web_processor: WebProcessor = Depends(get_webprocessor)):
    return {
        "current_post_parsing": await web_processor.get_current_post(),
        "current_page_parsing": await web_processor.get_current_page(),
    }


@router.get("/start")
async def start_scrape(web_processor: WebProcessor = Depends(get_webprocessor)):
    await web_processor.start_scrape()
