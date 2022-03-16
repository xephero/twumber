import os
import requests

class Twitter:
    def __init__(self):
        self.BEARER = os.environ['TWITTER_API_BEARER']

    def request(self, tweet_ids):
        headers = {"Authorization": f"Bearer {self.BEARER}"}
        url = f"https://api.twitter.com/2/tweets?ids={','.join(tweet_ids)}&media.fields=type&expansions=attachments.media_keys,referenced_tweets.id"
        return requests.get(url, headers=headers).json()

    def get_tweet_data(self, tweet_ids):
        return self.request(tweet_ids)

    def count_pics(self, all_tweets):
        if 'includes' not in all_tweets:
            return 0

        tweet_pics = 0

        for single_tweet in all_tweets['data']:
            # pics in the linked tweet
            tweet_pics += len(single_tweet['attachments']['media_keys'])

            # pics in the qrt
            qrt_id = False

            # get the qrt id
            if 'referenced_tweets' in single_tweet:
                for ref_tweet in single_tweet['referenced_tweets']:
                    if ref_tweet['type'] == 'quoted':
                        qrt_id = ref_tweet['id']

            # count the media keys from includes
            if qrt_id:
                for included_tweet in all_tweets['includes']['tweets']:
                    if included_tweet['id'] == qrt_id:
                        tweet_pics += len(included_tweet['attachments']['media_keys'])

        return tweet_pics

    def is_video(self, tweet_data):
        for media in tweet_data['includes']['media']:
            if media['type'] == 'video' or media['type'] == 'animated_gif':
                return True;

        return False;
