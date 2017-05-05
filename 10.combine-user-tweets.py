import json
import re

with open("./data/texts-by-id.json", 'r') as f:
    tweets = json.load(f)

with open("./data/combine-tweets.json", "w") as f:
    for tweet in tweets:
        text = "".join(tweet[1])
        text = re.sub(r'[^\x00-\x7F]+', " ", text)
        print("---------------")
        print(text)
        print("---------------")
        f.write(json.dumps(text) + '\n')
