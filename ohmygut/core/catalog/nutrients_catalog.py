import pandas as pd

from ohmygut.core import constants
from ohmygut.core.catalog.catalog import Catalog, Entity, EntityCollection
from ohmygut.core.hash_tree import HashTree
from time import time


NUTRIENT_TAG = 'NUTRIENT'


class NutrientsCatalogNikogosov(Catalog):
    """Object holding nutrient ontology"""

    def __init__(self, path):
        self.path = path
        self.__nutrients_by_idname = None
        self.__idname_by_nutrient = None
        self.__hash_tree = None

    def initialize(self):
        t1 = time()
        constants.logger.info('Creating nutrients catalog...')

        data = pd.read_csv(self.path, sep="\t")
        self.__nutrients_by_idname = {idname: [] for idname in data['idname'].values}
        for index, record in data.iterrows():
            self.__nutrients_by_idname[record['idname']].append(record['name'])

        self.__idname_by_nutrient = {name: idname for idname, name_list in
                                     self.__nutrients_by_idname.items() for name in name_list}
        self.__hash_tree = HashTree(self.__idname_by_nutrient.keys())

        t2 = time()
        constants.logger.info('Done creating nutrients catalog. Total time: %.2f sec.' % (t2 - t1))

    def find(self, sentence_text):
        """ Uses previously generated hash tree to search sentence for nutrient names

        input:
            sentence: sentence to search for nutrient names

        returns:
            list of nutrient_names
        """
        nutr_names = self.__hash_tree.search(sentence_text)
        entities = EntityCollection([Entity(nutrient,
                                            self.__idname_by_nutrient[nutrient],
                                            NUTRIENT_TAG) for nutrient in nutr_names], NUTRIENT_TAG)
        return entities

    def get_list(self):
        nutrients = []
        for key, value in self.__nutrients_by_idname.items():
            nutrients.append(value[0])
        return nutrients
