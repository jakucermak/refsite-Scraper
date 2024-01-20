from __future__ import annotations

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, mapped_column, Session, Mapped

from src.psql.db import Base
from .associations import association_table


class Tag(Base):
    __tablename__ = 'tags'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String())
    posts = relationship('Post', secondary=association_table, back_populates='tags')

    @classmethod
    def get_by_name(cls, db: Session, name) -> Tag | None:
        query = db.query(cls).filter(cls.name == name).first()
        return query
