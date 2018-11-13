#!/usr/bin/env python3
from orm import Database
import pickle
import numpy as np
import pandas as pd

def create_user(user_name , password):
    with Database() as db:
        user_name_taken = check_user_exist(user_name)
        if user_name_taken==False:
            sql='''INSERT INTO users(username,password) 
                            Values(?,?);'''
            db.c.execute(sql, (user_name, password))
            return True
        else:
            return False

def check_user_exist(user_name):
    with Database() as db:
        db.c.execute('''SELECT * FROM users WHERE username='{}';'''.format(user_name))
        result=db.c.fetchone()

        if result:
            return True
        else:
            return False

def check_user(user_name, password):
    with Database() as db:
        db.c.execute('''SELECT * FROM users WHERE username='{}'
                        AND password='{}';'''.format(user_name, password))
        result=db.c.fetchone()

        if result:
            return True
        else:
            return False

def get_restaurants(user_name):
    '''
    Create a recommendation algorith to get a list of restaurants and information about restaurants
    Return as a list of dictionaries 
    '''
    file = open("final_recommend_pickle.pkl",'rb')
    recommend = pickle.load(file)
    file.close()
    x=recommend[user_name]
    y= x.nlargest(10).index
    y=list(y)
    restaurants=[]
    for z in y:
        restaurants.append(get_restaurant_data(z))
    return restaurants

def get_restaurants_user_sim(user_name):
    '''
    Create a recommendation algorith to get a list of restaurants and information about restaurants
    Return as a list of dictionaries 
    '''
    file = open("user_similarity_recommend.pkl",'rb')
    recommend = pickle.load(file)
    file.close()
    x=recommend[user_name]
    y= x.nlargest(10).index
    y=list(y)
    restaurants=[]
    for z in y:
        restaurants.append(get_restaurant_data(z))
    return restaurants

def get_restaurants_item_sim(user_name):
    '''
    Create a recommendation algorith to get a list of restaurants and information about restaurants
    Return as a list of dictionaries 
    '''
    file = open("item_similarity_recommend.pkl",'rb')
    recommend = pickle.load(file)
    file.close()
    x=recommend[user_name]
    y= x.nlargest(10).index
    y=list(y)
    restaurants=[]
    for z in y:
        restaurants.append(get_restaurant_data(z))
    return restaurants

def get_restaurant_data(restaurant_id):
    with Database() as db:
        db.c.execute('''SELECT * FROM restaurants WHERE business_id = '{}';'''.format(restaurant_id))
        results=db.c.fetchone()
        results= {'Name': results[3],
                  'Address': results[6],
                  'Town': results[8] + ", "+results[7] + " "+ results[9],
                  'Categories': results[2],
                  'Yelps Average Star': results[5],
                  'Review Count': results[4],
                  'Business_id': results[1] }
        return results

def get_star(review):
    file = open("my_classifier.pkl",'rb')
    classifier = pickle.load(file)
    file.close()
    star = classifier.classify(review)
    return star

def add_review_to_db(user_name,business_id,stars,review):
    with Database() as db:
        db.c.execute('''INSERT INTO reviews(user_id,business_id,stars,text)
                        Values('{}','{}',{},'{}')'''.format(user_name,business_id,stars,review))
        return True

def get_preference(preference):
    with Database() as db:
        _length = len(preference)
        db.c.execute('''SELECT categories, business_id FROM restaurants;''')
        results=db.c.fetchall()
        recommends=[]
        for x in results:
            if(all(y in x[0] for y in preference)):
                recommends.append(x[1])
        return recommends

def get_user_id(business_id,star):
    with Database() as db:
        db.c.execute('''SELECT user_id FROM reviews WHERE business_id = '{}' AND stars = {};'''.format(business_id,star))
        results=db.c.fetchall()
        return results[0][0]




def get_review_ML_score(business_id):
    '''
    '''
    #restaurants = [{'name': 'Taco Bell', 'mlstar':5, 'Address': '456 Madison'}]

    pass

def preference_to_restaurants(preference):
    '''
    based on the preference provided, recommend restaurants
    '''
    dic_restaurants = {}
    with Database() as db:
        for element in preference:
            db.c.execute('''SELECT name FROM restaurants WHERE categories LIKE '%{}%';'''.format(element))
            results=db.c.fetchall()
            if results:
                for row in results:
                    if row[0] not in dic_restaurants.keys():
                        dic_restaurants[row[0]] = 1
                    else:
                        dic_restaurants[row[0]] += 1
        sort_restaurants = sorted((value, key) for (key, value) in dic_restaurants.items())
        sort_restaurants.reverse()
        #if len(sort_restaurants) <= 5:
            #for restaurant in sort_restaurants:
                #db.c.execute('''SELECT name, stars, address, state, city, postal_code FROM restaurants WHERE name ={};'''.format(restaurant[1]))

    return sort_restaurants
    #for i in range(5):

def search(search_item):
    '''search the item in restaurant name column
    '''
    with Database() as db:
        db.c.execute('''SELECT name, stars, address, state, city, postal_code FROM restaurants WHERE name LIKE '%{}%';'''.format(search_item))
        results=db.c.fetchall()
        if results:
            restaurants = []
            for row in results:
                dic = {
                    'name': row[0],
                    'mlstar': row[1],
                    'Address': row[2]+' '+row[3]+' '+row[4]+' '+row[5]
                }
                restaurants.append(dic)
            return restaurants
        else:
            return False


get_restaurants('-0IiMAZI2SsQ7VmyzJjokQ')

