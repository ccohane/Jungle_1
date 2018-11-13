# clean and transform the data so to be used by jungle project
# below is the code to load data to jungle.db


import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
'''
df_review_100=pd.read_csv('data/review.csv',nrows =100)
bus_id = df_review_100['business_id'].unique()
bus_id_df = pd.DataFrame({'business_id':bus_id })

df_bus = pd.read_csv('less_restaurants_description_in_matrix1.csv')
result = pd.merge(bus_id_df, df_bus, on = 'business_id')
result_1 = result.loc[:,['business_id','categories','name','neighborhood','review_count','state','address','city','stars']]

disk_engine = create_engine('sqlite:///jungle.db')
result_1.to_sql('restaurants', disk_engine, index=False, if_exists='append')

#df = pd.read_csv("data/review.csv",nrows =100)
#df_review = df.loc[:, ['user_id', 'business_id', 'stars','date', 'text']]
#df_review.rename(columns = {'text': 'review'}, inplace = True)

'''
engine = create_engine('sqlite:///Jungle.db')
df = pd.read_csv("description_in_matrix1.csv")
df = df.drop(['Unnamed: 0'],axis=1)
df.to_sql('restaurants',con=engine,index=False, if_exists='append')


engine = create_engine('sqlite:///Jungle.db')
df = pd.read_csv("reviews_in_matrix.csv")
df = df.drop(['Unnamed: 0','funny','useful','cool','review_id'],axis=1)
df.to_sql('reviews',con=engine,index=False, if_exists='append')




#disk_engine = create_engine('sqlite:///jungle.db')
#df_review.to_sql('reviews', disk_engine,index=False, if_exists='append')

# Insert df_review_5 data to jungle.db review table


