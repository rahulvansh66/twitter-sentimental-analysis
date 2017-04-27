from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import json
import pandas as pd
import matplotlib as mpl

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import rcParams
from mpltools import style
from matplotlib import dates
from datetime import datetime
#import seaborn as sns
import time 
import os 
#from scipy.misc import imread
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import random


#Authentication
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

MAX_TWEETS = 1000
#This handles Twitter authentication and the connection to Twitter Streaming API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = API(auth, wait_on_rate_limit=True)


#Data extraction
search_text = raw_input("Enter that you want to search : ")

data = Cursor(api.search, q = search_text).items(MAX_TWEETS)

mozsprint_data = []
# You will use this line in production instead of this
# current_working_dir = os.path.dirname(os.path.realpath(__file__))
print ('Data is processing...')
current_working_dir = "./"
log_tweets = current_working_dir  + str(time.time()) + '_moztweets.txt'
with open(log_tweets, 'w') as outfile:
	for tweet in data:
		mozsprint_data.append(json.loads(json.dumps(tweet._json)))
		outfile.write(json.dumps(tweet._json))
		outfile.write("\n")
		print (tweet)

print ('Data is being Structured...')
#Create the dataframe we will use
tweets = pd.DataFrame()
# We want to know when a tweet was sent
tweets['created_at'] = map(lambda tweet: time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')), mozsprint_data)
# Who is the tweet owner
tweets['user'] = map(lambda tweet: tweet['user']['screen_name'], mozsprint_data)
# How many follower this user has
tweets['user_followers_count'] = map(lambda tweet: tweet['user']['followers_count'], mozsprint_data)
# What is the tweet's content
tweets['text'] = map(lambda tweet: tweet['text'].encode('utf-8'), mozsprint_data)
# If available what is the language the tweet is written in
tweets['lang'] = map(lambda tweet: tweet['lang'], mozsprint_data)
# If available, where was the tweet sent from ?
tweets['Location'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] != None else None, mozsprint_data)
# How many times this tweet was retweeted and favorited
tweets['retweet_count'] = map(lambda tweet: tweet['retweet_count'], mozsprint_data)
tweets['favorite_count'] = map(lambda tweet: tweet['favorite_count'], mozsprint_data)
#print tweets.head()
print ('The process for structurring of data is finished.')
list_of_original_tweets = [element for element in tweets['text'].values if not element.startswith('RT')]
print "Number of Original Tweets : " + str(len(list_of_original_tweets))
list_of_retweets = [element for element in tweets['text'].values if element.startswith('RT')]
print "Number of Retweets : " + str(len(list_of_retweets))

def plot_tweets_per_category(category, title, x_title, y_title, top_n=5, output_filename="plot.png"):
    tweets_by_cat = category.value_counts()
    fig, ax = plt.subplots()
    ax.tick_params(axis='x')
    ax.tick_params(axis='y')
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_title(title)
    tweets_by_cat[:top_n].plot(ax=ax, kind='bar')
    fig.savefig(output_filename)
    fig.show()


plot_tweets_per_category(tweets['lang']," by Language","Language","Number of Tweets",2000,"mozsprint_per_language.png")
plot_tweets_per_category(tweets['Location'], " by Location", "Location", "Number of Tweets", 2000,"mozsprint_per_location.png")
plot_tweets_per_category(tweets['user'], " active users", "Users", "Number of Tweets", 20,"mozsprint_users.png")
