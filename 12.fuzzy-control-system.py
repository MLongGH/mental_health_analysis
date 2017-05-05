"""
Build fuzzy control system
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from requests import post, get
import os
import json

# Test tweet
sentences = "I think life is full of pain, and there is no way to avoid it. Recently, I just don't want to go out," \
            "and I would rather stay home by myself. I don't expect anything from others, sometimes I even don't expect anything" \
            "from myself.I just want to lay in bed, watching the clock running over my head. What's the point of hard work " \
            "and gain nothing in return. Taking a long nap is the only thing I want to do. In my dream, everything looks" \
            "perfect, and I prefer a really long nap."

# New Antecedent/Consequent objects hold universe variables and membership
# functions
sentiment = ctrl.Antecedent(np.arange(0, 11, 1), 'sentiment')
character = ctrl.Antecedent(np.arange(0, 11, 1), 'character')
depression = ctrl.Consequent(np.arange(0, 11, 1), 'depression')

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
sentiment['negtive'] = fuzz.trimf(sentiment.universe, [0, 0, 5])
sentiment['neutral'] = fuzz.trimf(sentiment.universe, [0, 5, 10])
sentiment['positive'] = fuzz.trimf(sentiment.universe, [5, 10, 10])

character['bad'] = fuzz.trimf(character.universe, [0, 0, 5])
character['normal'] = fuzz.trimf(character.universe, [0, 5, 10])
character['good'] = fuzz.trimf(character.universe, [5, 10, 10])

depression['low'] = fuzz.trimf(depression.universe, [0, 0, 5])
depression['normal'] = fuzz.trimf(depression.universe, [0, 5, 10])
depression['high'] = fuzz.trimf(depression.universe, [5, 10, 10])

# You can see how these look with .view()
sentiment.view()

character.view()

depression.view()

# Fuzzy rules
rule1 = ctrl.Rule(sentiment['negtive'] | character['bad'], depression['high'])
rule2 = ctrl.Rule(character['normal'], depression['normal'])
rule3 = ctrl.Rule(character['good'] | sentiment['positive'], depression['low'])

# create control system
depression_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

depression_predict = ctrl.ControlSystemSimulation(depression_ctrl)

"""
Pull overall sentiment analysis as input1 and pull personal charactors analysis result as input2,
use those two as fuzzy control system input
"""

"""
vader sentiment analysis score
"""

analyzer = SentimentIntensityAnalyzer()

vs = analyzer.polarity_scores(sentences)

input1 = ((vs["compound"] + 1) / 2) * 10
print("-------------------------------")
print("Sentiment score is: ")
print(input1)
print("-------------------------------")

"""
Liwc personal analysis score
"""

current_dir = os.path.dirname(os.path.realpath(__file__))

apikey = ""
apisecret = ""

header = {}
header['X-API-KEY'] = apikey
header['X-API-SECRET-KEY'] = apisecret
header['Content-type'] = 'application/json'
header['Accept'] = "application/json"

url = "https://app.receptiviti.com/v2/api/person"
# need to change the person_handle every time
payload = {"name": "userxxx", "gender": 0, "content": {"content_tags": [], "language": "english", "content_source": 8,
                                                       "language_content": sentences},
           "person_handle": "randomLetters"}

res = post(url, json=payload, headers=header)

result = (res.content).decode('utf-8')

json_result = json.loads(result)

Neuroticism = json_result["contents"][0]["receptiviti_scores"]["percentiles"]["neuroticism"]
Stressed = json_result["contents"][0]["receptiviti_scores"]["percentiles"]["stressed"]
Anxious = json_result["contents"][0]["receptiviti_scores"]["percentiles"]["anxious"]

input2 = ((Neuroticism + Stressed + Anxious) / 3) / 10

print("Character score is : ")
print(input2)
print("-------------------------------")

"""
Use fuzzy control system to predict
"""

depression_predict.input['sentiment'] = input1
depression_predict.input['character'] = input2

# Crunch the numbers
depression_predict.compute()

print("Depression prediction score is:")
print(depression_predict.output['depression'])
# depression.view(sim=depression_predict)
print("-------------------------------")
