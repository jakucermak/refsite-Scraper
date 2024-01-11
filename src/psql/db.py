from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import src.environment as env
SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(env.POSTGRES_USER,
                                                               env.POSTGRES_PASSWORD,
                                                               env.POSTGRES_HOST,
                                                               env.POSTGRES_PORT,
                                                               env.POSTGRES_DB)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
metadata = Base.metadata
