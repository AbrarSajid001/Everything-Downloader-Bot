#!/bin/bash
echo "Cleaning up..."
youtube-dl --rm-cache-dir
cd temp
rm -f -- *.mp3
rm -f *.video
rm -f output.ogg
rm -f audio.jpg
rm -f thumb.jpg
rm -f *.part
rm -f *.ytdl
rm -f *.mp4
rm -f audio.webm
rm -f file_*
cd ..
rm -f *.pyc
rm -f music/file_*
rm -f videos/file_*
rm -f file_*
echo "Done!"
