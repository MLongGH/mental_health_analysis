import json

with open("./data/dataset.json", 'r') as f:
    tweets = json.load(f)

results = []
for tweet in tweets:
    if tweet["label"] == 1:
        results.append(tweet["user_id"])

print(len(results))

results = list(set(results))

print(len(results))

with open("./data/user-id.json", "w") as outfile:
    json.dump(results, outfile)
