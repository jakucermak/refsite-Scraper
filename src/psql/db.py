import logging

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

import src.environment as env

logger = logging.getLogger(__name__)

logger.info("Creating connection string to database")
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(env.POSTGRES_USER,
                                                                       env.POSTGRES_PASSWORD,
                                                                       env.POSTGRES_HOST,
                                                                       env.POSTGRES_PORT,
                                                                       env.POSTGRES_DB)
logger.info("Creating database engine")
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)
logger.info("Creating database session")
AsyncSession = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


metadata = Base.metadata
