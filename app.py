from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates')


logged_in = True


@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('home.html', logged_in=logged_in)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/post')
def post():
    return render_template('post.html', logged_in=logged_in)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/topics')
def topics():
    return render_template('topics.html', logged_in=logged_in)

@app.route('/user')
def user():
    return render_template('user.html', logged_in=logged_in)

@app.route('/logout')
def logout():
    return redirect(url_for('home'))