import logging

class Logger:
    def __init__(self):
        self.logger = logging.getLogger("scraping_nlp_backend")

    def log(self, message):
        self.logger.info(message)
    