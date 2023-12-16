from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from src.psql.db import Base
from tag import Tag

association_table = Table('association', Base.metadata,
                          Column('post_id', Integer, ForeignKey('post.id')),
                          Column('tag_id', Integer, ForeignKey('tag.id'))
                          )


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    tags = relationship("Tag", secondary=association_table, back_populates="posts")
