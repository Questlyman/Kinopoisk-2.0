from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from key_secret import secret_key, username, localhost, database, pswd

app = Flask(__name__)
app.secret_key = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{pswd}@{localhost}/{database}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)


def hash_password(password):
    return generate_password_hash(password)


def verify_password(hash, password):
    return check_password_hash(hash, password)


def generate_captcha():
    f_num = randint(0, 30)
    s_num = randint(0, 30)
    action = randint(1, 3)

    if action == 1:
        result = f_num + s_num
        operation = f"{f_num} + {s_num} = "
    elif action == 2:
        result = f_num - s_num
        operation = f"{f_num} - {s_num} = "
    elif action == 3:
        result = f_num * s_num
        operation = f"{f_num} * {s_num} = "

    return operation, str(result)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    fname = data.get('first_name')
    lname = data.get('last_name')
    login = data.get('login')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    password_hash = hash_password(password)
    captcha_question, captcha_answer = generate_captcha()
    session['captcha_answer'] = captcha_answer

    return jsonify({"captcha": captcha_question})


@app.route('/verify_captcha', methods=['POST'])
def verify_captcha():
    data = request.json
    captcha_response = data.get('captcha_response')
    fname = data.get('first_name')
    lname = data.get('last_name')
    login = data.get('login')
    password = data.get('password')

    if captcha_response != session.get('captcha_answer'):
        return jsonify({"error": "Captcha incorrect"}), 400

    new_user = User(first_name=fname, last_name=lname, login=login, password_hash=hash_password(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful"})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    login = data.get('login')
    password = data.get('password')

    user = User.query.filter_by(login=login).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not verify_password(user.password_hash, password):
        return jsonify({"error": "Incorrect password"}), 401

    return jsonify({"message": "Login successful"})


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


