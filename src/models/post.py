from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from src.psql.db import Base
from .associations import association_table


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    tags = relationship("Tag", secondary=association_table, back_populates="posts")
