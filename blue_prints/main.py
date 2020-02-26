from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms.validators import DataRequired
from get_weather.weather import db
from get_weather.models import UserPost
from datetime import datetime


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/add', methods=['POST'])
@login_required
def addpost():
    name = request.form['name']
    email = request.form['email']
    title = request.form['title']
    #date_posted = request.form['date_posted']
    message = request.form['message']

    post = UserPost(name=name, email=email, title=title, message=message)
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

