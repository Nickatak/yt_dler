"""At this time, we're not using flask-login.  TODO: implement auth system."""

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.exc import NoResultFound
from werkzeug.security import check_password_hash, generate_password_hash

from . import Base, db_session


class User(UserMixin, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(256), unique=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(
            password,
            method="pbkdf2",
        )

    def __repr__(self):
        return f"User: {self.id}, {self.username}, {self.email}, {self.password}"

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db_session.add(self)
        db_session.commit()

    @staticmethod
    def get_by_id(user_id):
        try:
            return db_session.execute(select(User).where(User.id == user_id)).one()[0]
        except NoResultFound:
            return None

    @staticmethod
    def get_by_email(email):
        try:
            return db_session.execute(select(User).where(User.email == email)).one()[0]
        except NoResultFound:
            return None
