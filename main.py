import json
from time import sleep

import tweepy
# from TwitterAPI import TwitterAPI
# api = TwitterAPI("a51HGNktVIS8WQdrg6j6FLNpZ","lMgG2ZhVSGTaqVYTybJCAPDSvvK6rHVVla3kz88FYWxyWYnF2Y","1148213677004382210-ylHKSsv4fZ0UX5Dla4EXksyRL3p3We","DV34b3uPR7fthB6FZrhqYJjSnfjBFgSnQ8B384I8MXZuV")
# r = api.request('statuses/home_timeline', {'count':1})
# for item in r.get_iterator():
#     if 'text' in item:
#         print(item)
from tweepy.streaming import StreamListener
from tweepy import Stream


class Listener(StreamListener):

    def on_status(self, status):

        try:
            json_str = json.dumps(status._json)
            json_dict = json.loads(json_str)
            if "retweeted_status" not in json_dict:
                if json_dict["in_reply_to_status_id"] is None and json_dict["in_reply_to_user_id_str"] is None:
                    print("Independent tweet")
                    if not json_dict["entities"]["urls"]:
                        print("no urls!")
                        if "media" in json_dict["entities"]:
                            print("may have pictures")
                            if not json_dict["entities"]["media"]:
                                print("just text!")
                        else:
                            print("just text!")
                    if json_dict['truncated'] == True:
                        text = json_dict["extended_tweet"]["full_text"]
                    else:
                        text = json_dict["text"]
                    print("[" + json_dict['user']['name'] + "]" + " " + text)
                    print("Full tweet status:" + str(status))
        except Exception as e:
            print("exceptiooon")
            print(e)

    def on_error(self, status_code):
        print(status_code)

auth = tweepy.OAuthHandler("a51HGNktVIS8WQdrg6j6FLNpZ","lMgG2ZhVSGTaqVYTybJCAPDSvvK6rHVVla3kz88FYWxyWYnF2Y")
auth.set_access_token("1148213677004382210-ylHKSsv4fZ0UX5Dla4EXksyRL3p3We","DV34b3uPR7fthB6FZrhqYJjSnfjBFgSnQ8B384I8MXZuV")
api = tweepy.API(auth)
followees = []
for followee in tweepy.Cursor(api.friends_ids).items():
    followees.append(str(followee))
print(followees)
while True:
    # for status in tweepy.Cursor(api.home_timeline).items(1):
    #     # process status here
    #     json_str = json.dumps(status._json)
    #     if "retweeted_status" not in json_str:
    #         print(status.text)
    # sleep(0.5)
    twitterStream = Stream(auth, Listener())
    twitterStream.filter(follow=followees)
