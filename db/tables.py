from sqlalchemy import Boolean, Column, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=True)
    is_bot = Column(Boolean, default=False)
    language_code = Column(String(20))


class KnownWords(Base):
    __tablename__ = 'known_words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)
    words = Column(LargeBinary, nullable=False)
