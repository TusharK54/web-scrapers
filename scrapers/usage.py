
from cornell import *
from billboard import *
from github import *
from wikipedia import *

import logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    scraper = InfoboxScraper()
    #scraper.scrape('Albert_Einstein')
    #scraper.scrape('Jawaharlal_Nehru')
    #scraper.write('infobox')

    txt = scraper.get_robots_txt()
    print(txt)