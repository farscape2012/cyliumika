from app import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from .forms import LoginForm
from .user import User
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        _password_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        print("name: {}, _email: {}, _password: {}".format(form.username.data, form.email.data, _password_hash))
        try:
            app.config['USERS_COLLECTION'].insert({"_id": form.username.data, "email": form.email.data, "password": _password_hash, "email_ack": False})
            print "User created."
        except DuplicateKeyError:
            print "User already present in DB. Try other username"
            return render_template('register.html', form=form)
        print"Thanks for registering"
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        print "checking user credentials"
        user = app.config['USERS_COLLECTION'].find_one({"_id": form.username.data})
        if user and User.validate_login(user['password'], form.password.data):
            user_obj = User(user['_id'])
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            return redirect(request.args.get("next") or url_for("userhome"))
        flash("Wrong username or password!", category='error')
    return render_template('login.html', title='login', form=form)

@app.route('/userhome', methods=['GET', 'POST'])
@login_required
def userhome():
    return render_template('userhome.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    logout_user()
    flash("Logged out successfully!", category='success')
    return redirect(url_for('index'))


@app.route('/writealetter', methods=['GET', 'POST'])
@login_required
def writealetter():
    return render_template('writealetter.html')

@lm.user_loader
def load_user(username):
    u = app.config['USERS_COLLECTION'].find_one({"_id": username})
    if not u:
        return None
    return User(u['_id'])
