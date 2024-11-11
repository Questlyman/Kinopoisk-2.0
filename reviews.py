from models import Review, Film
from database import session

def add_review(user_id, film_id, score, com=None):
    if score < 0 or score > 10:
        raise ValueError("Оценка должна быть в пределах от 0 до 10")

    review = Review(user_id=user_id, film_id=film_id, score=score, com=com)
    session.add(review)
    session.commit()

    update_film_rating(film_id)

def edit_review(user_id, film_id, new_score, new_com=None):
    review = session.query(Review).filter_by(user_id=user_id, film_id=film_id).first()
    if not review:
        raise ValueError("Оценка не найдена для данного пользователя и фильма.")

    if new_score < 0 or new_score > 10:
        raise ValueError("Оценка должна быть в пределах от 0 до 10")
    review.score = new_score
    review.com = new_com
    session.commit()

    update_film_rating(film_id)

def delete_review(user_id, film_id):
    review = session.query(Review).filter_by(user_id=user_id, film_id=film_id).first()
    if not review:
        raise ValueError("Оценка не найдена для данного пользователя и фильма.")

    session.delete(review)
    session.commit()

    update_film_rating(film_id)


def update_film_rating(film_id):
    film = session.query(Film).filter_by(id=film_id).first()
    if not film:
        raise ValueError("Фильм не найден.")
    
    reviews = session.query(Review).filter_by(film_id=film_id).all()
    if reviews:
        avg_rating = sum([r.score for r in reviews]) / len(reviews)
        film.rating = round(avg_rating, 1) 
    else:
        film.rating = 0.0 

    session.commit()
