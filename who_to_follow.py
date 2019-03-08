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
    analysis = TextBlob(tweet_obj.text)
    print(ident, analysis.sentiment)
    return {'sentiment': analysis.sentiment, 'text': tweet_obj.text}


def search(subject):
    public_tweets = api.search(subject)

    print('We received {} tweets'.format(len(public_tweets)))

    all = list()
    for tweet in public_tweets:
        all.append(show_tweet(tweet))
    return all


def list_trends(place):
    place = place.capitalize()
    trends = api.trends_available()
    names = dict()
    for trend in trends:
        names[trend['name']] = trend['woeid']

    if place in names.keys():
        woeid = names[place]
    else:
        raise ValueError('this place does not exist in IDs')

    local_trends = api.trends_place(woeid)
    names = list()
    for trend in local_trends:
        for key in trend['trends']:
            print(key)
            names.append(key['name'])
        print('-' * 20)
    return names


if __name__ == '__main__':
    api = authenticate()
    place = input('write the place for trend:')
    trends = list_trends(place)

    all_trend_mentions = list()
    for trend in trends:
        all_trend_mentions.append(search(trend))

    with open('out.json', 'w') as file:
        json.dump(all_trend_mentions, file)

