import tweepy
from ..config.settings import (
    TWITTER_API_KEY,
    TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET
)

class TwitterExtractor:
    def __init__(self):
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)
    
    def extract_mentions(self, query, count=100):
        tweets = []
        try:
            for tweet in tweepy.Cursor(self.api.search_tweets, q=query).items(count):
                tweets.append({
                    'id': tweet.id,
                    'text': tweet.text,
                    'user': tweet.user.screen_name,
                    'created_at': tweet.created_at,
                    'location': tweet.user.location,
                    'source': 'twitter'
                })
        except Exception as e:
            print(f"Error extracting tweets: {e}")
        
        return tweets 