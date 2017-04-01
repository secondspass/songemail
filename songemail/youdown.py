import youtube_dl
from . import emailsender
from threading import Thread

ydl_opts = {
    'format': 'bestaudio/best',
    'forcetitle': True,
    'outtmpl': 'songs/%(title)s.%(ext)s', # the song is saved in songs dir as <title>.mp3
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }],
}


class downloadWorker(Thread):
    def __init__(self, url, to_address):
        Thread.__init__(self)
        self.url = url
        self.to_address = to_address
        self.songdict = {}

    def download_video(self):
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            self.songdict = ydl.extract_info(self.url, download=True)

    def run(self):
        self.download_video()
        title = self.songdict['title']
        emailsender.email_helper(title, self.to_address)
