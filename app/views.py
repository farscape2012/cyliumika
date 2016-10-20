import os
import sys
from app import app, lm
from flask import request, redirect, render_template, url_for, flash
from flask.ext.login import login_user, logout_user, login_required
from .forms import LoginForm
from .user import User
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from werkzeug.security import generate_password_hash
import pymongo

__dir__ = os.path.dirname(__file__)
LIB_DIR = os.path.realpath(os.path.join(__dir__, '../lib'))
print(LIB_DIR)
sys.path.append(LIB_DIR)

import mongodb
mongoDB = mongodb.MongoDBClient()
mongoDB.db_con(host='127.0.0.1', username='admin', password='admin', port=27017, database='moon', collection='user')



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
        #_password_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        #TODO: figure out why hash does not work
        print("name: {}, _email: {}, _password: {}".format(form.username.data, form.email.data,form.password.data))
        try:
            mongoDB.insert_one({"_id": form.email.data, "email": form.email.data, "user": form.username.data, "password": form.password.data, "email_ack": False})
        except pymongo.errors.DuplicateKeyError:
            ## I dont know what should return here. I just return random output
            return json.dumps({'html':'<span>All fields good !!</span>'})
        
        #try:
        #    app.config['USERS_COLLECTION'].insert({"_id": form.username.data, "email": form.email.data, "password": _password_hash, "email_ack": False})
        #    print "User created."
        #except DuplicateKeyError:
        #    print "User already present in DB. Try other username"
        #    return render_template('register.html', form=form)
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
        # TODO: figure out why hash does not work
        _password_hash = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        print _password_hash
        doc = mongoDB.query_one(query={"email": form.email.data, "password": form.password.data})
        print("email: {}, password: {}".format(form.email.data, form.password.data))
        print doc
        if doc is not None:
            print('here 1')
            user_obj = User(doc['_id'])
            login_user(user_obj)
            flash("Logged in successfully!", category='success')
            print('here 12')
            return redirect(request.args.get("next") or url_for("userhome"))
            #return redirect('/userhome')
        else:
            print('here 2')
            return render_template('login.html',error = 'Wrong Email address. Try again')

        print "checking user credentials"
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
    doc = mongoDB.query_one(query={"email": username})
    if not doc:
        return None
    return User(doc['_id'])
