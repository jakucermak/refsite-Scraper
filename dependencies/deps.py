import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.psql.db import AsyncSession
from src.services.web_processor import WebProcessor

logger = logging.getLogger(__name__)


async def get_db() -> AsyncSession:
    db = AsyncSession()
    try:
        logger.info("Creating database tables session")
        yield db
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info("Closing db")
        await db.close()


def get_webprocessor(db=Depends(get_db)) -> WebProcessor:
    return WebProcessor.get_instance(db)
