import logging

from sqlalchemy.ext.asyncio import AsyncSession

import src.utils.scraper as scraper
from dependencies.async_iterator import AsyncListIterator
from src.routes.serializers.posts_serializer import PostSerializer
from src.utils.req import get
from .db_writer import create_post, create_tag_obj, write_tag_and_post

logger = logging.getLogger(__name__)


class WebProcessor:
    __next_page = ''
    __current_page = ''
    __current_post_url = ''
    _instance = None

    @classmethod
    def get_instance(cls, db):
        if cls._instance is None:
            cls._instance = cls(db)
        return cls._instance

    def __init__(self, db: AsyncSession):
        self.dropped_posts = []
        self.db = db

    async def __process_titled_page(self, page_no):
        logger.info(f'Processing page {page_no}')
        self.__current_page = page_no
        try:
            response_text = scraper.scrape(get, page_no).text
        except Exception as e:
            logger.error(f'Error while scraping page {page_no} with exception {e}')
            return
        parser = scraper.parse_response(response_text)
        post_ids = scraper.get_ids(parser)
        self.__next_page = scraper.get_next_page(parser)

        for post_id in post_ids:
            self.__current_post_url = post_id
            await self.__process_detail_page(post_id)

    async def __process_detail_page(self, post_id: str):
        logger.info(f'Processing detail page {post_id}')
        try:
            response_text = scraper.scrape(get, post_id=post_id).text
        except Exception as e:
            logger.exception("Exception occurred while {}".format(repr(e)))
            dropped_post = PostSerializer(post_id=post_id, reason=f"{repr(e)}")
            self.dropped_posts.append(dropped_post)
            return
        parser = scraper.parse_response(response_text)
        tags = AsyncListIterator(scraper.get_tags(parser))
        q = scraper.retrieve_qa_content(parser, scraper.QASectionType.QUESTION)
        date = scraper.get_date_post(parser)
        a = scraper.retrieve_qa_content(parser, scraper.QASectionType.ANSWER)

        if None is q or None is a:
            dropped_post = PostSerializer(post_id=post_id, reason="question or answer is None")
            self.dropped_posts.append(dropped_post)
            return

        try:
            post_id = int(post_id)
        except ValueError:
            logger.error("Invalid post id type: {} id content: {}".format(type(post_id), post_id))
        tag_objs = []

        async for tag in tags:
            tag_obj = await create_tag_obj(self.db, tag)
            tag_objs.append(tag_obj)

        post = await create_post(self.db, post_id, q, a, date)

        try:
            if post is not None:
                await write_tag_and_post(self.db, tag_objs, post)
            else:
                return
        except Exception as e:
            logger.error("Error writing to DB with error {}".format(repr(e)))

    async def start_scrape(self):
        while self.__next_page is not None:
            await self.__process_titled_page(self.__next_page)
        self.__current_post_url = "Finished"

    async def get_current_page(self):
        return self.__current_page

    async def get_current_post(self):
        return self.__current_post_url

    async def get_dropped_posts(self) -> AsyncListIterator:
        return AsyncListIterator(self.dropped_posts)

    async def retry_post(self, post_id: str):
        await self.__process_detail_page(post_id)

    def remove_id_dropped_posts(self, post_id: str):
        try:
            self.dropped_posts.remove(post_id)
        except ValueError as e:
            logger.error("Could not remove post with id {} because of {}".format(post_id, repr(e)))
