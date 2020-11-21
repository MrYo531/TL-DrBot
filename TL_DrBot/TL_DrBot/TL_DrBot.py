"""
TL_DrBot - This twitter bot summarizes news articles for you!
           All you have to do is mention it when replying to a tweet that has a news article in it.

    This project was created for Codechella!

    Date Created - Nov 20, 2020
    Authors - Jason Zavala, Ashley Liu, Michelle Tai, and Kidus Yohannes
"""

import tweepy
import twitter_credentials as tc
import json
from get_url import get_url
from summary import summry


# Authentication setup
auth = tweepy.OAuthHandler(tc.CONSUMER_KEY, tc.CONSUMER_SECRET)
auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


# Overrides the stream listener to add logic to the on_data method,
# which is what gets called when a tweet is received.
class StreamListener(tweepy.StreamListener):
    def on_data(self, status):
        # Defines the variables we need to use
        tweet = json.loads(status)
        tweet_username = tweet["user"]["screen_name"]
        parent_tweet_id = tweet["in_reply_to_status_id"]

        # Determines if the tweet was a reply from a news article or a stand alone mention
        if parent_tweet_id is not None:
            # Grabs the url from the parent tweet and summarizes it
            url = get_url(tc.BEARER_TOKEN, parent_tweet_id)
            # TODO: Handle stories that are too short. Right now we just return first 280cs
            summary = summry(url)
            summary = summary[:(280 - len(tweet_username) - 2)]

            # Replies to the original tweet with the summary
            print(summary)
            api.update_status(f"@{tweet_username} {summary}", in_reply_to_status_id=tweet["id"])

        else:
            # Replies to the tweet with help instructions
            print("No parent tweet.")
            api.update_status(f"@{tweet_username} \"help command\"", in_reply_to_status_id=tweet["id"])


def main():
    # Creates a connection to Twitter and listens for tweets mentioning the bot
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    bot_handle = "@TL_DrBot"
    stream.filter(track=[f'{bot_handle}'], is_async=True)

    print("Streaming from Twitter...")

    # Where to put this?
    # print("Streaming ended.")


if __name__ == '__main__':
    main()
