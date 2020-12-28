
import pytube, time
from bs4 import BeautifulSoup
from base import Scraper

class VideoDownloader(Scraper):

    def __init__(self):
        base_url = 'https://www.youtube.com'
        super().__init__(base_url)
        self.streams = []

    def download(self, video_url, filename):
        self.streams, prev_streams = [], self.streams
        self.scrape(video_url)
        self.write(filename)
        self.streams = prev_streams

    def scrape(self, video_url):
        video = pytube.YouTube(video_url)
        print(video.streams.all())
        self.streams.append(video.streams.first())

    def write(self, filename) -> str:
        output_folder = '/videos'
        for stream in self.streams:
            stream.download(output_folder)

if __name__ == "__main__":
    download = VideoDownloader()
    download.download('https://www.youtube.com/watch?v=tGVh91cTJAg', 'temp')
