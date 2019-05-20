# secrets
consumer_key = 'qoP626mqHzOS8STg4UUHv90BA'
consumer_secret = '8CFxe7Irehu73CSbxMiLLBjlvB0ncC2vsIlYV7UN25srgSqw0i'
access_token = '980573350299881472-hatER1wJGoy4JxKq7N7bICHzXJC5yN3'
access_secret = 'RU3S3bVybvbxWE0zWF8sbvJ571JhQr3YFlekcnPyFfb7e'
# bots
import random
from io import BytesIO
import requests
import tweepy
from PIL import Image
from PIL import ImageFile

# from secrets import *

ImageFile.LOAD_TRUNCATED_IMAGES = True
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


def tweet_image(url, username, status_id):
    filename = 'temp.png'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        i = Image.open(BytesIO(request.content))
        i.save(filename)
        scramble(filename)
        api.update_with_media('scramble.png', status='@{0}'.format(username), in_reply_to_status=status_id)
    else:
        print("unable to download image")


def scramble(filename):
    BLOCKLEN = 64
    img = Image.open(filename)
    width, height = img.size
    xblock = width // BLOCKLEN
    yblock = height // BLOCKLEN
    blockmap = [(xb * BLOCKLEN, yb * BLOCKLEN, (xb + 1) * BLOCKLEN, (yb + 1) * BLOCKLEN)
                for xb in range(xblock) for yb in range(yblock)]
    shuffle = list(blockmap)
    random.shuffle(shuffle)
    result = Image.new(img.mode, (width, height))
    for box, sbox in zip(blockmap, shuffle):
        crop = img.crop(sbox)
        result.paste(crop, box)
    result.save('scramble.png')


class BotStreamer(tweepy.StreamListener):
    def on_status(self, status):
        username = status.user.screen_name
        status_id = status.id

        if 'media' in status.entities:
            for image in status.entities['media']:
                tweet_image(image['media_url'], username, status_id)


myStreamListener = BotStreamer()
stream = tweepy.Stream(auth, myStreamListener)
stream.filter(track=['@ShangshangH'])