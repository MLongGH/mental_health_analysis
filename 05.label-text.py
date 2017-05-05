import json

with open("./data/clean-tweets.json", 'r') as f:
    tweets = json.load(f)

print(len(tweets))

n = 0

for tweet in tweets:
    if "label" not in tweet:
        text = tweet["text"]
        print("-------------------")
        print(text)
        userLabel = input()
        userLabel = int(userLabel)
        tweet["label"] = userLabel
        n += 1
        if n == 100:  # label n tweets each time and save it to file
            break

with open("./data/all-labeled.json", "w") as outfile:
    json.dump(tweets, outfile)
