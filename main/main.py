from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired, InputRequired, Length
from get_weather.models import User, UserPost
from get_weather.weather import db


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


class AddPostForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(message='An email is required !')])
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(max=100, message='Not greater a 100')])


@main.route('/add', methods=['POST'])
@login_required
def addpost():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    post = UserPost(name=name, email=email, message=message)

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

