from __future__ import annotations

import logging

from sqlalchemy import Column, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.psql.db import Base
from .associations import association_table

logger = logging.getLogger(__name__)


class Tag(Base):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String())
    posts = relationship('Post', secondary=association_table, back_populates='tags')

    @classmethod
    async def get_by_name(cls, db: AsyncSession, name) -> Tag | None:
        try:
            result = await db.execute(select(cls).where(cls.name == name))
            return result.scalars().first()
        except Exception as e:
            logger.error(e)
