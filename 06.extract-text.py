import json

with open("./data/all-labeled.json", 'r') as f:
    tweets = json.load(f)

results = []
for tweet in tweets:
    temp = []
    new_text = tweet["text"].replace("\n", "")
    new_text = new_text.replace("\"", "")
    new_text = new_text.replace("\'", "")
    new_text = new_text.strip(' \t\n\r')
    if new_text:
        temp.append(new_text)
        temp.append(tweet["label"])
        results.append(temp)

print(len(results))

data = open("./data/all-text-label.csv", "w")
for text in results:
    new_text = text[0] + "," + str(text[1])
    data.write("%s\n" % new_text)
data.close()
