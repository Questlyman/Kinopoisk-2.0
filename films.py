from models import Film
from database import session
import os


def add_film(name, time, year, age_limit, description, genres, rating_imdb):
    film = Film(
        name=name,
        time=time,
        year=year,
        age_limit=age_limit,
        description=description,
        genres=genres,
        rating_imdb=rating_imdb,
        rating=0.0
    )
    session.add(film)
    session.commit()

# ВОЗМОЖНО НЕ РАБОТАЕТ, Я ВРОДЕ ЧТО-ТО МЕНЯЛ, УЖЕ НЕ ПОМНЮ ЧТО СЛОМАЛ
def edit_film(name, new_name=None, new_time=None, new_year=None, new_age=None, new_description=None, new_genres=None, 
              new_rating_imdb=None, new_rating=None):
    film = session.query(Film).filter_by(name=name).first()
    if film:
        if new_name:
            film.name = new_name
        if new_time:
            film.time = new_time
        if new_description:
            film.description = new_description
        if new_genres:
            film.genres = new_genres
        if new_rating_imdb is not None:
            film.rating_imdb = new_rating_imdb
        if new_age is not None:
            film.age_limit = new_age
        if new_year is not None:
            film.year = new_year
        if new_rating is not None:
            film.rating = new_rating
        session.commit()


def delete_film(name, password):
    if password == os.getenv("film_del_password"):
        film = session.query(Film).filter_by(name=name).first()
        if film:
            session.delete(film)
            session.commit()
