from sqlalchemy import Table, Column, Integer, ForeignKey
from src.psql.db import Base

association_table = Table('association', Base.metadata,
                          Column('post_id', Integer, ForeignKey('posts.id')),
                          Column('tag_id', Integer, ForeignKey('tags.id')))
