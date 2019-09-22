import logging

logger = logging.getLogger('WebMixer/Logs')


class LinkReport:
    """
    Keeps a record of links encountered during scraping, along with how the link was
    handled and any issues or warnings encountered.
    """
    def __init__(self):
        self.current_file = None
        self.file_links = {}

    def scraping_started(self, filename):
        logger.warning("Started scraping {}".format(filename))
        if not filename in self.file_links:
            self.file_links[filename] = []

        self.current_file = self.file_links[filename]

    def scraping_finished(self, filename):
        logger.warning("Finished scraping {}".format(filename))
        self.current_file = None

    def link_processed(self, url, message=None, warnings=None):
        if self.current_file is None:
            logger.warning("link_processed called but current_file is not set. This event log will not be saved.")
            return

        logger.warning(('Link processed: {}.'.format(url)))
        if message:
            logger.info(message)
        if warnings:
            logger.warning(','.join(warnings))
        self.current_file.append((url, message, warnings))

session_reporter = LinkReport()
