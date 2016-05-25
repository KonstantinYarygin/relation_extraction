from time import time

from ohmygut.core.catalog.catalog import Catalog, Entity, EntityCollection
from ohmygut.core.constants import logger
from ohmygut.core.hash_tree import HashTree

DIET_TAG = "DIET"


class DietsCatalog(Catalog):
    def get_list(self):
        pass

    def __init__(self, tidy_csv_path):
        super().__init__()
        self.tidy_csv_path = tidy_csv_path
        self.__hash_tree = None
        self.__diets = None

    def initialize(self):
        t1 = time()
        logger.info('Creating diets catalog...')
        with open(self.tidy_csv_path) as file:
            diets = file.read().splitlines()

        self.__hash_tree = HashTree(diets)
        self.__diets = diets

        t2 = time()
        logger.info('Done creating diets catalog. Total time: %.2f sec.' % (t2 - t1))

    def find(self, sentence_text):
        diet_names = self.__hash_tree.search(sentence_text)

        entities = EntityCollection([Entity(name, 'noid', DIET_TAG) for name in diet_names], DIET_TAG)
        return entities
