from flask import Flask, render_template, request, redirect, url_for
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

class Users(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Posts', backref='user', lazy=True)
    comments = db.relationship('Comments', backref='user', lazy=True)

class Posts(db.Model):
    postID = db.Column(db.Integer, primary_key=True)
    postUsername = db.Column(db.String(80), nullable=False)
    userID = db.Column(db.Integer,db.ForeignKey(Users.userID), nullable=False)
    postTxt = db.Column(db.String(80), nullable=False)
    comments = db.relationship('Comments', backref='post', cascade='delete', lazy=True)

class Comments(db.Model):
    commentID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer,db.ForeignKey(Users.userID), nullable=False)
    postID = db.Column(db.Integer,db.ForeignKey(Posts.postID), nullable=False)
    commentTxt = db.Column(db.String, nullable=False)


#ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/createUser', methods=['GET','POST'])
def createUser():
    if request.method == 'POST':
        newUser = Users(username=request.form['username'])
        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('createUser'))
    return render_template('createUser.html')


#POSTS
@app.route('/posts', methods=['GET','POST'])
def posts():
    posts = Posts.query.all()
    users = Users.query.all()
    comments = Comments.query.all()
    if request.method == 'POST':
        findPoster = db.session.query(Users).filter(Users.userID == request.form['poster']).first()
        postUsername = findPoster.username
        newPost = Posts(
            userID=request.form['poster'],
            postUsername =postUsername,
            postTxt=request.form['postText']
        )
        db.session.add(newPost)
        db.session.commit() 
        return redirect(url_for('posts'))
    return render_template('posts.html',posts=posts,users=users,comments=comments)

@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def postEdit(id):
    postEdit=Posts.query.get(id)
    if request.method =="POST":
        postEdit.postTxt = request.form.get('postEdit')
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('postEdit.html',posts=postEdit)

@app.route('/posts/delete/<int:id>', methods=['GET','POST'])
def postDelete(id):
    post = Posts.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts'))


#COMMENTS
@app.route('/posts/comment',methods=['GET','POST'])
def comment():
    comments=Comments.query.all()
    posts=Posts.query.all()
    users=Users.query.all()
    if request.method == 'POST':
        findcomPoster = db.session.query(Users).filter(Users.userID == request.form['commentPoster']).first()
        ComUsername = findcomPoster.username
        newComment = Comments(
            postID = request.form.get('postID'),
            userID = request.form['commentPoster'],
            commentTxt= request.form['commentText']
        )
        db.session.add(newComment)
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('posts.html',comments=comments,posts=posts,users=users)

@app.route('/posts/comment/edit', methods=['GET','POST'])
def commentEdit():
    pass

@app.route('/posts/comment/delete<int:id>', methods=['GET','POST'])
def commentDelete(id):
    comment = Comments.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('posts'))

    
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)