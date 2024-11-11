import re
from models import User
from database import session

def validate_email(email):
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if re.match(email_regex, email):
        return True
    return False

def add_user(name, login, password, email):
    if not validate_email(email):
        raise ValueError("Некорректный email адрес")
    
    user = User(name=name, login=login, password=password, email=email)
    session.add(user)
    session.commit()

def edit_user(login, new_name=None, new_email=None):
    user = session.query(User).filter_by(login=login).first()
    if new_name:
        user.name = new_name
    if new_email:
        if validate_email(new_email):
            user.email = new_email
        else:
            raise ValueError("Некорректный email адрес")
    session.commit()

def delete_user(login, password):
    user = session.query(User).filter_by(login=login).first()
    if user and user.password == password:
        session.delete(user)
        session.commit()
    else:
        raise ValueError("Неверный пароль или пользователь не найден")
