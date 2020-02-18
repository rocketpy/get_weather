
import json
import urllib.request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect
#from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

#app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)
    
# for auth routes
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# for non-auth 
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

"""
def create_app():
    app = Flask(__name__)
    #app.config['SECRET_KEY'] = ''
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)
    
    # for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # for non-auth 
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
"""
"""
# create a table for comments 
class CommentPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    
# create a table(other way) for comments
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
"""
"""    
class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key = True)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    shoesize = db.Column(db.Integer)
    sex = db.Column(db.String)

    def __init__(self, height, weight, shoesize, sex):
        self.height = height
        self.weight = weight
        self.shoesize = shoesize
        self.sex = sex
"""
"""
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather")
def weather():
    return render_template("weather.html")

@app.route("/posts/<int:post_id>")
def posts(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('posts.html', post=post)

@app.route("/success", methods = ['POST'])
def success():
    return render_template("success.html")

"""
if (__name__ =="__main__"):
    app.run(debug=True)

