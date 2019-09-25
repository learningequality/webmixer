import json
import logging

logger = logging.getLogger('WebMixer/Logs')


LINK_BROKEN = 'broken'
LINK_ERROR = 'error'
LINK_IGNORED = 'ignored'
LINK_PROCESSED = 'processed'
LINK_UNSUPPORTED = 'unsupported'

LINK_STATUSES = [
    LINK_BROKEN,
    LINK_ERROR,
    LINK_IGNORED,
    LINK_PROCESSED,
    LINK_UNSUPPORTED
]

class LinkReport:
    """
    Keeps a record of links encountered during scraping, along with how the link was
    handled and any issues or warnings encountered.
    """
    def __init__(self):
        self.current_file = None
        self.file_links = {}

    def export_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as output:
            json.dump(self.file_links, output, indent=4, ensure_ascii=False)

    def scraping_started(self, filename):
        logger.warning("Started scraping {}".format(filename))
        if not filename in self.file_links:
            self.file_links[filename] = {}

        self.current_file = self.file_links[filename]

    def scraping_finished(self, filename):
        logger.debug("Finished scraping {}".format(filename))
        self.current_file = None

    def link_processed(self, url, status, scraper=None, message=None, warnings=None):
        if self.current_file is None:
            logger.warning("link_processed called but current_file is not set. This event log will not be saved.")
            return

        if not status in LINK_STATUSES:
            raise KeyError("Unknown processing status {} found.".format(status))

        logger.debug(('Link processed: {}.'.format(url)))
        if message:
            logger.info(message)
        if warnings:
            logger.warning(','.join(warnings))
        if not status in self.current_file:
            self.current_file[status] = []
        data = {
            'url': url,
            'scraper': scraper,
            'message': message,
            'warnings': warnings
        }
        logger.debug("Adding data: {}".format(data))
        self.current_file[status].append(data)

session_reporter = LinkReport()
