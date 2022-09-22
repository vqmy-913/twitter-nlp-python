import tweepy as tw
import pandas as pd

api_key = "d3o8KDkIsCalgWGRG94Aiz1kD"
api_secret = "R4ctU7EXikABReWWRP5tuPsrfFgpwiHcitArEWRzFksX8Xe285"

auth = tw.OAuthHandler(api_key, api_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# get tweets from the API
search_query = "retail technology iot since:2015-01-01 -filter:retweets"
tweets = tw.Cursor(api.search_tweets,
              q=search_query,
              lang="en").items(10000)

# store the API responses in a list
tweets_copy = []
for tweet in tweets:
    tweets_copy.append(tweet)
print("Total Tweets fetched:", len(tweets_copy))

# intialize the dataframe
tweets_df = pd.DataFrame()

# populate the dataframe
for tweet in tweets_copy:
    hashtags = []
    try:
        for hashtag in tweet.entities["hashtags"]:
            hashtags.append(hashtag["text"])
        text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
    except:
        pass
    tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name, 
                                               'user_location': tweet.user.location,\
                                               'user_description': tweet.user.description,
                                               'user_verified': tweet.user.verified,
                                               'date': tweet.created_at,
                                               'text': text, 
                                               'hashtags': [hashtags if hashtags else None],
                                               'source': tweet.source}))
    tweets_df = tweets_df.reset_index(drop=True)

# show the dataframe
tweets_df.head()
