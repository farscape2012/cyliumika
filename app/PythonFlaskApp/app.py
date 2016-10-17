# encoding=utf8-
from flask import Flask,render_template, request, redirect, session, json
import web

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

        #if len(data) > 0:
            #if check_password_hash(str(data[0][3]),_password):
            #    session['user'] = data[0][0]
        #TODO check login
        if _username == "mika.koskimaki@gmail.com":
            # TODO check password
            if _password == "mm":
                session['username'] = _username
                return redirect('/userhome')
            else:
                return render_template('signin.html',error = 'Wrong Password. Try again')
        else:
            return render_template('signin.html',error = 'Wrong Email address. Try again')


    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        print "closing"
        #TODO close mongodb??

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
