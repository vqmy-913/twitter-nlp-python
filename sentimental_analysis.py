import config
import pandas as pd
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions
from operator import itemgetter
import tweet_obtain

# References: 
# - https://cloud.ibm.com/apidocs/natural-language-understanding?code=python#features-examples
# - https://towardsdatascience.com/how-to-use-the-ibm-watson-tone-analyzer-to-perform-emotional-sentiment-analysis-in-python-d1d4ad022d0b
# - https://github.com/IBM/use-advanced-nlp-and-tone-analyser-to-analyse-speaker-insights
# - https://betterprogramming.pub/using-python-pandas-with-excel-d5082102ca27

natural_language_understanding = ""

"""
Authenticates developer credentials with Watson Natural Language Understanding API and
establishes a secure connection for developemnt
"""
def NLU_authentication() -> None:
    global natural_language_understanding
    ibm_watson_authenticator = IAMAuthenticator(config.IBM_WATSON_NLU_API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07', 
        authenticator=ibm_watson_authenticator
    )
    natural_language_understanding.set_service_url(config.IBM_WATSON_NLU_URL)

"""
Given a tweet, this function passes it to natural language understanding analyzer to analyze it, and
returns the sentiments and emotions associated with the particular tweet

@type tweet: str
@param tweet: tweet to be sentinally analysed
@rtype: list of a dict with keys keyword, sentiment, emotion
@returns keywords_sentiments_emotions:  data regarding the sentinal alaysis of the tweet 
"""
def analysing_sentiments(tweet: str) -> list:
    response = natural_language_understanding.analyze(
        language='en',
        text=tweet,
        features=Features(keywords=KeywordsOptions(sentiment=True, emotion=True, limit=10))).get_result()

    return analyse_keywords(sorted(response['keywords'],
            key=itemgetter('relevance'), reverse=True))

"""
Given the main keywords of the tweet, this function interprets the sentiment and emotion associated
with those keywords, and returns the sentiments and emotions associated with the particular main
keyword of the particular tweet

@type keywords: list
@param keywords: main keywords in the tweet
@rtype: list of a dict with keys keyword, sentiment, emotion
@returns keywords_sentiments_emotions:  data regarding the sentinal alaysis of the main keywords of
                                        the tweet 
"""
def analyse_keywords(keywords: list) -> list:
    keywords_sentiments_emotions = []

    for i in keywords:
        keywords_sentiments_emotions_buffer = {
            'keyword': i['text'],
            'sentiment': i['sentiment']['label'],
            'emotion': ''
        }

        maximum = i['emotion']['sadness']
        keywords_sentiments_emotions_buffer['emotion'] = 'sadness'

        if i['emotion']['joy'] > maximum:
            maximum = i['emotion']['joy']
            keywords_sentiments_emotions_buffer['emotion'] = 'joy'

        elif i['emotion']['fear'] > maximum:
            maximum = i['emotion']['fear']
            keywords_sentiments_emotions_buffer['emotion'] = 'fear'

        elif i['emotion']['disgust'] > maximum:
            maximum = i['emotion']['disgust']
            keywords_sentiments_emotions_buffer['emotion'] = 'disgust'

        elif i['emotion']['anger'] > maximum:
            maximum = i['emotion']['anger']
            keywords_sentiments_emotions_buffer['emotion'] = 'anger'

        keywords_sentiments_emotions.append(keywords_sentiments_emotions_buffer)

        return keywords_sentiments_emotions

"""
Performs the sentimental analysis on the tweets obtained for the keyword enetered by user.

Begins by establishing a secure connection, followed by retrieving the tweets from tweet_obtain.py,
loops through all the tweets by quarter, performs a sentimental analysis on each of them, and stores
the sentiment associated with the tweet in a nested list along with the quarter of the year that
tweet belongs to,this is followed by converting the data in nested list to a dataframe and finally
ends with writing the data of the dataframe to an enxcel sheet which will then be outputted on the
dashboard using Power BI
"""
def sentimental_analysis():
    NLU_authentication()

    tweets_dict = tweet_obtain.fetchTweets()

    tweet_sentiment = []
    for quarter in tweets_dict:
        for tweet in tweets_dict[quarter]:
            tweet_sentiment.append([quarter, tweet, analysing_sentiments(tweet)[0].get('sentiment')])
    
    sentiment_df = pd.DataFrame(tweet_sentiment, columns=['Quarter','Tweet','Sentiment'])
    
    sentiment_df.to_excel("Sentimental Analysis of Tweets.xlsx", index=False, sheet_name="sheet1")

# Calling the function to fetch tweets and start their sentimental analysis
sentimental_analysis()
