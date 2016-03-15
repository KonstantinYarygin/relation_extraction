import pandas as pd

from ohmygut.core.catalog.catalog import Catalog


class UsdaFoodCatalog(Catalog):
    def __init__(self, food_file_path):
        super().__init__()
        self.food_file_path = food_file_path
        self.__hash_tree = None

    def find(self, sentence_text):
        pass

    def initialize(self):
        food_data_frame = pd.read_table(self.food_file_path)
        food_data_frame.loc['word']