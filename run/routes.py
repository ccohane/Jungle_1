#!usr/bin/env python3

from flask import Flask, render_template, request, redirect, session, jsonify, url_for, escape
import requests, model, random


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
        user_name= model.get_id_in_matrix(user_name)
        if(user_name== None):
            user_name= model.get_random_username()
        restaurants=model.get_restaurants(user_name)
        random.shuffle(restaurants)
        return render_template('dashboard.html', restaurants = restaurants[:10], message = "Jungle recommends these fine establishments based on your profile!")
    else:
        user_name='%s' % escape(session['username'])
        #restaurants=model.get_restaurants(user_name)
        #when preference is chosen, form data will be used 
        #to recommend restaurants
        preference = request.form.getlist('preference')
        restaurants = model.get_restaurants(user_name)
        random.shuffle(restaurants)
        return render_template('dashboard.html', restaurants = restaurants[:10],message = "Jungle recommends these fine establishments based on your profile!")
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
        #user_name='%s' % escape(session['username'])
        recommends = model.get_preference(preference)
        restaurants=[]
        for x in recommends[:50]:
            restaurants.append(model.get_restaurant_data(x))
        random.shuffle(restaurants)
        return render_template('dashboard.html', restaurants = restaurants[:10], message = "Jungle recommends these fine establishments based on the preferences you entered!")



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
        business_ids = model.search(search_item)
        restaurants=[]
        for x in business_ids:
            restaurants.append(model.get_restaurant_data(x[0]))
        random.shuffle(restaurants)
        if len(restaurants)>0:
            return render_template('dashboard.html', restaurants = restaurants[:10],message = "Is this the restaurant you are looking for?")
        else:
            user_name='%s' % escape(session['username'])
            user_name= model.get_id_in_matrix(user_name)
            if(user_name== None):
                user_name= model.get_random_username()
            restaurants=model.get_restaurants(user_name)
            random.shuffle(restaurants)
            return render_template('dashboard.html', restaurants = restaurants[:10], message = "Restaurant cannot be found but here are some restaurants you may like. ")


@app.route('/review',methods=['GET','POST'])
def review():
    if request.method == 'POST':
        user_name='%s' % escape(session['username'])
        business_id = request.form['business_id']
        review = request.form['review']
        star = int(request.form['star'])
        user_name = model.get_user_id(business_id,star, user_name)
        #star = model.get_star(review)
        model.add_review_to_db(user_name,business_id,star,review)
        restaurants = model.get_restaurants(user_name)
        random.shuffle(restaurants)
        return render_template('dashboard.html', restaurants = restaurants[:10],message = "Jungle recommends these fine establishments based on your profile!")


if __name__=="__main__":
    #FIXME change the following server setings from 127.1 to 0.0.0.0
    app.run(host="0.0.0.0", port="1997", debug=True)
    
