
import time
from bs4 import BeautifulSoup
from base import DataScraper

class UserCommitsScraper(DataScraper):
    """
    A web scraper that can extract and save user commit data from the Github website.

    Dataset Features:
    -----------------

    """

    def __init__(self):
        base_url = 'https://github.com'
        features = ['Date', 'Repository', 'Commits']
        super().__init__(base_url, features)

    def scrape(self, username:str):
        """
        Extracts Github commit data for the given user.

        Parameters:
        -----------
        username (str) - The user whose Github commit data to scrape.
        """
        total_time = 0 # Program metadata

        user_page = self.session.get(self.base_url + '/' + username)
        if not user_page:
            raise ValueError(username + ' is not a valid user.')
        soup = BeautifulSoup(user_page.text, 'lxml')

        raw_year = soup.find_all('li', {'class': 'js-year-link'})
        print()


        
class UserRepositoriesScraper(DataScraper):

    pass

class RepositoryScraper(DataScraper):

    pass