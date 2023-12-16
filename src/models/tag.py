from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.psql.db import Base
from post import association_table

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String())
    posts = relationship('Post',secondary=association_table, back_populates='tags')