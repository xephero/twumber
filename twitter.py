import os
import requests

class Twitter:
    def __init__(self):
        self.BEARER = os.environ['TWITTER_API_BEARER']

    def request(self, tweet_ids):
        headers = {"Authorization": f"Bearer {self.BEARER}"}
        url = f"https://api.twitter.com/2/tweets?ids={','.join(tweet_ids)}&media.fields=type&expansions=attachments.media_keys"
        return requests.get(url, headers=headers).json()

    def get_tweet_data(self, tweet_ids):
        return self.request(tweet_ids)

    def count_pics(self, tweet_data):
        if 'includes' not in tweet_data:
            return 0

        return len(tweet_data['includes']['media'])

    def is_video(self, tweet_data):
        for media in tweet_data['includes']['media']:
            if media['type'] == 'video':
                return True;

        return False;
