import json
import tweepy
from textblob import TextBlob

with open('credentials.json') as cred_file:
    credentials = json.load(cred_file)

auth = tweepy.OAuthHandler(credentials['consumer_key'],
                           credentials['consumer_secret'])

auth.set_access_token(credentials['access_token'],
                      credentials['access_token_secret'])

try:
    api = tweepy.API(auth)
except Exception as e:
    print('We got a error authenticating')
    print('your credentials.json are correct?')
    print('ERROR: {}'.format(e))

subject = input('Write the subject: ')
public_tweets = api.search(subject)

for tweet in public_tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
print("")
