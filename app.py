from flask import Flask, render_template, request, redirect, url_for, flash
import datetime
import pymysql
import bcrypt
from config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, SECRET, SALT
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from form import RegistrationForm, LoginForm, PostReplyForm, ReplyReplyForm, PostForm
from models import Topic, User, Post, PostReply, ReplyReply
from database import db
from flask_wtf.csrf import CSRFProtect
## If you see this, pull worked ##
app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = f"{SECRET}"
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['REMEMBER_COOKIE_DURATION'] = datetime.timedelta(weeks=1)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

def status():
    logged_in = current_user.is_authenticated
    return logged_in

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('home.html', logged_in=status())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Get the user from the database
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf8'), user.password.encode('utf8')):
            # Log in the user
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('home'))
        else:
            # Invalid username or password
            flash('Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/posts/<int:post_id>')
@login_required
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    replies = post.replies.all()
    return render_template('post.html', post=post, replies=replies, logged_in=status())


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.user_id,
            topic_id=form.topic.data
        )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('topics'))

    return render_template('create_post.html', title='Create Post', form=form, Topic=Topic, logged_in=status())

@app.route('/posts/<int:post_id>/reply', methods=['GET', 'POST'])
@login_required
def reply_to_post(post_id):
    post = Post.query.get_or_404(post_id)

    form = PostReplyForm()

    if form.validate_on_submit():
        reply = PostReply(
            user=current_user,
            post=post,
            content=form.content.data
        )
        db.session.add(reply)
        db.session.commit()
        flash('Your reply has been posted.')
        return redirect(url_for('view_post', post_id=post.post_id))

    return render_template('reply.html', post=post, form=form, logged_in=status())


@app.route('/replies/<int:reply_id>/reply', methods=['GET', 'POST'])
@login_required
def reply_to_reply(reply_id):
    reply = PostReply.query.get_or_404(reply_id)

    form = ReplyReplyForm()

    if form.validate_on_submit():
        reply = ReplyReply(
            user=current_user,
            parent_reply=reply,
            content=form.content.data
        )
        db.session.add(reply)
        db.session.commit()
        flash('Your reply has been posted.')
        return redirect(url_for('view_post', post_id=reply.parent_reply_id))

    return render_template('reply.html', post=reply.post, form=form, logged_in=status())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new User object with the form data and add it to the database
        user = User(username=form.username.data, password=bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt()))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/topics')
@login_required
def topics():
    topics = Topic.query.all()
    posts = Post.query.all()
    return render_template('topics.html', logged_in=status(), topics=topics, posts=posts, Post=Post)

@app.route('/user')
@login_required
def user():
    return render_template('user.html', logged_in=status())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()