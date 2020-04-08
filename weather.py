#import requests
from flask import Flask
#from bs4 import BeautifulSoup
from flask_admin import Admin
#from flask_wtf import FlaskForm
#from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
#from wtforms import StringField, PasswordField, BooleanField
#from flask_admin.contrib.sqla import ModelView
#from flask_login import login_user, logout_user
#from wtforms.validators import InputRequired, Length
#from flask import render_template, redirect, url_for, request, flash
#from werkzeug.security import generate_password_hash, check_password_hash
#from flask_user import UserMixin, login_required, current_user


app = Flask(__name__)
app.config.from_pyfile('config.py')
admin = Admin(app)
db = SQLAlchemy(app)
db.init_app(app)

"""
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['WTF_CSRF_SECRET_KEY'] = "CSRF_SECRET_KEY"
app.config['CSRF_ENABLED'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
"""


"""
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    sex = db.Column(db.String(6))
    email = db.Column(db.String(255), unique=True)
    birthday = db.Column(db.String(10))
    password = db.Column(db.String(50))
    posts = db.relationship('UserPost', backref='author')


class UserPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(255))
    message = db.Column(db.Text(1000))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
"""
"""
class SignUp(FlaskForm):
    name = StringField('name', validators=[InputRequired(message='An name is required !'),
                                           Length(min=2, max=20)])
    surname = StringField('surname', validators=[InputRequired(message='An surname is required !'),
                                                 Length(min=2, max=20)])
    email = StringField('email', validators=[InputRequired(message='An email is required !'),
                                             Length(min=5, max=255)])
    sex = StringField('sex', validators=[InputRequired(message='Field sex is required !'),
                                         Length(min=4, max=6, message='Not greater a 6 simbols')])
    birthday = StringField('birthday', validators=[InputRequired(message='Field birthday is required !'),
                                                   Length(min=6, max=10, message='Not greater a 6 simbols')])
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(min=5, max=50, message='Not greater a 50')])


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(message='An email is required !'),
                                             Length(min=5, max=255)])
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(min=5, max=50, message='Not greater a 50')])
    remember = BooleanField('remember me')


class AddPostForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(message='An name is required !'),
                                           Length(min=2, max=20, message='It is a wrong length')])
    email = StringField('email', validators=[InputRequired(message='An email is required !'),
                                             Length(min=5, max=255, message='It is a wrong length')])
    message = StringField('message', validators=[InputRequired(message='Text field is required !'),
                                                 Length(min=5, max=1000, message='It is a wrong length')])
"""
"""
# Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@app.route('/signup', methods=['POST', 'GET'])
def signup_post():
    form = SignUp()
    name = request.form.get('name')  # request.form['name']
    surname = request.form.get('surname')
    email = request.form.get('email')
    sex = request.form.get('sex')
    birthday = request.form.get('birthday')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return render_template('login.html', form=form)

    if form.validate_on_submit():
        new_user = User(name=name, surname=surname, email=email, sex=sex, birthday=birthday,
                        password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)  # adding a new user to db
        db.session.commit()
        flash('New user created , login please !')
        return redirect(url_for('login_post', form=form))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login_post():
    form = LoginForm()
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        # flash('Please check your login details and try again !')
        return render_template('login.html', form=form)

    if form.validate_on_submit():
        login_user(user, remember=remember)
        flash('Logged in successfully.')
        return redirect(url_for('add_post', form=form))

    return render_template('login.html', form=form)


@app.route('/weather', methods=['GET', 'POST'])
@login_required
def show_weather():
    night_temperature = []
    day_temperature = []

    def get_html(url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
        r = requests.get(url, headers=headers)
        return r.text

    def get_data(html):
        soup = BeautifulSoup(html, 'lxml')
        night_temp = soup.find_all('div', {'class': 'value'})[0].find('span', {'class': "unit unit_temperature_c"}).text
        day_temp = soup.find_all('div', {'class': 'value'})[1].find('span', {'class': "unit unit_temperature_c"}).text
        night_temperature.append(night_temp)
        day_temperature.append(day_temp)

    def main():
        url = 'https://www.gismeteo.ua/weather-zaporizhia-5093/'
        get_data(get_html(url))

    main()
    return render_template('weather.html', night_temperature=night_temperature[-1],
                           day_temperature=day_temperature[-1])


@app.route('/add', methods=['POST', 'GET'])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_post = UserPost(name=name, email=email, message=message)
        db.session.add(new_post)
        db.session.commit()
        flash('Post added as successfully.')
        return redirect(url_for('add_post', form=form))

    return render_template('post.html', form=form)


@app.route('/posts')
@login_required
def post():
    posts = UserPost.query.all()
    # posts = UserPosts.query.filter_by(name=current_user.name)
    return render_template('posts.html', posts=posts)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404_error.html', title='404'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500_error.html', title='500'), 500

login_manager = LoginManager()
login_manager.login_view = 'login.html'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(UserPost, db.session))
"""

if __name__ == '__main__':
    app.run()
