import json
import re


def cleanTweet(tweepyTweet):
    text=tweepyTweet["text"]
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)  # no emoji
    text = re.sub(r"@\w*\s*", "", text)
    text = text.strip(' \t\n\r')  # some seems like white space but can't be striped, they are emoji icons
    text = re.sub(r'[^\x00-\x7F]+', " ", text) # filter out hebrew chat as "\u05d8"
    return text


with open("./data/unique-text.json", 'r') as f:
    tweets = json.load(f)

print(len(tweets))

print(tweets[0])

print(type(tweets))


for tweet in tweets:
    tweet["text"]=cleanTweet(tweet)


for tweet in tweets:
    if tweet["text"] == "":
        tweets.remove(tweet)

for tweet in tweets:
    if tweet["text"] == " ":
        tweets.remove(tweet)

print(len(tweets))

with open("./data/clean-tweets.json", "w") as outfile:
    json.dump(tweets, outfile)

