import config
import pandas as pd
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# References: 
# - https://cloud.ibm.com/apidocs/natural-language-understanding?code=python#features-examples

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
