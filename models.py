from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Time, DECIMAL, TEXT, ARRAY
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True)

    reviews = relationship("Review", back_populates="user")


class Film(Base):
    __tablename__ = 'films'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    time = Column(Time(0), nullable=False)
    description = Column(TEXT)
    genres = Column(ARRAY(String), nullable=False)
    rating_imdb = Column(DECIMAL(3, 1), nullable=False)
    rating = Column(DECIMAL(3, 1), default=0.0)

    reviews = relationship("Review", back_populates="film")


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    film_id = Column(Integer, ForeignKey('films.id'))
    score = Column(Integer)
    com = Column(Text, nullable=True)

    user = relationship("User", back_populates="reviews")
    film = relationship("Film", back_populates="reviews")
