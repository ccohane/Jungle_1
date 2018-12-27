import nltk, re
import numpy as np
import pandas as pd
import pickle
import timeit
nltk.download('punkt')

df=pd.DataFrame()
df2=pd.DataFrame()
df3=pd.DataFrame()
count=0
for x in pd.read_csv('restaurant_reviews.csv',chunksize=200000):
    if count < 8:
        df = pd.concat([df,x])
    elif 8 <= count < 16 :
        df2 = pd.concat([df2,x])
    else:
        df3 = pd.concat([df3,x])
    count+=1
df=pd.concat([df,df2,df3])

def format_sentence(sent):
    return({word: True for word in nltk.word_tokenize(sent)})

def strip_accents(text):
    import unicodedata
    try:
        text = unicode(text, 'utf-8')
    except NameError: # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

import time
print(time.time())
very_bad=[[format_sentence(strip_accents(row['text'])),row['stars']] for index,row in df.iterrows() if row['stars']==1] 
print(time.time())
bad=[[format_sentence(strip_accents(row['text'])),row['stars']] for index,row in df.iterrows() if row['stars']==2]
print(time.time())
good=[[format_sentence(strip_accents(row['text'])),row['stars']] for index,row in df.iterrows() if row['stars']==3]
print(time.time())
great=[[format_sentence(strip_accents(row['text'])),row['stars']] for index,row in df.iterrows() if row['stars']==4]
print(time.time())
excellent=[[format_sentence(strip_accents(row['text'])),row['stars']] for index,row in df.iterrows() if row['stars']==5]
print(time.time())

training= very_bad[:int((.9)*len(pos))] + bad[:int((.9)*len(pos))] + good[:int((.9)*len(pos))] + great[:int((.9)*len(pos))] + excellent[:int((.9)*len(pos))]
test= very_bad[int((.1)*len(pos)):] + bad[int((.1)*len(pos)):] + good[int((.1)*len(pos)):] + great[int((.1)*len(pos)):] + excellent[int((.1)*len(pos)):]


save_training_data = open("training.pickle","wb")
pickle.dump(training, save_training_data)
save_training_data.close()

save_test_data = open("test.pickle","wb")
pickle.dump(test, save_test_data)
save_test_data.close()

from nltk.classify import NaiveBayesClassifier

classifier = NaiveBayesClassifier.train(training)

save_classifier = open("naivebayes.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

from nltk.classify.util import accuracy
f = open("accuracy.txt", "a")
f.write(str(accuracy(classifier, test)))
f.close()
