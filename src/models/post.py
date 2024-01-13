from __future__ import annotations

from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import Mapped

from src.psql.db import Base
from .associations import association_table
from .tag import Tag


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    question = Column(String)
    answer = Column(String)
    tags: Mapped[List[Tag]] = relationship("Tag", secondary=association_table, back_populates="posts")
