import json
import tweepy
from textblob import TextBlob


def authenticate():
    with open('credentials.json') as cred_file:
        credentials = json.load(cred_file)

    auth = tweepy.OAuthHandler(credentials['consumer_key'],
                               credentials['consumer_secret'])

    auth.set_access_token(credentials['access_token'],
                          credentials['access_token_secret'])

    try:
        api = tweepy.API(auth)
        return api
    except Exception as e:
        print('We got a error authenticating')
        print('your credentials.json are correct?')
        print('ERROR: {}'.format(e))


def show_tweet(tweet_obj, identation=0):
    ident = '|{}'.format(' '*identation)
    print('-' * 20)
    print(ident, tweet_obj.text)
    analysis = TextBlob(tweet.text)
    print(ident, analysis.sentiment)
    return {'sentiment': analysis.sentiment, 'retweets': tweet_obj.retweeters}


def search():
    api = authenticate()
    subject = input('Write the subject: ')
    public_tweets = api.search(subject)

    print('We received {} tweets'.format(len(public_tweets)))

    all = list()
    for tweet in public_tweets:
        all.append(show_tweet(tweet))


if __name__ == '__main__':
    search()
