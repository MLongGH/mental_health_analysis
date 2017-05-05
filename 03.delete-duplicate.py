import json

with open("./data/depression.json", 'r') as f:
    tweets = json.load(f)

unique = {each['text']: each for each in tweets}.values()

tweets = list(unique)

with open("./data/unique-text.json", "w") as outfile:
    json.dump(tweets, outfile)
