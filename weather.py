from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, DataRequired
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user


app = Flask(__name__)

# app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
admin = Admin(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/admin/PycharmProjects/get_weather/get_weather/db.sqlite'
db.init_app(app)


# from .project.models.models import User, UserPost
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

# db.init_app(app)
# from .project.main.main import main as main_blueprint
# main = Blueprint('main', __name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


class AddPostForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(message='An email is required !')])
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(max=100, message='Not greater a 100')])


@app.route('/add', methods=['POST'])
@login_required
def add_post():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    post = UserPost(name=name, email=email, message=message)
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))

# from .project.auth.auth import auth as auth_blueprint
# auth = Blueprint('auth', __name__, template_folder='templates')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
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

    return redirect(url_for('app.login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('app.index'))


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
    return redirect(url_for('app.profile'))


# app.register_blueprint(auth)  # auth_blueprint
# app.register_blueprint(main)  # main_blueprint

# app.config['SECRET_KEY'] = ''
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
# db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'app.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(UserPost, db.session))


if __name__ == '__main__':
    app.run(debug=True)
