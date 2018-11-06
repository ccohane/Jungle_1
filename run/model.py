#!/usr/bin/env python3
from orm import Database

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
    with Database() as db:
        db.c.execute('''SELECT name, stars, address, state, city, postal_code FROM restaurants LIMIT 10;''')
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

def get_review_ML_score(business_id):
    '''
    '''
    #restaurants = [{'name': 'Taco Bell', 'mlstar':5, 'Address': '456 Madison'}]

    pass

def preference_to_restaurants(preference):
    '''based on the preference provided, recommend restaurants
    '''
    pass


