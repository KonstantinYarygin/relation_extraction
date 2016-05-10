from time import time

import pandas as pd

from ohmygut.core.catalog.catalog import Catalog
from ohmygut.core.catalog.catalog import Entity, EntityCollection
from ohmygut.core.constants import logger
from ohmygut.core.hash_tree import HashTree

FOOD_TAG = 'FOOD'


class UsdaFoodCatalog(Catalog):
    def get_list(self):
        return list(self.__food_data_frame['group'].drop_duplicates()) + list(self.__food_data_frame['name'])

    def __str__(self):
        return "usda food catalog"

    def __init__(self, food_file_path):
        super().__init__()
        self.food_file_path = food_file_path
        self.__hash_tree = None
        self.__food_dict = None
        self.__group_by_food_name = None
        self.__food_data_frame = None

    def initialize(self):
        t1= time()
        logger.info('Creating food catalog...')
        self.__food_data_frame = pd.read_table(self.food_file_path, sep=',')
        self.__food_dict = {food_group: [] for food_group in self.__food_data_frame['group'].values}
        for index, record in self.__food_data_frame.iterrows():
            self.__food_dict[record['group']].append(record['name'].strip())

        self.__group_by_food_name = {food: group for group, food_list in self.__food_dict.items() for food in food_list}
        self.__hash_tree = HashTree(self.__group_by_food_name.keys())

        t2 = time()
        logger.info('Done creating food catalog. Total time: %.2f sec.' % (t2 - t1))

    def find(self, sentence_text):
        food_names = self.__hash_tree.search(sentence_text)
        entities = EntityCollection([Entity(name, self.__group_by_food_name[name], FOOD_TAG) for name in food_names],
                                    FOOD_TAG)
        return entities
