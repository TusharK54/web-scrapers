
import time
from bs4 import BeautifulSoup
from base import MaterialScraper

class InfoboxScraper(MaterialScraper):
    """
    A web scraper that can extract and save infobox data from Wikipedia entries.
    """

    def __init__(self):
        base_url = 'https://en.wikipedia.org'
        super().__init__(base_url)
        self.crawl_delay = 0

    def scrape(self, topic:str):

        total_time = time.time_ns() # Program metadata

        # Get infobox from page
        topic = topic.replace(' ', '_')
        page = self.session.get(self.base_url + '/wiki/' + topic)
        if not page:
            raise ValueError(page.url + ' page not found - ' + topic + ' is invalid')
        soup = BeautifulSoup(page.text, 'lxml')
        infobox = soup.find('table', {'class': 'infobox'})

        # Scrape data from infobox
        infobox_data = {}
        entries = infobox.find_all('tr')
        for entry in entries:
            entry_key = entry.find('th', {'scope': 'row'})
            if not entry_key:
                continue
            key = entry_key.get_text()

            # Extract entries and remove citations
            entry_value = entry.find('td')
            for ref in entry_value.find_all('sup', {'class': 'reference'}): 
                ref.decompose()
            value = entry_value.get_text()

            infobox_data[key] = value
            
        # Append data and update program metadata and log
        total_time = (time.time_ns() - total_time) * 10**-9
        self.add_entry(topic, infobox_data)
        self.logger.info(f'DONE scraping Wikipedia infobox on {topic} in {round(total_time, 5)} seconds')
