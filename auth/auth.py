from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, InputRequired, Length
from get_weather.weather import db
from get_weather.models import User, UserPost


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()  # this returns if email already exists in database

    if user:  # redirect back to signup page
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # adding a new user to db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(message='An email is required !')])
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(max=100, message='Not greater a 100')])


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))

