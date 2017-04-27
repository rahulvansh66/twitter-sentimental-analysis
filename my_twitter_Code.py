import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from textblob import TextBlob
import csv
import pygal
import once_more

def set_up():
    consumer_key = ''

    consumer_secret = ''

    access_token = ''
    access_token_secret = ''

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


def analyse_tweets(search_item):
    positive_count, negative_count, neutral_count = (0, 0, 0)

    public_tweets = set_up().search(search_item, count=1000)

    with open('twitter_sentiment.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["Sl.No", "Author", "Tweets", "Tweet_Type"])

        for i, tweets in enumerate(public_tweets):
           
            analysis = TextBlob(tweets.text)
            author = tweets.user.screen_name
            
            polarity = analysis.sentiment.polarity
            row_to_add = str(i+1) + ',' + tweets.text + ',' + author + ','
            #print type(row_to_add)
            new_row_to_add = (row_to_add.encode("utf-8"))
            #print type(new_row_to_add)
            """
            input_data = "UTF-16"
            output_data = "ASCII"
            unicode_data = unicode_file.read().decode(input_data)
            """            
            
            if polarity > 0:
                positive_count += 1
                f.write(new_row_to_add + 'Positive')
                f.write('\n')
            elif polarity == 0:
                neutral_count += 1
                f.write(new_row_to_add + 'Negative')
                f.write('\n')
            else:
                negative_count += 1
                f.write(new_row_to_add + 'Neutral')
                f.write('\n')
                
       

    return positive_count, negative_count, neutral_count


if __name__ == '__main__':
    
    #search_data_name=raw_input("Enter keyword that you want to search : ")
    print ('Please wait for few minutes your report is generating.....')
    search_term = once_more.search_text
    p_count, neg_count, neu_count = analyse_tweets(search_term)
    p = pygal.Pie(inner_radius=0.4)
    p.title = 'Tweets based on search term: ' + str(search_term) + ' (in %)'
    p.add('Positive Tweets', p_count)
    p.add('Neutral Tweets', neu_count)
    p.add('Negative Tweets', neg_count)
    p.render()
    p.render_to_file('tweets.svg')
    print "Process has been finished, your file is ready, now you can check it :) "
