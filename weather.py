from flask import Flask
from flask_admin import Admin
from flask_wtf import FlaskForm
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, logout_user
from wtforms.validators import InputRequired, Length, DataRequired
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_user import UserMixin, UserManager, SQLAlchemyAdapter, login_required, current_user


app = Flask(__name__)

# app.config.from_pyfile('config.py')

admin = Admin(app)
app.config['CSRF_ENABLED'] = False
app.config['USER_ENABLE_EMAIL'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
db.init_app(app)
Bootstrap(app)


class User(db.Model, UserMixin):
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


class SignUp(FlaskForm):
    name = StringField('name', validators=[InputRequired(message='An name is required !')])
    surname = StringField('surname', validators=[InputRequired(message='An surname is required !')])
    sex = StringField('sex')
    email = StringField('email', validators=[InputRequired(message='An email is required !')])
    birthday = StringField('birthday')
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(max=100, message='Not greater a 100')])


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(message='An email is required !')])
    password = PasswordField('password', validators=[InputRequired(message='A password is required !'),
                                                     Length(max=100, message='Not greater a 100')])


class AddPostForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(message='An name is required !')])
    email = StringField('email', validators=[InputRequired(message='An email is required !')])
    message = StringField('message', validators=[InputRequired(message='Text field is required !')])

# db_adapter = SQLAlchemyAdapter(db, User)
# user_manager = UserManager(db_adapter, app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup_post():
    form = SignUp()
    name = request.form.get('name')
    surname = request.form.get('surname')
    email = request.form.get('email')
    sex = request.form.get('sex')
    birthday = request.form.get('birthday')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()  # this returns if email already exists in database

    if user:  # redirect back to signup page
        flash('Email address already exists')
        return redirect(url_for('signup.html', form=form))

    # create new user
    new_user = User(id=id, name=name, surname=surname, email=email, sex=sex, birthday=birthday,
                    password=generate_password_hash(password, method='sha256'))

    # adding a new user to db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login.html'))


@app.route('/login', methods=['POST', 'GET'])
def login_post():
    form = LoginForm()
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login.html'))
    login_user(user, remember=remember)
    return redirect(url_for('weather.html', form=form))


"""
# main = Blueprint('main', __name__, template_folder='templates')
@app.route('/')
def index():
    return render_template('index.html')
"""


@app.route('/weather')
#@login_required
def weather():
    return render_template('weather.html')

"""
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
"""


@app.route('/add', methods=['POST', 'GET'])
#@login_required
def add_post():
    form = AddPostForm()
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    new_post = UserPost(name=name, email=email, message=message)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('index.html', form=form))

# from .project.auth.auth import auth as auth_blueprint
# auth = Blueprint('auth', __name__, template_folder='templates')


@app.route('/posts')
#@login_required
def post():
    posts = UserPost.query.order_by(UserPost.date_posted.desc()).all()
    return render_template('post.html', post=posts)


@app.route('/logout')
#@login_required
def logout():
    logout_user()
    return redirect(url_for('index.html'))


# app.register_blueprint(auth)  # auth_blueprint
# app.register_blueprint(main)  # main_blueprint

login_manager = LoginManager()
login_manager.login_view = 'login.html'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(UserPost, db.session))


if __name__ == '__main__':
    app.run(debug=True)
