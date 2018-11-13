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
        return redirect("/preference")
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
            return render_template('login.html', message='Incorrect username or password')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect('/go')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'GET':
        user_name='%s' % escape(session['username'])
        restaurants=model.get_restaurants(user_name)
        return render_template('dashboard.html', restaurants = restaurants[:10])
    else:
        user_name='%s' % escape(session['username'])
        #restaurants=model.get_restaurants(user_name)
        #when preference is chosen, form data will be used 
        #to recommend restaurants
        preference = request.form.getlist('preference')
        restaurants = model.preference_to_restaurants(preference)
        return render_template('dashboard.html', restaurants = restaurants[:10])
'''
@app.route('/preference', methods=['GET', 'POST'])
def preference():
    if request.method == 'GET':
        return render_template('preference.html')
    else:
        return render_template('dashboard.html')
'''
@app.route('/preference', methods=['GET', 'POST'])
def preference():
    if request.method == 'GET':
        return render_template('preference.html')
    else:
        preference = request.form.getlist('preference')
        #similar_user = model.get_user_id(preference)
        #restaurants = model.get_restaurants(similar_user)
        recommends = model.get_preference(preference)
        restaurants=[]
        for x in recommends:
            print(x)
            restaurants.append(model.get_restaurant_data(x))
        return render_template('dashboard.html', restaurants = restaurants[:10])



# Search function
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_item = request.form['search']
        return redirect("/searchresult/{}".format(search_item))
    else:
        return render_template('search.html')

# Search result function
@app.route("/searchresult/<search_item>", methods=['GET', 'POST'])
def searchresult(search_item):
    if request.method == 'GET':
        result = model.search(search_item)
        if result:
            return render_template('search.html', restaurants = result)
        else:
            return render_template('search.html', message = "bad search item")


@app.route('/review',methods=['GET','POST'])
def review():
    if request.method == 'POST':
        user_name='%s' % escape(session['username'])
        business_id = request.form['business_id']
        review = request.form['review']
        star = int(request.form['star'])
        user_name = model.get_user_id(business_id,star)
        #star = model.get_star(review)
        model.add_review_to_db(user_name,business_id,star,review)
        restaurants = model.get_restaurants(user_name)

        return render_template('dashboard.html', restaurants = restaurants[:10])


if __name__=="__main__":
    #FIXME change the following server setings from 127.1 to 0.0.0.0
    app.run(host="127.1", port="5000", debug=True)
    
