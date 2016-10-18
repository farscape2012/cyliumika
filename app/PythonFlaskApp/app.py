# encoding=utf8-
import pymongo
import os
import sys
from flask import Flask,render_template, request, redirect, session, json

__dir__ = os.path.dirname(__file__)
LIB_DIR = os.path.realpath(os.path.join(__dir__, '../../lib'))
print(LIB_DIR)
sys.path.append(LIB_DIR)

import mongodb
mongoDB = mongodb.MongoDBClient()
mongoDB.db_con(host='127.0.0.1', username='admin', password='admin', port=27017, database='moon', collection='user')

app = Flask(__name__)
app.secret_key = 'this is very secret key in messagemoon'

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')

@app.route('/signUp',methods=['POST'])
def signUp():

    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    print("name: {}, _email: {}, _password: {}".format(_name, _email, _name))
    try:
        mongoDB.insert_one({"_id": _name, "email": _email, "password": _password, "email_ack": False})
    except pymongo.errors.DuplicateKeyError:
        return json.dumps({'html':'<span>All fields good !!</span>'})
    # validate the received values
    if _name and _email and _password:
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']

        doc = mongoDB.query(query={"email": _username, "password": _password})
        if doc.count() == 1:
            return redirect('/userhome')
        else:
            return render_template('signin.html',error = 'Wrong Email address. Try again')

    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        print "closing"

@app.route('/userhome')
def userhome():
    if session.get('username'):
        return render_template('userhome.html')
    else:
        return render_template('signin.html',error = 'Unauthorized Access, You are not logged in')

@app.route('/writealetter')
def writeletter():
    if session.get('username'):
        return render_template('writealetter.html')
    else:
        return render_template('signin.html',error = 'Unauthorized Access, You are not logged in')

@app.route('/storeletter',methods=['POST'])
def storeletter():
    try:
        if True:
            _title = request.form['letterTitle']
            _description = request.form['letterContent']
            # TODO forward to mongodb
            if True:
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error occurred!')

        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
