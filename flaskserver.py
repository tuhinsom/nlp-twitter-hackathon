import os
from flask import Flask, request, render_template, redirect, url_for, Response
from flask_restful import Resource, Api
import json
import numpy as np
import decimal
import string
import datetime as dttm
#import re
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import pandas as pd

from analysisutilities import analysis_utilities

import timeit
app = Flask(__name__)

api = Api(app)

CORS(app)
serverHost = 'localhost'
mongo_host = "localhost"
mongo_port = "27017"
mongo_user = "tweetnlp2018"
mongo_pass = "tweetnlp2018"
mongo_db_name = "tweetnlp2018db"

client = MongoClient("mongodb://"+mongo_user+":"+mongo_pass+"@"+mongo_host+":"+mongo_port)
db = client.tweetnlp2018db

consumer_key="XXX" #your consumer key here
consumer_secret="MMM" #your consumer secret key here
access_token="YYY" #your access token here
access_token_secret="ZZZ" #your access token secret here

@app.route('/tweetsearch')
def DeliverTweetSearchView():
	return render_template('view_tweet.html', name='')

@app.route('/tweetanalyze')
def DeliverTweetAnalysisView():
	return render_template('view_analyzetweet.html', name='')

@app.route('/')
def InitSearch():
	return render_template('index.html', name='')

import tweepy

class InitiateSearch(Resource):
	def post(self):
		return_val = {}
		json_dict = request.json
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)

		api = tweepy.API(auth)
                tweet_dump = []
                #since_id = p_since_id
		public_tweets = api.home_timeline()
		#print(public_tweets)
		for tweet in public_tweets:
		    if db.tweet_collection.find({"id":tweet.id}).count() == 0 :
		        doc= {"text":tweet.text,"created_at":tweet.created_at.isoformat(),"from_user":tweet.user.name,"profile_image_url":tweet.user.profile_image_url}

    		        tweet_dump.append( doc )
    		        #let us tokenize and preprocess the data before storing
    		        au = analysis_utilities()
    		        tokenized_tweet = au.preprocess(tweet.text, False)
    		        #lets eliminate the stopwords now as they dont count much of an importance
			text_tokens = au.eliminate_stopwords(tokenized_tweet)
                        text_counts = au.feed_text_counts(text_tokens)

    		        doc_collection= {"id":tweet.id,"text":tweet.text, "favorite_count":tweet.favorite_count, "text_tokens":text_tokens,"text_counts":text_counts, "created_at":tweet.created_at.isoformat(),"from_user":tweet.user.name,"profile_image_url":tweet.user.profile_image_url}

		        result = db.tweet_collection.insert_one(doc_collection)

		return tweet_dump


api.add_resource(InitiateSearch, '/searchprocess')

class AnalyzeFeed(Resource):
	def post(self):
		return_val = {}
		#receive data from datepicker for the date range for pulling historical data
		json_dict = request.json
		toDte=""
		fromDte=""
		findParam = {}
		if json_dict.get('toDte','NA')!='NA':
			toDte = json_dict.get('toDte')
		if json_dict.get('fromDte','NA')!='NA':
			fromDte = json_dict.get('fromDte')

		if toDte!='' and fromDte!='':
			findParam = {'created_at': {'$gte':fromDte,'$lt': toDte} }
		elif toDte!='' and fromDte=='':
			findParam = {'created_at': {'$lt': toDte} }
		elif toDte == '' and fromDte != '':
			findParam = {'created_at': {'$lt': fromDte} }



		# let us pull data from historical repo
		public_tweets_cur = db.tweet_collection.find( findParam )

                tweet_dump = []
		#print(public_tweets)
                if public_tweets_cur != False:
			au = analysis_utilities()


			for tweet in public_tweets_cur:
				#print(tweet)
				if tweet.get('text_tokens','NA')!='NA':
					text_tokens = tweet["text_tokens"]
				else:
					text_tokens = au.preprocess(tweet['text'], False)

				if tweet.get('favorite_count','NA')!='NA':
					favorite_count = tweet['favorite_count']
				else:
					favorite_count = 0

				#lets eliminate the stopwords now as they dont count much of an importance
				#text_tokens = au.eliminate_stopwords(text_tokens)
                                #text_counts = au.feed_text_counts(text_tokens)
				#doc= {"text":tweet['text'],"text_tokens":text_tokens,"text_counts":text_counts,"created_at":tweet['created_at'],"favorite_count":favorite_count, "from_user":tweet['from_user'],"profile_image_url":tweet['profile_image_url']}
				doc= {"id":tweet['id'],"created_at":tweet['created_at'],"favorite_count":favorite_count, "from_user":tweet['from_user'],"text":tweet['text']}
				tweet_dump.append( doc )

			df = pd.DataFrame(tweet_dump)
			#returning the dataframe is mime text/html
			tweet_dump = Response(df.to_html(classes ="tweet_dataframe"), mimetype='text/html')

		return tweet_dump

api.add_resource(AnalyzeFeed, '/analyzefeed')


class DrillAnalysis(Resource):
	def post(self):
		return_val = {}
		#receive data from datepicker for the date range for pulling historical data
		json_dict = request.json
		toDte=""
		fromDte=""
		findParam = {}
		if json_dict.get('pid','NA')!='NA':
			pid = json_dict.get('pid')
		if json_dict.get('puser','NA')!='NA':
			puser = json_dict.get('puser')


		if json_dict.get('toDte','NA')!='NA':
			toDte = json_dict.get('toDte')
		if json_dict.get('fromDte','NA')!='NA':
			fromDte = json_dict.get('fromDte')

		if toDte!='' and fromDte!='':
			findParam = {'created_at': {'$gte':fromDte,'$lt': toDte}, "from_user":puser }
		elif toDte!='' and fromDte=='':
			findParam = {'created_at': {'$lt': toDte}, "from_user":puser  }
		elif toDte == '' and fromDte != '':
			findParam = {'created_at': {'$lt': fromDte}, "from_user":puser  }



		# let us pull data from historical repo
		public_tweets_cur = db.tweet_collection.find( findParam )

                tweet_dump = []
		#print(public_tweets)
                if public_tweets_cur != False:
			au = analysis_utilities()


			for tweet in public_tweets_cur:
				#print(tweet)
				if tweet.get('text_tokens','NA')!='NA':
					text_tokens = tweet["text_tokens"]
				else:
					text_tokens = au.preprocess(tweet['text'], False)

				if tweet.get('favorite_count','NA')!='NA':
					favorite_count = tweet['favorite_count']
				else:
					favorite_count = 0

				#lets eliminate the stopwords now as they dont count much of an importance
				#text_tokens = au.eliminate_stopwords(text_tokens)
                                #text_counts = au.feed_text_counts(text_tokens)
				#doc= {"text":tweet['text'],"text_tokens":text_tokens,"text_counts":text_counts,"created_at":tweet['created_at'],"favorite_count":favorite_count, "from_user":tweet['from_user'],"profile_image_url":tweet['profile_image_url']}
				doc= {"id":tweet['id'],"created_at":tweet['created_at'],"favorite_count":favorite_count, "from_user":tweet['from_user'],"text":tweet['text']}
				tweet_dump.append( doc )

			df = pd.DataFrame(tweet_dump)
			#returning the dataframe is mime text/html
			tweet_dump = Response(df.to_html(classes ="tweet_dataframe"), mimetype='text/html')

		return tweet_dump

api.add_resource(DrillAnalysis, '/drillanalysis')

import datetime
def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host=serverHost, port=port)
