from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
import routes
import models
import forms


app = Flask(__name__)
app.config.from_pyfile('config.py')
admin = Admin(app)
db = SQLAlchemy(app)
db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
