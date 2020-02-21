from flask import Flask,  render_template, request
from flask_sqlalchemy import SQLAlchemy
from .main import main as main_blueprint
from .auth import auth as auth_blueprint
from .models import User
from flask_login import LoginManager


app = Flask(__name__)
db = SQLAlchemy(app)
# app.config['SECRET_KEY'] = ''

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
# for auth routes
app.register_blueprint(auth_blueprint)
# for non-auth
app.register_blueprint(main_blueprint)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)


"""
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    # app.config['SECRET_KEY'] = ''
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    # for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # for non-auth
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


if __name__ == '__main__':
    create_app()

"""