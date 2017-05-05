import sys
import json
import tweepy


def shouldUseTweet(tweet):
    isRetweet = tweet.retweeted or "RT" in tweet.text
    return not isRetweet

# Returns a json like this:
# {
#   "hashtags":[
#     "FeelTheBern",
#     "BernieWouldHaveWon"
#   ],
#   "created_at":"Fri Mar 31 04:56:03 +0000 2017",
#   "timestamp":1490957763,
#   "id":847673825760133120,
#   "coords":[
#     -118.4804198,
#     34.022688
#   ],
#   "user_id":3260552160,
#   "urls":[
#     "https://t.co/W9DxShWqIL"
#   ],
#   "fav_count":0,
#   "user_name":"DonnyJHuber",
#   "rt_count":0,
#   "lang":"en",
#   "text":"Joe knows what's up. #FeelTheBern #BernieWouldHaveWon  "
# }

def cleanTweet(tweepyTweet):
    raw = tweepyTweet._json
    out = {}

    out["id"] = raw["id"]
    out["lang"] = raw["lang"]
    out["created_at"] = raw["created_at"]
    out["timestamp"] = int(tweepyTweet.created_at.timestamp())
    out["rt_count"] = raw["retweet_count"]
    out["fav_count"] = raw["favorite_count"]

    # user stuff
    out["user_id"] = raw["user"]["id"]
    out["user_name"] = raw["user"]["screen_name"]

    text = raw["text"]
    if "entities" in raw:
        entities = raw["entities"]
        if "hashtags" in entities and len(entities["hashtags"]) > 0:
            out["hashtags"] = []
            for hashtag in entities["hashtags"]:
                out["hashtags"].append(hashtag["text"])
        if "media" in entities and len(entities["media"]) > 0:
            for media in entities["media"]:
                text = text.replace(media["url"], "")
        if "urls" in entities and len(entities["urls"]) > 0:
            out["urls"] = []
            for url in entities["urls"]:
                out["urls"].append(url["url"])
                text = text.replace(url["url"], "")

    out["text"] = text

    if raw["coordinates"] != None:
        out["coords"] = raw['coordinates']
    elif raw["place"] != None:
        b_box = raw['place']['bounding_box']['coordinates'][0]
        coords = [0, 0]
        for coord in b_box:
            coords[0] = coords[0] + coord[0]
            coords[1] = coords[1] + coord[1]
        coords[0] /= len(b_box)
        coords[1] /= len(b_box)
        out["coords"] = [round(coords[0], 7), round(coords[1], 7)]

    return out

# Replace the API_KEY and API_SECRET with your application's key and secret.
auth = tweepy.AppAuthHandler('IoYrvpeHdD1rhkxhQgQQN0xIX', 'JSoBm1MTn7csCPhxyEVXNZJqcFo4nMXXgYJNe7iWcrWAfXTcKU')

api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

if (not api):
    print("Can't Authenticate")
    sys.exit(-1)

# Continue with rest of code

searchQuery = 'depression'  # this is what we're searching for
maxTweets = 100000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = 'depression.txt' # We'll store the tweets in a text file.


# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                if shouldUseTweet(tweet):
                    output = cleanTweet(tweet)
                    f.write(json.dumps(output) + "\n")
                    # f.write(json.dumps(tweet._json) + "\n")
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))