""" Code Challenge -- Restaurant Review DL

The purpose of this analysis is to build a prediction model to predict whether a review on 
the restaurant is positive or negative. To do so, we will work on Restaurant Review dataset. 

Dataset: Restaurant_Reviews.tsv is a dataset from Kaggle datasets which consists of 1000
 reviews on a restaurant.

To build a model to predict if review is positive or negative, following steps are performed.

Importing Dataset
Preprocessing Dataset
Vectorization
Training and Classification using Deep Learning model
Analysis Conclusion (train and test score) """


import pandas as pd

df =  pd.read_csv('Restaurant_Reviews.tsv',sep="\t")

df.head(5)

df.isnull().any(axis = 0)

from sklearn.model_selection import train_test_split

features_train, features_test, labels_train, labels_test = train_test_split(df['Review'], df['Liked'], random_state = 42, test_size = 0.5 )

from sklearn.feature_extraction.text import TfidfVectorizer

vect = TfidfVectorizer(min_df=5)

features_train_vectorized = vect.fit_transform(features_train)

features_train_vectorized

features_train_vectorized = features_train_vectorized.todense()

import numpy as np

from keras.models import Sequential

from keras.layers.core import Dense, Dropout, Activation

from keras.optimizers import Adadelta,Adam,RMSprop

from keras.utils import np_utils

model = Sequential()

model.add(Dense(700,input_shape= (198,)))

model.add(Activation('relu'))

model.add(Dropout(0.5))

model.add(Dense(500))

model.add(Activation('relu'))

model.add(Dropout(0.5))

model.add(Dense(100))

model.add(Activation('relu'))

model.add(Dropout(0.5))

model.add(Dense(1))

model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam')

model.fit(features_train_vectorized, labels_train, batch_size=32, epochs=10)

labels_train_predclass = model.predict_classes(features_train_vectorized,batch_size=64)

labels_test_predclass = model.predict_classes(vect.transform(features_test).todense(),batch_size=64)

from sklearn.metrics import accuracy_score

print('Training accuracy is :', accuracy_score(labels_train, labels_train_predclass))
print('Testing accuracy is :', accuracy_score(labels_test,labels_test_predclass))























