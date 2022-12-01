#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 15 17:31:01 2022

@author: puruboii
"""

#utilities
import pickle
import numpy as np
import pandas as pd

#preprocessing
from textProcessing import preprocess_tweet

#sklearn
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report

#Importing the dataset
n = ['sentiment', 'ids', 'date', 'flag', 'user', 'tweet']
filename = 'training.1600000.processed.noemoticon.csv'
dataset = pd.read_csv('dataset/' + filename, sep=',', names=n, encoding='Latin-1')

#Removing the unnecessary columns.
dataset = dataset[['sentiment','tweet']]

#Replacing the values to ease understanding
dataset['sentiment'] = dataset['sentiment'].replace(4,1)
dataset['sentiment'] = dataset['sentiment'].replace(0,-1)

#Preprocessing Tweets
dataset['tweet'] = dataset['tweet'].apply(preprocess_tweet)

#Storing data in lists.
tweet, sentiment = list(dataset['tweet']), list(dataset['sentiment'])

#Splitting the data
X_train, X_test, y_train, y_test = train_test_split(tweet, sentiment, test_size=0.2, random_state=42)

#TF-IDF Vectoriser: converts a collection of raw documents to a matrix of TF-IDF features
vectoriser = TfidfVectorizer(ngram_range=(1,2), max_features=500000)
vectoriser.fit(X_train)


#Transforming the dataset
X_train = vectoriser.transform(X_train)
X_test  = vectoriser.transform(X_test)

#Function to evaluate model
def model_Evaluate(model):
    
    # Predict values for Test dataset
    y_pred = model.predict(X_test)

    # Print the evaluation metrics for the dataset.
    print(classification_report(y_test, y_pred))

#MultinomialNB Model
MNBmodel = MultinomialNB(alpha = 1)
MNBmodel.fit(X_train, y_train)
model_Evaluate(MNBmodel)

#Saving the models
with open('vectoriser-ngram-(1,2).pickle','wb') as file:
    pickle.dump(vectoriser, file)
    
with open('Sentiment-MNB.pickle','wb') as file:
    pickle.dump(MNBmodel, file)






