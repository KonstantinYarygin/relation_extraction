from ohmygut.core.catalog.catalog import Catalog, EntityCollection
from ohmygut.core.constants import logger


class DoNothingCatalog(Catalog):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag

    def find(self, sentence_text):
        return EntityCollection([])

    def get_list(self):
        return []

    def initialize(self):
        logger.info("created do nothing catalog")
