#!usr/bin/env python3

from flask import Flask, render_template, request, redirect, session, jsonify, url_for, escape
import requests, model


app=Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Qhgvf8z\n\xec]/'
#----------------------------------------------------------------------------------------
@app.route('/')
def index():
    if 'username' in session:
        return redirect("/dashboard")
    return redirect("/go")

@app.route('/go', methods=['GET'])
def start():
    if request.method == 'GET':
        return render_template('go.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        session['username'] = request.form['username']
        username = request.form['username']
        password = request.form['password']
        suc=model.create_user(username,password)
        if suc:
            return redirect(url_for('index'))
        else:
            return render_template('register.html', message='Username Taken')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        session['username'] = request.form['username']
        if model.check_user(username,password):
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Login error')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/go')

@app.route('/dashboard')
def dashboard():
    if request.method == 'GET':
        user_name='%s' % escape(session['username'])
        #restaurants=model.get_restaurants(user_name)
        return render_template('dashboard.html', )
    else:
        user_name='%s' % escape(session['username'])
        #restaurants=model.get_restaurants(user_name)
        return render_template('dashboard.html', message='Username Taken')


if __name__=="__main__":
    #FIXME change the following server setings from 127.1 to 0.0.0.0
    app.run(host="127.1", port="5000", debug=True)
    
