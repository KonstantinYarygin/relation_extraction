import pandas as pd

from ohmygut.core.catalog.catalog import Catalog
from ohmygut.core.hash_tree import HashTree


class UsdaFoodCatalog(Catalog):
    def __str__(self):
        return "usda food catalog"

    def __init__(self, food_file_path):
        super().__init__()
        self.food_file_path = food_file_path
        self.__hash_tree = None

    def find(self, sentence_text):
        return self.__hash_tree.search(sentence_text)

    def initialize(self):
        food_data_frame = pd.read_table(self.food_file_path, sep=";", encoding="utf-8")
        words = list(food_data_frame['word'].values)
        words_capitalized = list(map(lambda x: x.capitalize(), words))
        words += words_capitalized
        self.__hash_tree = HashTree(words)
