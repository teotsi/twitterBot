import json

import praw
import tweepy
from tweepy import Stream
# from TwitterAPI import TwitterAPI
# api = TwitterAPI("a51HGNktVIS8WQdrg6j6FLNpZ","lMgG2ZhVSGTaqVYTybJCAPDSvvK6rHVVla3kz88FYWxyWYnF2Y","1148213677004382210-ylHKSsv4fZ0UX5Dla4EXksyRL3p3We","DV34b3uPR7fthB6FZrhqYJjSnfjBFgSnQ8B384I8MXZuV")
# r = api.request('statuses/home_timeline', {'count':1})
# for item in r.get_iterator():
#     if 'text' in item:
#         print(item)
from tweepy.streaming import StreamListener

reddit = praw.Reddit('NBATwitterBot', user_agent='nba bot agent')


class Listener(StreamListener):

    def on_status(self, status):

        try:
            json_str = json.dumps(status._json)
            json_dict = json.loads(json_str)
            if "retweeted_status" not in json_dict:
                if json_dict["in_reply_to_status_id"] is None and json_dict["in_reply_to_user_id_str"] is None:
                    print("Independent tweet")
                    if "extended_tweet" in json_dict:
                        final_dict = json_dict["extended_tweet"]
                    else:
                        final_dict = json_dict
                    if not final_dict["entities"]["urls"]:
                        print("no urls!")
                        if "media" in final_dict["entities"]:
                            print("may have pictures")
                            if not final_dict["entities"]["media"]:
                                print("just text!")
                        else:
                            print("just text!")
                    if json_dict['truncated']:
                        text = json_dict["extended_tweet"]["full_text"]
                    else:
                        text = json_dict["text"]
                    title = "[" + json_dict['user']['name'].split(" ")[1] + "]"+text
                    url = "twitter.com/"+json['user']['screen_name']+"/"+json_dict['id']
                    print("[" + json_dict['user']['name'].split(" ")[1] + "]"+text)
                    print("url: "+url)
                    print("Full tweet status:" + json.dumps(status._json, indent=4))
                    reddit.subreddit('reddit_api_test').submit(title, url=url)
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
    # for status in tweepy.Cursor(api.home_timeline).items(1):
    #     # process status here
    #     json_str = json.dumps(status._json)
    #     if "retweeted_status" not in json_str:
    #         print(status.text)
    # sleep(0.5)
    twitterStream = Stream(auth, Listener())
    twitterStream.filter(follow=followees)
