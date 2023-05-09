from flask_login import UserMixin
from flask_security import RoleMixin
from database import db

class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

class Topic(db.Model):
    __tablename__ = 'topics'

    topic_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)


class Post(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    topic = db.relationship(Topic, backref=db.backref('posts', lazy='dynamic'))
    user = db.relationship(User, backref=db.backref('posts', lazy='dynamic'))


class PostReply(db.Model):
    __tablename__ = 'post_replies'

    reply_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    post = db.relationship(Post, backref=db.backref('replies', lazy='dynamic'))
    user = db.relationship(User, backref=db.backref('post_replies', lazy='dynamic'))


class ReplyReply(db.Model):
    __tablename__ = 'reply_replies'

    reply_id = db.Column(db.Integer, primary_key=True)
    parent_reply_id = db.Column(db.Integer, db.ForeignKey('post_replies.reply_id'))
    parent_reply_reply_id = db.Column(db.Integer, db.ForeignKey('reply_replies.reply_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    parent_reply = db.relationship('PostReply', backref=db.backref('replies', lazy='dynamic'))
    parent_reply_reply = db.relationship('ReplyReply', remote_side=[reply_id], backref=db.backref('replies', lazy='dynamic'))
    user = db.relationship('User', backref=db.backref('reply_replies', lazy='dynamic'))
    post = db.relationship('Post', backref=db.backref('reply_replies', lazy='dynamic'))
    