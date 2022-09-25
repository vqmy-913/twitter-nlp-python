import config
import pandas as pd
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions
from operator import itemgetter

# References: 
# - https://cloud.ibm.com/apidocs/natural-language-understanding?code=python#features-examples
# - https://towardsdatascience.com/how-to-use-the-ibm-watson-tone-analyzer-to-perform-emotional-sentiment-analysis-in-python-d1d4ad022d0b
# - https://github.com/IBM/use-advanced-nlp-and-tone-analyser-to-analyse-speaker-insights

natural_language_understanding = ""

"""
This function authenticates developer credentials with Watson Natural Language Understanding API and
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