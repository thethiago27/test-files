import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def db_session(database_url: str = None) -> sessionmaker:
    if database_url is None:
        logging.error("Database URL not provided")

    engine = create_engine(database_url)
    session_factory = sessionmaker(bind=engine)

    return session_factory

