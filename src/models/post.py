from __future__ import annotations

import datetime
import logging
from typing import List

from sqlalchemy import Column, String, DateTime, select, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship, mapped_column

from src.psql.db import Base
from .associations import association_table
from .tag import Tag

logger = logging.getLogger(__name__)


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    question = Column(String)
    answer = Column(String)
    created_at = Column(Date)
    time_created = Column(DateTime, default=datetime.datetime.utcnow)
    tags: Mapped[List[Tag]] = relationship("Tag", secondary=association_table, back_populates="posts")

    @classmethod
    async def check_for_post_exists(cls, db: AsyncSession, post_id: int) -> bool:
        try:
            result = await db.execute(select(cls).where(cls.id == post_id))
            post = result.scalars().first()

            if post is None:
                return False
            else:
                return True
        except Exception as e:
            logger.exception(e)
