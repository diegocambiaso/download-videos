#!/usr/bin/env python
# coding = utf8
#
# Copyright (C) 2023, Diego Cambiaso
# GNU General Public License v3.0

# Version: 2

'''
This script is for educational purposes and will let you download a video.
'''

__version__ = 2

from pytube import YouTube
import pyperclip as pc

def DownloadVideo(url):
    try:
        youtubeObject = YouTube(url)
        youtubeObject = youtubeObject.streams.get_highest_resolution()
        print("Downloading...")
        youtubeObject.download()
    except(OSError, RuntimeError, ValueError):
        print("An error has occurred")
    except Exception as e:
        print("An error has ocurred.")
        e.add_note("Unknowed error trying donwloading the video")
        print("Error: ", e)
    except KeyboardInterrupt:
        print("Stoped by the user")
    else:
        print("Download is completed successfully")

if __name__ == "__main__":
    print("Download Video")
    print("-"*20)
    
    resp = "youtube.com" in pc.paste()
    
    if resp:
        url = pc.paste()
        print(f"Do you want to download: {url}")
        a = input("Y/n: ")
        if a.upper() == "Y":
            DownloadVideo(url)
    else:
        url = input("Write (or ctrl+v) the video URL: ")
        DownloadVideo(url)
    
    print("Finished")
    
