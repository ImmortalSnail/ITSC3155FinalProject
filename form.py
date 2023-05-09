from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired
from models import Topic

class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=8, max=50)
    ])
    confirm = PasswordField('Repeat Password')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class PostReplyForm(FlaskForm):
    content = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReplyReplyForm(FlaskForm):
    content = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    topic = SelectField('Topic', choices=[('1', 'Computer Hardware'), ('2', 'Computer Software'), ('3', 'Networking'), ('4', 'Cyberecurity'), 
                                          ('5', 'Programming Langs'), ('6', 'AI'), ('7', 'Databases'), ('8', 'Web Dev'), ('8', 'Data Science'), ('10', 'Programming Help')], validators=[DataRequired()])
    submit = SubmitField('Post')