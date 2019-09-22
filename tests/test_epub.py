import os
import unittest

from webmixer.reporting import session_reporter
from webmixer.scrapers.pages.base import EPubScraper
from webmixer.utils import guess_scraper

this_dir = os.path.dirname(os.path.abspath(__file__))


class EPubTest(unittest.TestCase):
    epub_file = os.path.join(this_dir, 'files/epub/_proyectoedia_geografiaehistoria_epubs_feriahistoria_12_guiadidactica_feriahis.epub')

    def test_epub_detection(self):
        scraper = guess_scraper(self.epub_file)
        assert isinstance(scraper, EPubScraper)

    def test_epub_links(self):
        scraper = guess_scraper(self.epub_file)
        scraper.process()
        assert not session_reporter.file_links
