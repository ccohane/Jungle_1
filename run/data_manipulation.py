# clean and transform the data so to be used by jungle project
# below is the code to load data to jungle.db


import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine

engine = create_engine('sqlite:///Jungle.db')
df = pd.read_csv("run/description_in_matrix1.csv")
df = df.drop(['Unnamed: 0'],axis=1)
df.to_sql('restaurants',con=engine,index=False, if_exists='append')


engine = create_engine('sqlite:///Jungle.db')
df = pd.read_csv("run/reviews_in_matrix.csv")
df = df.drop(['Unnamed: 0','funny','useful','cool','review_id'],axis=1)
df.to_sql('reviews',con=engine,index=False, if_exists='append')




#disk_engine = create_engine('sqlite:///jungle.db')
#df_review.to_sql('reviews', disk_engine,index=False, if_exists='append')

# Insert df_review_5 data to jungle.db review table


