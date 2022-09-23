import tweepy as tw
import pandas as pd
import datetime as dt
import config

auth = tw.OAuthHandler(config.TWEETY_API_KEY, config.TWEETY_API_SECRET)
api = tw.API(auth, wait_on_rate_limit=True)

def populateDataframe(tweets_copy):
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
                                                'user_location': tweet.user.location,
                                                'user_description': tweet.user.description,
                                                'user_verified': tweet.user.verified,
                                                'date': tweet.created_at,
                                                'text': text, 
                                                'hashtags': [hashtags if hashtags else None],
                                                'source': tweet.source})])

        tweets_df = tweets_df.reset_index(drop=True) # rate limit, tweepy might sleep for 10 minutes

    return tweets_df

# view the dataframe
#def viewDataframe(df):
    #tweets_df.columns # user_name, user_location, user_description, user_verified, date, text, hashtags, source
    #tweets_df.shape

def addQuarter(df):
    df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
    # add new column 'quarter'
    df['quarter'] = df['date'].dt.to_period('Q')

def dataframeToDict(tweets_df):

    tweets_df_small = tweets_df.iloc[:,[8,5]]
    tweets_df_small['quarter'] = tweets_df_small['quarter'].astype(str) # i ran this twice

    tweets_dict = {}
    for quarter in tweets_df_small['quarter']:
        tweets_dict[quarter] = []
        for tweet in tweets_df_small['text']:
            tweets_dict[quarter].append(tweet)
    
    return tweets_dict

# get tweets from the API
def fetchTweets():
    search_query = "retail technology -filter:retweets"
    tweets = tw.Cursor(api.search_tweets,
                q=search_query,
                lang="en").items(10) # adjust no. of tweets here!

    # store the API responses in a list
    tweets_copy = []
    for tweet in tweets:
        tweets_copy.append(tweet)

    # print("Total Tweets fetched:", len(tweets_copy))

    # intialize and populate the dataframe
    tweets_df = populateDataframe(tweets_copy)

    # classify tweets in quarters
    addQuarter(tweets_df)

    # print(tweets_df)
    
    # change dataframe into dictionary
    tweets_dict = dataframeToDict(tweets_df)

    
    # result: return tweets in a dictionary
        # "Quarter 1 2020" : [tweet1, tweet2, tweet3 ...]
        # "Quarter 2 2020" : [tweet1, tweet2, tweet3 ...]
    return tweets_dict

fetchTweets()
