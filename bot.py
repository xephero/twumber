try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from twitter import Twitter
import discord
import re
import os

client = discord.Client()

tweet_id_pattern = re.compile(r"https?://(?:www\.)?(?:mobile\.)?twitter\.com/[^ ]+/status/(\d+)")
api = Twitter()

def get_emoji(digit):
    return str(digit) + u'\ufe0f\u20e3'

def get_emojis(number):
    if number >= 10:
        return ['\U0001f51f', '\u2795']

    return list(map(get_emoji, str(number)))

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    tweet_ids = tweet_id_pattern.findall(message.content)

    if len(tweet_ids) == 0:
        return

    num_pics = api.count_pics(tweet_ids)

    if num_pics < 2:
        return

    reactions = get_emojis(num_pics)

    for reaction in reactions:
        print(f"Adding reaction {reaction}")
        await message.add_reaction(reaction)

client.run(os.environ['DISCORD_TOKEN'])
