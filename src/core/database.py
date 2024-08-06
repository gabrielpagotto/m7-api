from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.core.config import config

SQLALCHEMY_DATABASE_URL = f"postgresql://{config.db_user}:{config.db_password}@{config.db_host}/{config.db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from src.core.model import *