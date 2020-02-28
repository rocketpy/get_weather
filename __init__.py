from flask import Flask, Blueprint,  render_template, request, current_app
from flask_sqlalchemy import SQLAlchemy
from .main.main import main as main_blueprint
from .auth.auth import auth as auth_blueprint
from .models import User, UserPost
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, InputRequired, Length
from get_weather.weather import db
from get_weather.models import User, UserPost


app = Flask(__name__)
admin = Admin(app)

# app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@app.route('/add', methods=['POST'])
@login_required
def addpost():
    name = request.form['name']
    email = request.form['email']
    title = request.form['title']
    message = request.form['message']

    post = UserPost(name=name, email=email, title=title, message=message)

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    surname = request.form.get('surname')
    sex = request.form.get('sex')
    email = request.form.get('email')
    birthday = request.form.get('birthday')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()  # this returns if email already exists in database

    if user:  # redirect back to signup page
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user
    new_user = User(name=name, surname=surname, sex=sex, email=email, birthday=birthday,
                    password=generate_password_hash(password, method='sha256'))

    # adding a new user to db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(message='An email is required !')])
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(max=100, message='Not greater a 100')])


@app.route('/login', methods=['POST'])
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


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(UserPost, db.session))


if __name__ == '__main__':
    app.run(debug=True)
