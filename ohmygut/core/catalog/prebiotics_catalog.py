from time import time

from ohmygut.core.catalog.catalog import Catalog, Entity, EntityCollection
from ohmygut.core.constants import logger
from ohmygut.core.hash_tree import HashTree

PREBIOTIC_TAG = "PREBIOTIC"


class PrebioticsCatalog(Catalog):
    def __init__(self, tidy_csv_path):
        super().__init__()
        self.tidy_csv_path = tidy_csv_path
        self.__hash_tree = None
        self.__prebiotics = None

    def initialize(self):
        t1 = time()
        logger.info('Creating prebiotics catalog...')
        with open(self.tidy_csv_path) as file:
            prebiotics = file.read().splitlines()

        self.__hash_tree = HashTree(prebiotics)
        self.__prebiotics = prebiotics

        t2 = time()
        logger.info('Done creating prebiotics catalog. Total time: %.2f sec.' % (t2 - t1))

    def find(self, sentence_text):
        prebiotic_names = self.__hash_tree.search(sentence_text)

        entities = EntityCollection([Entity(name, 'noid', PREBIOTIC_TAG) for name in prebiotic_names], PREBIOTIC_TAG)
        return entities
