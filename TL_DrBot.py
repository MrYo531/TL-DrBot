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
from summry import summry

# Authentication setup
auth = tweepy.OAuthHandler(tc.CONSUMER_KEY, tc.CONSUMER_SECRET)
auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


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
            summary = summry(url)

            # Split the summary into multiple tweets (in case it's longer than 280 characters)
            # A tweet can be at most 280 characters. We have to consider the length of the mention too.
            # (+ 2 to account for the @ symbol and the space after the username)
            summary_split = []
            split_size = 280 - (len(tweet_username) + 2)
            for index in range(0, len(summary), split_size):
                summary_split.append(summary[index:min(index+split_size, len(summary))])

            # For each split, tweet it as a reply to the previous tweet, creating a thread
            bot_twitter_id = "1329945307996594177"
            tweet_reply_to = tweet["id"]
            for summary_section in summary_split:
                api.update_status(f"@{tweet_username} {summary_section}", in_reply_to_status_id=tweet_reply_to)
                # Grabs the id of the tweet just tweeted and assigns it to be the next reply_id
                tweet = api.user_timeline(id=bot_twitter_id, count=1)[0]
                tweet = tweet._json
                tweet_reply_to = tweet["id"]

        else:
            # Replies to the tweet with help instructions
            api.update_status(f"Hi @{tweet_username} ! I see you've mentioned me but without a news article for me to summarize. UwU. "
                              f"Mention me when replying to a news article, yeah? <3 OwO", in_reply_to_status_id=tweet["id"])


def main():
    # Creates a connection to Twitter and listens for tweets mentioning the bot
    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    bot_handle = "@TL_DrBot"
    stream.filter(track=[bot_handle], is_async=True)

    print("Streaming from Twitter...")

    """# sending the direct message
    text = "This is a Direct Message."
    direct_message = api.send_direct_message("3182143332", text)
    print(direct_message.message_create['message_data']['text'])"""

    # Where to put this?
    # print("Streaming ended.")


if __name__ == '__main__':
    main()
