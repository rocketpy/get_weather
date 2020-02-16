import json
import urllib.request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
#from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres1@localhost/DataCollector'  #  'sqlite:///blog.db'
db = SQLAlchemy(app)

# 1 create a table for comments 
class CommentPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    

# 2 create a table for comments
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)

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


if (__name__ =="__main__"):
    app.run(debug=True)

