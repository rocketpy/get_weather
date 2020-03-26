from flask import Flask
import scrapy
# import socketio
from scrapy.crawler import CrawlerProcess
# from scrapy.settings import CrawlerSettings
from flask_admin import Admin
from flask_wtf import FlaskForm
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, BooleanField
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, logout_user
from wtforms.validators import InputRequired, Length, DataRequired
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_user import UserMixin, UserManager, SQLAlchemyAdapter, login_required, current_user
# from .get_weather.get_weather.spiders import
# from flask_bootstrap import Bootstrap


app = Flask(__name__)
# sio = socketio.AsyncServer()
# sio.attach(app)
admin = Admin(app)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['WTF_CSRF_SECRET_KEY'] = "CSRF_SECRET_KEY"
app.config['CSRF_ENABLED'] = True  # False , for disable csrf protection
# app.config.from_pyfile('config.py')
# app.config['USER_ENABLE_EMAIL'] = False
# app.config['USER_APP_NAME'] = 'Flask_weather'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
db.init_app(app)
# Bootstrap(app)


#  Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    name = db.Column(db.String(20))
    surname = db.Column(db.String(20))
    sex = db.Column(db.String(6))
    email = db.Column(db.String(50), unique=True)
    birthday = db.Column(db.String(10))
    password = db.Column(db.String(50))


# db_adapter = SQLAlchemyAdapter(db, User)
# user_manager = UserManager(db_adapter, app)


class UserPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(50))
    message = db.Column(db.Text(1000))
#   date_posted = db.Column(db.DateTime)


# Forms and validators
class SignUp(FlaskForm):
    name = StringField('name', validators=[InputRequired(message='An name is required !'),
                                           Length(min=2, max=20)])
    surname = StringField('surname', validators=[InputRequired(message='An surname is required !'),
                                                 Length(min=2, max=20)])
    sex = StringField('sex', validators=[Length(min=4, max=6, message='Not greater a 6 simbols')])
    email = StringField('email', validators=[InputRequired(message='An email is required !'),
                                             Length(min=10, max=50)])
    birthday = StringField('birthday', validators=[Length(min=6, max=10, message='Not greater a 6 simbols')])
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(min=5, max=50, message='Not greater a 50')])


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(message='An email is required !'),
                                             Length(min=10, max=50)])
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(min=5, max=50, message='Not greater a 50')])
    remember = BooleanField('remember me')


class AddPostForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(message='An name is required !'),
                                           Length(min=2, max=20)])
    email = StringField('email', validators=[InputRequired(message='An email is required !'),
                                             Length(min=10, max=50)])
    message = StringField('message', validators=[InputRequired(message='Text field is required !'),
                                                 Length(min=5, max=1000)])


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
    form = SignUp()  # (csrf_enabled=False)

    name = request.form.get('name')  # request.form['name']
    surname = request.form.get('surname')
    email = request.form.get('email')
    sex = request.form.get('sex')
    birthday = request.form.get('birthday')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if form.validate_on_submit():
        new_user = User(name=name, surname=surname, email=email, sex=sex, birthday=birthday,
                        password=generate_password_hash(password, method='sha256'))
        if user:
            flash('Email address already exists')
            return render_template('login.html', form=form)

        db.session.add(new_user)  # adding a new user to db
        db.session.commit()
        flash('New user created !')
        return render_template('profile.html')  # return redirect('/success')

    return render_template('signup.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login_post():
    form = LoginForm()
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if form.validate_on_submit():
        login_user(user, remember=remember)
        flash('Logged in successfully.')
        return redirect(url_for('add_post', form=form))

    if user:  # or not check_password_hash(user.password, password):
        flash('Please check your login details and try again !')
        return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/weather', methods=['GET', 'POST'])
@login_required
def show_weather():
    night_temperature = []
    day_temperature = []
    if request.method == 'POST':

        class MySpider(scrapy.Spider):
            name = "weather_spider"
            allowed_domains = ['gismeteo.ua']
            start_urls = ['https://www.gismeteo.ua/weather-zaporizhia-5093/']

            def parse(self, response):
                values = response.css('div.value')
                night_temp = values.css('span.unit.unit_temperature_c::text')[0].extract()
                day_temp = values.css('span.unit.unit_temperature_c::text')[1].extract()
                night_temperature.append(night_temp)
                day_temperature.append(day_temp)

        process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
        process.crawl(MySpider)
        process.start()

    return render_template('weather.html', night_temperature=night_temperature[-1], day_temperature=day_temperature[-1])

# from scrapy import cmdline
# cmdline.execute("scrapy crawl myspider".split())


@app.route('/add', methods=['POST', 'GET'])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_post = UserPost(name=name, email=email, message=message)  # date_posted=datetime.now()
        db.session.add(new_post)
        db.session.commit()
        flash('Post added as successfully.')
        return redirect(url_for('add_post'))

    return render_template('post.html', form=form)


@app.route('/posts')
@login_required
def post():
    posts = UserPost.query.all()
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


# app.register_blueprint(auth)
# app.register_blueprint(main)

login_manager = LoginManager()
login_manager.login_view = 'login.html'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(UserPost, db.session))


if __name__ == '__main__':
    app.run(debug=False)

# socketio.run(app, debug=True)
# app.run(debug=False)
# app.run(host='0.0.0.0', port=4000)   http://localhost:4000/
