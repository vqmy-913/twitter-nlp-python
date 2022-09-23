import tweepy as tw
import pandas as pd
import datetime as dt
from pprint import pprint

api_key = "GrD31hjfaqUZumgMWerT7BojE"
api_secret = "WrcoBU5OQR0439mgbrGzybuwMDwjQriM8NbqAMe7vaRK1MpMjz"

auth = tw.OAuthHandler(api_key, api_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# get tweets from the API
search_query = "retail technology -filter:retweets"
tweets = tw.Cursor(api.search_tweets,
              q=search_query,
              lang="en").items(10) # adjust no. tweets here!

# store the API responses in a list
tweets_copy = []
for tweet in tweets:
    tweets_copy.append(tweet)
print("Total Tweets fetched:", len(tweets_copy))

# intialize and populate the dataframe
tweets_df = pd.DataFrame()
for tweet in tweets_copy:
    hashtags = []
    try:
        for hashtag in tweet.entities["hashtags"]:
            hashtags.append(hashtag["text"])
        text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
    except:
        pass
    tweets_df = pd.concat([tweets_df,pd.DataFrame({'user_name': tweet.user.name, 
                                               'user_location': tweet.user.location,\
                                               'user_description': tweet.user.description,
                                               'user_verified': tweet.user.verified,
                                               'date': tweet.created_at,
                                               'text': text, 
                                               'hashtags': [hashtags if hashtags else None],
                                               'source': tweet.source})])
    tweets_df = tweets_df.reset_index(drop=True) # rate limit, tweepy might sleep for 10 minutes

# view the dataframe
#tweets_df.columns # user_name, user_location, user_description, user_verified, date, text, hashtags, source
#tweets_df.shape

# classify tweets in quarters
def addQuarter(df):
    df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
    # add new column 'quarter'
    df['quarter'] = df['date'].dt.to_period('Q')
addQuarter(tweets_df)

# change dataframe into dictionary
tweets_df_small = tweets_df.iloc[:,[8,5]]
tweets_df_small['quarter'] = tweets_df_small['quarter'].astype(str) # i ran this twice

tweets_dict = {}
for quarter in tweets_df_small['quarter']:
    tweets_dict[quarter] = []
    for tweet in tweets_df_small['text']:
        tweets_dict[quarter].append(tweet)

# print dictionary
pprint(tweets_dict)

# result: return tweets in a dictionary
    # "Quarter 1 2020" : [tweet1, tweet2, tweet3 ...]
    # "Quarter 2 2020" : [tweet1, tweet2, tweet3 ...]