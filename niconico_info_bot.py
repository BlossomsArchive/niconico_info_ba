# coding: utf-8

import feedparser
from misskey import Misskey
from atproto import Client, models
import os
import time


f = open("niconico_info_feed.txt", "r")
old_up = f.read()
f.close()

entries = feedparser.parse(
    'https://blog.nicovideo.jp/niconews/index.xml')['entries']

i = 0
try:
    new_up = entries[0]['published']
    while (True):
        if entries[i]['published'] == old_up:
            g = open("niconico_info_feed.txt", "w")
            g.write(new_up)
            g.close()
            print("↑ここまでが新着↑")
            break

        else:
            title = entries[i]['title']
            page_url = entries[i]['link']

            post_text = "【ニコニコインフォ新着】\n"+title+"\n"+page_url

            # Misskey
            misskey_address = os.environ.get("MISSKEY_SERVER_ADDRESS")
            misskey_token = os.environ.get("MISSKEY_TOKEN")
            api = Misskey(misskey_address)
            api.token = misskey_token
            api.notes_create(text=post_text)

            # Bluesky
            bluesky = Client()
            bluesky.login(str(os.environ.get("BLUESKY_MAIL_ADDRESS")),str(os.environ.get("BLUESKY_PASSWORD")))
            bluesky.send_post(post_text)
            print(post_text+"\n-----------------------------------------------")
            time.sleep(10)

            i += 1
except:
    h = open("niconico_info_feed.txt", "w")
    h.write(new_up)
    h.close
