from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = "password"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'SECRET'


db = SQLAlchemy(app)

#DATABASES

class Posts(db. Model):
    postID = db.Column(db.Integer, primary_key=True)
    poster = db.Column(db.String(80), nullable=False)
    postTxt = db.Column(db.String(80), nullable=False)
    #comments = db.relationship('Comments', backref='posts', lazy=True)

class Comments(db.Model):
    commentID = db.Column(db.Integer, primary_key=True)
    poster = db.Column(db.String, nullable=False)
    commentTxt = db.Column(db.String, nullable=False)


#ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts', methods=['GET','POST'])
def posts():
    posts = Posts.query.all()
    if request.method == 'POST':
        newPost = Posts(
            poster=request.form['name'],
            postTxt=request.form['postText']
        )
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('posts.html',posts=posts)


    
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)