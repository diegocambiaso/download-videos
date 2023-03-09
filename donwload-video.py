from pytube import YouTube

def DownloadVideo(url):
    try:
        youtubeObject = YouTube(url)
        youtubeObject = youtubeObject.streams.get_highest_resolution()
        print("Downloading...")
        youtubeObject.download()
        print("Download is completed successfully")
    except:
        print("An error has occurred")

if __name__ == "__main__":
    print("Download Video")
    print("-"*20)
    
    url = input("Write (or ctrl+v) the video URL: ")
    DownloadVideo(url)

    print("Finished")
