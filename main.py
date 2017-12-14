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
from mutagen.mp3 import MP3

TOKEN = "499796086:AAEAJNzSVmgMqcAmC9fBur3KSywC3ZoU1o8"

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(chat_type)
    flavor = telepot.flavor(msg)
    summary = telepot.glance(msg, flavor=flavor)
    print(flavor, summary)
    if content_type == 'audio':
        audiofile = msg['audio']
        fileid = msg['audio']['file_id']
        flavor = telepot.flavor(msg)
        summary = telepot.glance(msg, flavor=flavor)
        print(flavor, summary)
        print(fileid)
        print(bot.getFile(file_id=fileid))
        os.system("wget https://api.telegram.org/file/bot" + TOKEN + "/" + bot.getFile(file_id=fileid)['file_path'] + " -O " + bot.getFile(file_id=fileid)['file_path'])
        audio = MP3(bot.getFile(file_id=fileid)['file_path'])
        length = audio.info.length * 0.33
        l2 = (audio.info.length * 0.33) + 60
        if audio.info.length > l2:
            os.system("ffmpeg -ss " + str(length) + " -t 60 -y -i " + bot.getFile(file_id=fileid)['file_path'] + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
        else:
            os.system("ffmpeg -ss 0 -t 60 -y -i " + bot.getFile(file_id=fileid)['file_path'] + " -strict -2 -ac 1 -map 0:a -codec:a opus -b:a 128k -vbr off output.ogg")
        sendVoice(chat_id, "output.ogg")
    if msg['text'].startswith("/start"):
        bot.sendMessage(chat_id,"Hello, please send me the name of the song or an URL from Soundcloud, YouTube and many more I have to convert :)")
    if msg['text'].startswith("http://") or msg['text'].startswith("https://"):
        bot.sendMessage(chat_id, "Please wait...I'm converting the URL to an MP3 file")
        filename = os.popen("node --no-warnings download-url.js " + msg['text']).read().rstrip()
        bot.sendMessage(chat_id, "Sending the file...")
        sendAudio(chat_id, filename)
        bot.sendMessage(chat_id,"Here you go!\nConsider a small donation at https://koyu.space/support if you like this bot :)")
    if chat_type == "private" and not msg['text'].startswith("/start") and not msg['text'].startswith("http"):
        try:
            bot.sendMessage(chat_id, "Please wait...I'm converting the song to an MP3 file")
            metadata = os.popen("node --no-warnings download.js " + msg['text']).read()
            cmd = 'youtube-dl --add-metadata -x --prefer-ffmpeg --extract-audio --write-thumbnail --embed-thumbnail -v --audio-format mp3 \
                --output "audio.%%(ext)s" %summary'%(metadata)
            os.system(cmd)
            url_data = urlparse.urlparse(metadata)
            query = urlparse.parse_qs(url_data.query)
            #video = query["v"][0]
            #os.system("wget -O audio.jpg http://i4.ytimg.com/vi/" + video + "/default.jpg")
            cmd = ["youtube-dl", "--get-title", "--skip-download", metadata]
            output = subprocess.Popen(cmd,stdout=subprocess.PIPE).communicate()[0]
            output = output.split("\n")[0]
            time.sleep(3)
            tag = eyed3.load("audio.mp3")
            try:
                title = tag.tag.title.split(" - ")[1]
                artist = tag.tag.title.split(" - ")[0]
                title = title.replace(artist + " - ","")
                try:
                    if not "Remix" in title and not "Mix" in title:
                        title = title.split(" (")[0]
                except:
                    pass
                try:
                    title = title.split(" [")[0]
                except:
                    pass
            except:
                title = tag.tag.title
                artist = tag.tag.artist
                #bot.sendMessage(chat_id,artist+" - "+title)
            os.system("sacad '" + artist + "' '" + title + "' 800 audio.jpg")
            os.system("lame -V 0 -b 128 --ti audio.jpg --tt \"" + title + "\" --ta \"" + artist + "\" audio.mp3")
            bot.sendMessage(chat_id,"Sending the file...")
            filename = artist.replace(" ", "_") + "-" + title.replace(" ", "_") + ".mp3"
            os.rename("audio.mp3.mp3", filename)
            sendAudio(chat_id,filename)
            os.system("rm -f *.mp3")
            bot.sendMessage(chat_id,"Here you go!\nConsider a small donation at https://koyu.space/support if you like this bot :)")
        except:
            bot.sendMessage(chat_id, "I couldn't find the song you're looking for. Maybe you could go find yourself a link and enter it here, so I know where to start from.")

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
