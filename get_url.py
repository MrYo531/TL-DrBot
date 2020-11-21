import requests
import json


# Gets the embedded article url from the given tweet
# This uses v2 of the twitter API (v1 from tweepy was inconsistent)
def get_url(bearer_token, tweet_id):
    headers = {
        'Authorization': 'Bearer {}'.format(bearer_token),
    }

    params = (
        ('tweet.fields', 'entities'),
    )

    response = requests.get(f'https://api.twitter.com/2/tweets/{tweet_id}', headers=headers, params=params)
    tweet = json.loads(response.text)
    url = tweet["data"]["entities"]["urls"][0]["expanded_url"]
    return url
