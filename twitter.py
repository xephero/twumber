import os
import requests

class Twitter:
    def __init__(self):
        self.BEARER = os.environ['TWITTER_API_BEARER']

    def request(self, tweet_ids):
        headers = {"Authorization": f"Bearer {self.BEARER}"}
        url = f"https://api.twitter.com/2/tweets?ids={','.join(tweet_ids)}&media.fields=type&expansions=attachments.media_keys"
        return requests.get(url, headers=headers).json()

    def count_pics(self, tweet_ids):
        response = self.request(tweet_ids)

        if 'includes' not in response:
            return 0

        return len(response['includes']['media'])