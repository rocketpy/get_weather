import os
from flask import Flask, Blueprint,  render_template, request, current_app
from flask_sqlalchemy import SQLAlchemy
from .models import User, UserPost
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)

app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
admin = Admin(app)

from .main import main as main_blueprint
from .auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)  # for auth routes
app.register_blueprint(main_blueprint)  # for non-auth


# app.config['SECRET_KEY'] = ''
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(UserPost, db.session))


if __name__ == '__main__':
    app.run()
