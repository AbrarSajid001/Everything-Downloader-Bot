#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys
import time
import telepot
import requests
import os
import re
import requests
import subprocess
import urlparse
import time
import re
import eyed3
import random
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

reload(sys)
sys.setdefaultencoding("utf-8")

TOKEN = ""
f = open("random.txt", "w+")
f.write(str(random.randint(20,30)))
f.close()

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(chat_type)
    flavor = telepot.flavor(msg)
    summary = telepot.glance(msg, flavor=flavor)
    print(flavor, summary, chat_type)
    f = open("random.txt", "r")
    rnumber = int(f.read())
    f.close()
    if content_type == 'audio':
        audiofile = msg['audio']
        fileid = msg['audio']['file_id']
        flavor = telepot.flavor(msg)
        summary = telepot.glance(msg, flavor=flavor)
        print(flavor, summary)
        print(fileid)
        print(bot.getFile(file_id=fileid))
        filename = bot.getFile(file_id=fileid)['file_path']
        os.system("wget https://api.telegram.org/file/bot" + TOKEN + "/" + filename + " -O " + filename)
        if ".mp3" in filename:
            audio = MP3(filename)
            length = audio.info.length * 0.33
            l2 = (audio.info.length * 0.33) + 60
        if ".m4a" in filename:
            audio = MP4(filename)
            length = audio.info.length * 0.33
            l2 = (audio.info.length * 0.33) + 60
        if audio.info.length > l2:
            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
        else:
            os.system("ffmpeg -ss 0 -t 60 -y -i " + filename + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vn output.ogg")
        sendVoice(chat_id, "output.ogg")
    if content_type == "text":
        if msg['text'].startswith("/conv http://") or msg['text'].startswith("/conv https://") and not chat_type == "channel":
            bot.sendMessage(chat_id, "Please wait...I'm converting the URL to an MP3 file")
            try:
                url = msg['text'].split("/conv ")[1]
                filename = subprocess.Popen("node --no-warnings download-url.js \"" + url + "\"", stdout=subprocess.PIPE, shell=False).stdout.read()
                bot.sendMessage(chat_id, "Sending the file...")
                sendAudio(chat_id, filename)
                audio = MP3(filename)
                length = audio.info.length * 0.33
                l2 = length + 60
                if audio.info.length > l2:
                    os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                else:
                    os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                    sendVoice(chat_id, "output.ogg")
                    bot.sendMessage(chat_id,"Here you go!")
            except Exception, e:
                bot.sendMessage(chat_id, "Uh-oh, something bad happened. Note that Telegram limits bot uploads to 50MB. Otherwise contact @Sommerlichter for further assistance.\n\n```\n" + str(e) + "\n```", "Markdown")
        else:
            if "😂" in msg['text']:
                count = len(msg['text'].split("😂")) - 1
                f = open("counters/joy.txt", "r")
                s = f.read()
                f.close()
                if s == "":
                    s = "0"
                sum = int(count) + int(s)
                f = open("counters/joy.txt", "w")
                f.write(str(sum))
                f.close()
                if sum % rnumber == 0:
                    bot.sendMessage(chat_id, "😂 level is now: " + str(sum))
            if "bro" in msg['text']:
                count = len(msg['text'].split("bro")) - 1
                f = open("counters/bro.txt", "r")
                s = f.read()
                f.close()
                if s == "":
                    s = "0"
                sum = int(count) + int(s)
                f = open("counters/bro.txt", "w")
                f.write(str(sum))
                f.close()
                if sum % rnumber == 0:
                    bot.sendMessage(chat_id, "bro level is now: " + str(sum))
            if "Hi" in msg['text']:
                count = len(msg['text'].split("Hi")) - 1
                f = open("counters/hi.txt", "r")
                s = f.read()
                f.close()
                if s == "":
                    s = "0"
                sum = int(count) + int(s)
                f = open("counters/hi.txt", "w")
                f.write(str(sum))
                f.close()
                if sum % rnumber == 0:
                    bot.sendMessage(chat_id, "Hi level is now: " + str(sum))
            if "lol" in msg['text']:
                count = len(msg['text'].split("lol")) - 1
                f = open("counters/lol.txt", "r")
                s = f.read()
                f.close()
                if s == "":
                    s = "0"
                sum = int(count) + int(s)
                f = open("counters/lol.txt", "w")
                f.write(str(sum))
                f.close()
                if sum % rnumber == 0:
                    bot.sendMessage(chat_id, "lol level is now: " + str(sum))
            if msg['text'].startswith("/start"):
                bot.sendMessage(chat_id,"Hello, please send me the name of the song or an URL from Soundcloud, YouTube and many more I have to convert :)")
            if chat_type == "private" and msg["text"].startswith("http"):
                bot.sendMessage(chat_id, "Please wait...I'm converting the URL to an MP3 file")
                try:
                    url = msg['text']
                    filename = subprocess.Popen("node --no-warnings download-url.js \"" + url + "\"", stdout=subprocess.PIPE, shell=False).stdout.read()
                    bot.sendMessage(chat_id, "Sending the file...")
                    sendAudio(chat_id, filename)
                    audio = MP3(filename)
                    length = audio.info.length * 0.33
                    l2 = length + 60
                    if audio.info.length > l2:
                        os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                    else:
                        os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                    sendVoice(chat_id, "output.ogg")
                    bot.sendMessage(chat_id,"Here you go!")
                except Exception, e:
                    bot.sendMessage(chat_id, "Uh-oh, something bad happened. Note that Telegram limits bot uploads to 50MB. Otherwise contact @Sommerlichter for further assistance.\n\n```\n" + str(e) + "\n```", "Markdown")
            if chat_type == "private" and not msg['text'].startswith("/start") and not msg['text'].startswith("http") and not msg['text'].startswith("/conv"):
                try:
                    bot.sendMessage(chat_id, "Please wait...I'm converting the song to an MP3 file")
                    metadata = subprocess.Popen("node --no-warnings download.js " + msg['text'], stdout=subprocess.PIPE, shell=False).stdout.read()
                    filename = subprocess.Popen("node --no-warnings download-url.js " + metadata, stdout=subprocess.PIPE, shell=False).stdout.read()
                    bot.sendMessage(chat_id, "Sending the file...")
                    sendAudio(chat_id, filename)
                    audio = MP3(filename)
                    length = audio.info.length * 0.33
                    l2 = (audio.info.length * 0.33) + 60
                    if audio.info.length > l2:
                        os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                    else:
                        os.system("ffmpeg -ss 0 -t 60 -y -i \"" + filename + "\" -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
                    sendVoice(chat_id, "output.ogg")
                    bot.sendMessage(chat_id,"Here you go!\nConsider a small donation at https://koyu.space/support if you like this bot :)")
                except:
                    bot.sendMessage(chat_id, "I cannot find the song you're looking for. Go find yourself a link and enter it here, so I know where to start from.")

def sendAudio(chat_id,file_name):
    url = "https://api.telegram.org/bot%s/sendAudio"%(TOKEN)
    files = {'audio': open(file_name, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

def sendVoice(chat_id,file_name):
    url = "https://api.telegram.org/bot%s/sendVoice"%(TOKEN)
    files = {'voice': open(file_name, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print('Listening ...')

while 1:
    time.sleep(10)
