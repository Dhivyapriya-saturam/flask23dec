import json

from flask import Flask, request, session, redirect, url_for, render_template, g
import requests
import os
from ex import ex_blueprint

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(ex_blueprint)


@app.route('/login', methods=['GET', 'POST'])
def index():
    """
    create a session for the user
    :return:
    """
    if request.method == 'POST':
        session.pop('user', None)

        if request.form['password'] == 'password':
            session['user'] = request.form['username']
            var = session.get('user', None)
            print(var)
            return redirect(url_for('protected', name=var))

    return render_template('index.html')


@app.route('/protected')
def protected():
    """
    protect the existing user credentials
    :return:
    """
    if g.user:
        # return "hello"
        username = request.args.get('name')
        # return "hello"+username
        return render_template('protected.html', name=username)

    return redirect(url_for('index'))


@app.route('/display')
def dis():
    list = [1, 2, 3]
    if list[0]:
        return render_template('display.html', id=list[0])
    elif list[1]:
        return render_template('display.html', id=list[1])
    elif list[2]:
        return render_template('display.html', id=list[2])


'''
@app.route('/processjson',methods='GET', '')
def processjson():
    url="https://localhost:8080"
    data={'divya':'IT'}
    headers={'Content-type':'application/json','Accept': 'text/plain'}
    r=requests.post(url, data=json.dumps(data), headers=headers)
    return render_template('jsonfile.html', file=r)

'''


@app.before_request
def before_request():
    """
    store the user into session
    """
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/getsession')
def getsession():
    """
    Availability of user in session
    :return:
    """
    if 'user' in session:
        return session['user']

    return 'Not logged in!'


@app.route('/dropsession')
def dropsession():
    """
    Drop the session for that user
    :return:
    """
    session.pop('user', None)
    return 'Dropped!'


if __name__ == '__main__':
    app.run(debug=True)
