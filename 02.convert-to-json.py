import json

f = open("./data/depression.txt", "r")
doc_set = f.read().split('\n')
f.close()

res = []
for i in range(len(doc_set) - 1):
    res.append(json.loads(doc_set[i]))

with open("./data/depression.json", "w") as outfile:
    json.dump(res, outfile)
