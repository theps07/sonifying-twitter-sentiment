#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 16:06:20 2022

@author: puruboii
"""
import pickle
import argparse
from textProcessing import preprocess_tweet
from nltk.sentiment import SentimentIntensityAnalyzer
import json
import tweepy
import time
from pythonosc.udp_client import SimpleUDPClient

# Authentication
consumerKey = "ObeA0sLDeuZtU8wv4ZYJQYbco"
consumerSecret = "EztlJirHnq4wJD9I4D54uYIBlqFPqCCtfvP1R5LtX3iBo9ZlOk"
accessToken = "1350237673483595779-y93iJNKYbteddLxVajYGEzhZHwlLvB"
accessTokenSecret = "Rya5y2swjoz9XxrOfnF26LJ3FMY0egHe1mtnXOrBuzz01"
sia = SentimentIntensityAnalyzer()


def sendOSC(data, oscMsg, ip="127.0.0.1", port=7300):
    # OSC
    client = SimpleUDPClient(ip, port)  # Create client
    client.send_message(oscMsg, data)  # send osc message
    # time.sleep(2)                     #time interval


def sendOSCs(data1, data2, data3, data4, data5, oscMsg1, oscMsg2,
             oscMsg3, oscMsg4, oscMsg5, ip="127.0.0.1", port=7300):
    # OSC
    client = SimpleUDPClient(ip, port)  # Create client
    client.send_message(oscMsg1, data1)  # send osc message
    client.send_message(oscMsg2, data2)  # send osc message
    client.send_message(oscMsg3, data3)  # send osc message
    client.send_message(oscMsg4, data4)  # send osc message
    client.send_message(oscMsg5, data5)  # send osc message
    time.sleep(4)  # time interval


def load_models():
    # Load the vectoriser.
    file = open('vectoriser-ngram-(1,2).pickle', 'rb')
    vectoriser = pickle.load(file)
    file.close()

    # Load the MNB Model.
    file = open('Sentiment-MNB.pickle', 'rb')
    MNBmodel = pickle.load(file)
    file.close()
    return vectoriser, MNBmodel


def predict(vectoriser, model, tweet):
    # Predict the sentiment
    textdata = vectoriser.transform([tweet])
    sentiment = model.predict(textdata)
    return sentiment


vectoriser, MNBmodel = load_models()


class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def streamTweets(self, hashTagList):
        # This handles Twitter auth and the connection to the Twitter Streaming API.
        stream = TweetsListener(
            consumerKey, consumerSecret, accessToken, accessTokenSecret)
        sendOSC(hashTagList[0], oscMsg="/soni/hashtag")
        stream.filter(track=hashTagList, languages=['en'])
        return True


class TweetsListener(tweepy.Stream):
    """
    A basic listener class that just listens for the tweets.
    """

    def on_data(self, data):
        try:
            msg = json.loads(data)
            # for tweet longer than 140 chars

            if "extended_tweet" in msg:
                tweet = msg['extended_tweet']['full_text']
                processed_tweet = preprocess_tweet(tweet)
                #sentiment = sia.polarity_scores(processed_tweet)
                sentiment = predict(vectoriser, MNBmodel, processed_tweet)
                followers = msg['user']['followers_count']

                sendOSCs(data1=tweet, data2=int(sentiment[0]),
                         data3=followers, data4=1, data5=1, oscMsg1="/soni/tweet",
                         oscMsg2="/soni/sentiment", oscMsg3="/soni/followers",
                         oscMsg4="/soni/average", oscMsg5="/soni/key")

                print('\033[4;3336;49mTweet\033[0;0m\n')
                print('\033[1;33;48m' + tweet + '\033[0;0m\n')
                print('\033[4;3336;49mSentiment:\033[0;0m\n')
                print('\033[1;36;48m' + str(sentiment[0]) + '\033[0;0m\n')
                print('\033[4;3336;49mFollowers:\033[0;0m\n')
                print(msg['user']['followers_count'])

            else:
                tweet = msg['text']
                processed_tweet = preprocess_tweet(tweet)
                #sentiment = sia.polarity_scores(processed_tweet)
                sentiment = predict(vectoriser, MNBmodel, processed_tweet)
                followers = msg['user']['followers_count']

                sendOSCs(data1=tweet, data2=int(sentiment[0]),
                         data3=followers, data4=1, data5=1, oscMsg1="/soni/tweet",
                         oscMsg2="/soni/sentiment", oscMsg3="/soni/followers",
                         oscMsg4="/soni/average", oscMsg5="/soni/key")

                print('\033[4;3336;49mTweet\033[0;0m\n')
                print('\033[1;33;48m' + tweet + '\033[0;0m\n')
                print('\033[4;3336;49mSentiment:\033[0;0m\n')
                print('\033[1;36;48m' + str(sentiment[0]) + '\033[0;0m\n')
                print('\033[4;3336;49mFollowers:\033[0;0m\n')
                print(msg['user']['followers_count'])

            return True

        except KeyboardInterrupt():
            return False

        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return False

    def on_error(self, status):
        print(status)
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Python script to scrape the Twitter API, conduct sentiment analysis and send data to Max/MSP.")
    parser.add_argument('--track', metavar='H', type=str,
                        nargs=1, help="Enter hashtag to track. (unspaced)")
    args = parser.parse_args()
    hashtag = vars(args)['track']
    stream = TwitterStreamer()
    stream.streamTweets(hashtag)
