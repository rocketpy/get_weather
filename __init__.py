import json
import urllib.request
from flask import Flask__,  render_template, request
from flask_sqlalchemy import SQLAlchemy


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
