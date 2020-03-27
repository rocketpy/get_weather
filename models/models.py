from get_weather.weather import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    sex = db.Column(db.String(10))
    email = db.Column(db.String(50), unique=True)
    birthday = db.Column(db.DateTime)
    password = db.Column(db.String(50))


class UserPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    message = db.Column(db.Text)
