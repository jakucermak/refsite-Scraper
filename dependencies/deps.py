import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.psql.db import AsyncSession
from src.services.web_processor import WebProcessor

logger = logging.getLogger(__name__)


class IgnoreSpecificLogFilter(logging.Filter):
    def filter(self, record):
        # Seznam zpráv k ignorování
        messages_to_ignore = [
            "Error while receiving a control message (SocketClosed): empty socket content",
            "Error while receiving a control message (SocketClosed): received exception \"peek of closed file\""
        ]

        # Vrátí False, pokud zpráva obsahuje některou z ignorovaných zpráv
        return not any(message in record.getMessage() for message in messages_to_ignore)


async def get_db() -> AsyncSession:
    db = AsyncSession()
    try:
        logger.info("Creating database tables session")
        yield db
    except Exception as e:
        logger.exception(repr(e))
    finally:
        logger.info("Closing db")
        await db.close()


def get_webprocessor(db=Depends(get_db)) -> WebProcessor:
    return WebProcessor.get_instance(db)
