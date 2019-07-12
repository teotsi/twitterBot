import json

import praw
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener

reddit = praw.Reddit('NBATwitterBot', user_agent='nba bot agent')


def submit_thread(dict):
    if dict['truncated']:
        text = dict["extended_tweet"]["full_text"]
    else:
        text = dict["text"]
    name = str(dict['user']['name'])
    title = "[" + name.split(" ")[1] + "]" + text
    url = "twitter.com/" + dict['user']['screen_name'] + "/status/" + str(dict['id'])
    print(title)
    print("url: " + url)
    reddit.subreddit('nba').submit(title, url=url)


class Listener(StreamListener):

    def on_status(self, status):

        try:
            json_str = json.dumps(status._json)
            json_dict = json.loads(json_str)
            if "retweeted_status" not in json_dict:
                if json_dict["in_reply_to_status_id"] is None and json_dict["in_reply_to_user_id_str"] is None:
                    # it is not a retweet or a reply
                    if "extended_tweet" in json_dict:
                        final_dict = json_dict["extended_tweet"]
                    else:
                        final_dict = json_dict
                    if not final_dict["entities"]["urls"]:  # no links to outside sources
                        if "media" in final_dict["entities"]:  # may have pictures
                            if not final_dict["entities"]["media"]:  # It only has text, thus it is eligible
                                submit_thread(json_dict)
                        else:  # It only has text, thus it is eligible
                            submit_thread(json_dict)
        except Exception as e:
            print("exceptiooon")
            print(e)

    def on_error(self, status_code):
        print(status_code)


auth = tweepy.OAuthHandler("a51HGNktVIS8WQdrg6j6FLNpZ", "lMgG2ZhVSGTaqVYTybJCAPDSvvK6rHVVla3kz88FYWxyWYnF2Y")
auth.set_access_token("1148213677004382210-ylHKSsv4fZ0UX5Dla4EXksyRL3p3We",
                      "DV34b3uPR7fthB6FZrhqYJjSnfjBFgSnQ8B384I8MXZuV")
api = tweepy.API(auth)
followees = []
for followee in tweepy.Cursor(api.friends_ids).items():
    followees.append(str(followee))
print(followees)
while True:
    twitterStream = Stream(auth, Listener())
    twitterStream.filter(follow=followees)
