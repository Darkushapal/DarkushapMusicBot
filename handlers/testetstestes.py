import yt_dlp

url = "https://www.youtube.com/watch?v=RYCR55P99yg"

options = {'format': "ba"}

with yt_dlp.YoutubeDL(options) as ydl:
    ydl.download(url)

