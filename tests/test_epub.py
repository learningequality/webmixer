import os
import unittest

import webmixer.reporting as reporting
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
        assert len(reporting.session_reporter.file_links) == 5
        for filename in reporting.session_reporter.file_links:
            file_links = reporting.session_reporter.file_links[filename]
            for status in file_links:
                assert status in reporting.LINK_STATUSES
                assert status != reporting.LINK_ERROR
