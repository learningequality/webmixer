import unittest

from webmixer.utils import guess_scraper
from webmixer.scrapers.pages import wikipedia


class WikipediaTest(unittest.TestCase):
    url = 'https://en.wikipedia.org/wiki/Sushi'

    def test_wikipedia_scraper_detected(self):
        scraper = guess_scraper(self.url, scrapers=[wikipedia.WikipediaScraper])

        assert isinstance(scraper, wikipedia.WikipediaScraper)
