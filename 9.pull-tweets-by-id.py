import tweepy  # https://github.com/tweepy/tweepy
import csv
import json
import re


def shouldUseTweet(tweet):
    isRetweet = tweet.retweeted or "RT" in tweet.text
    return not isRetweet


def cleanTweet(tweepyTweet):
    text = tweepyTweet.text.encode("utf-8")
    print("type of text extracted from raw[text] is : " + "\n")
    print(type(text))
    print(text)
    text = text.decode()
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)  # no emoji

    raw = tweepyTweet._json

    if "entities" in raw:
        entities = raw["entities"]
        if "media" in entities and len(entities["media"]) > 0:
            for media in entities["media"]:
                text = text.replace(media["url"], "")
        if "urls" in entities and len(entities["urls"]) > 0:
            for url in entities["urls"]:
                text = text.replace(url["url"], "")

    text = re.sub(r"@\w*\s*", "", text)

    text = text.strip(' \t\n\r')  # some seems like white space but can't be striped, they are emoji icons

    text = re.sub(r'[^\x00-\x7F]+', " ", text)  # filter out hebrew chat as "\u05d8"

    return text


# Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_all_tweets(id):
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(id=id, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(id=id, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    outtweets = []
    for tweet in alltweets:
        if shouldUseTweet(tweet):
            text = cleanTweet(tweet)
            if text:
                outtweets.append(text)
    return outtweets

    pass

# user-id.json has list of user ids
with open("./data/user-id.json", 'r') as f:
    tweets = json.load(f)

results = []

if __name__ == '__main__':
    # pass in the username of the account you want to download
    with open("./data/texts-by-id.json", "w") as f:
        for id in tweets:
            item = []
            item.append(id)
            item.append(get_all_tweets(id))
            f.write(json.dumps(item) + ',')

# when the code throw errors, mostly because for some user ID, I don't have authorization, so delete that ID,
# the code can keep running.
