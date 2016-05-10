import re
from time import time

import pandas as pd

from ohmygut.core import constants
from ohmygut.core.catalog.catalog import Catalog, Entity, EntityCollection
from ohmygut.core.hash_tree import HashTree

DISEASE_TAG = 'DISEASE'


class DiseasesCatalog(Catalog):
    def get_list(self):
        pass

    def __str__(self):
        return "diseases catalog"

    def __init__(self, diseases_csv_path):
        self.disease_dictionary = {}
        self.hash_tree = None
        self.diseases_csv_path = diseases_csv_path

    def initialize(self):
        t1 = time()
        constants.logger.info('Creating diseases catalog...')

        data = pd.read_csv(self.diseases_csv_path, sep="\t")
        data = data[['id', 'name']]
        data_dict = data.to_dict("records")
        for row in data_dict:
            self.disease_dictionary[row['name']] = row['id']
        self.hash_tree = HashTree(self.disease_dictionary.keys())

        t2 = time()
        constants.logger.info('Done creating diseases catalog. Total time: %.2f sec.' % (t2 - t1))

    def find(self, sentence_text):
        """ Uses previously generated hash tree to search sentence for nutrient names

        input:
            sentence: sentence to search for nutrient names

        returns:
            list of nutrient_names
        """
        diseases_names = self.hash_tree.search(sentence_text)
        entities = EntityCollection([Entity(name,
                                            self.disease_dictionary[name],
                                            DISEASE_TAG) for name in diseases_names], DISEASE_TAG)
        return entities
