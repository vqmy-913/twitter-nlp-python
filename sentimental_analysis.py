import json
import config
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
# import tweet_obtain

# Ref: https://cloud.ibm.com/apidocs/natural-language-understanding?code=python#features-examples

ibm_watson_authenticator = IAMAuthenticator(config.IBM_WATSON_API_KEY)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07', 
    authenticator=ibm_watson_authenticator
)
natural_language_understanding.set_service_url(config.IBM_WATSON_URL)

# tweets_dict = tweet_obtain.fetchTweets()

response = natural_language_understanding.analyze(
    html="<html><head><title>Fruits</title></head><body><h1>Apples and Oranges</h1><p>I love apples! I don't like oranges.</p></body></html>",
    features=Features(emotion=EmotionOptions(targets=['apples','oranges']))).get_result()

print(json.dumps(response, indent=2))

print('done')