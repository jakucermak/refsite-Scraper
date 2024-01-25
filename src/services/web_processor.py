import logging

from sqlalchemy.ext.asyncio import AsyncSession

import src.utils.scraper as scraper
from dependencies.async_iterator import AsyncListIterator
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
        self.dropped_post_ids = []
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
            logger.exception("Exception occurred while {}".format(e))
            self.dropped_post_ids.append(post_id)
            return
        parser = scraper.parse_response(response_text)
        tags = AsyncListIterator(scraper.get_tags(parser))
        q = scraper.retrieve_qa_content(parser, scraper.QASectionType.QUESTION)
        a = scraper.retrieve_qa_content(parser, scraper.QASectionType.ANSWER)

        try:
            post_id = int(post_id)
        except ValueError:
            logger.error("Invalid post id type: {} id content: {}".format(type(post_id), post_id))
        tag_objs = []

        async for tag in tags:
            tag_obj = await create_tag_obj(self.db, tag)
            tag_objs.append(tag_obj)

        post = await create_post(self.db, post_id, q, a)

        try:
            if post is not None:
                await write_tag_and_post(self.db, tag_objs, post)
            else:
                return
        except Exception as e:
            logger.error("Error writing to DB with error {}".format(e))

    async def start_scrape(self):
        while self.__next_page is not None:
            await self.__process_titled_page(self.__next_page)
        self.__current_post_url = "Finished"

    async def get_current_page(self):
        return self.__current_page

    async def get_current_post(self):
        return self.__current_post_url

    async def get_dropped_posts(self) -> AsyncListIterator:
        return AsyncListIterator(self.dropped_post_ids)

    async def retry_post(self, post_id: str):
        await self.__process_detail_page(post_id)
