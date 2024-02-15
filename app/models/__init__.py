"""Eventually, I'll make this it's own standalone models package that can be imported anywhere for any project."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

load_dotenv()
engine = create_engine(
    os.getenv("SQLALCHEMY_TESTING_URI")
    if os.getenv("FLASK_ENV") == "testing"
    else os.getenv("SQLALCHEMY_DATABASE_URI")
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


Base = declarative_base()
Base.query = db_session.query_property()

from .users import User  # noqa: E402


def create_all():
    Base.metadata.create_all(bind=engine)


def drop_all():
    Base.metadata.drop_all(bind=engine)
