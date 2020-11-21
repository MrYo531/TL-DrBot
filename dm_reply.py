import twitter_credentials 
import tweepy
from newspaper import Article
import nltk
nltk.download('punkt')

auth = tweepy.OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

last_dms = api.list_direct_messages(1)
count = 0
#check dm every _ minutes; if the list is different, check those new messages and their links
for messages in last_dms:
    print(messages)
    print("\n")
    count = count+1
print(count)
# user input will go into the url, which will be parsed from last dm
url = 'https://www.nytimes.com/2020/11/20/us/politics/georgia-trump-michigan-election.html?action=click&module=Spotlight&pgtype=Homepage' 

article = Article(url)
article.download()
article.parse()
article.nlp()
print(article.summary)

