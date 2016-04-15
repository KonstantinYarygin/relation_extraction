import re
from time import time

import pandas as pd
from nltk.tokenize import word_tokenize

from ohmygut.core import constants
from ohmygut.core.catalog.catalog import Catalog
from ohmygut.core.hash_tree import HashTree
from ohmygut.core.tools import untokenize


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

        self.__remove_disease_literally()

        self.__add_all_cases_of_cases()

        self.hash_tree = HashTree(self.disease_dictionary.keys())

        t2 = time()
        constants.logger.info('Done creating diseases catalog. Total time: %.2f sec.' % (t2 - t1))

    def __remove_disease_literally(self):
        """Removes 'disease' item from catalog"""
        try:
            del self.disease_dictionary['disease']
        except:
            pass

    def __add_all_cases_of_cases(self):
        for name, doid_id in list(self.disease_dictionary.items())[:]:
            word_list = word_tokenize(name)
            is_abbreviation_list = [word.isupper() for word in word_list]

            first_capital = untokenize(
                [word_list[0].capitalize() if not is_abbreviation_list[0] else word_list[0]] + word_list[1:])
            all_capital = untokenize([word.capitalize() if not is_abbreviation else word for word, is_abbreviation in
                                      zip(word_list, is_abbreviation_list)])
            all_lower = untokenize([word.lower() if not is_abbreviation else word for word, is_abbreviation in
                                    zip(word_list, is_abbreviation_list)])
            all_upper = name.upper()

            self.disease_dictionary.update({all_lower: doid_id,
                                            all_capital: doid_id,
                                            all_upper: doid_id,
                                            first_capital: doid_id})

    def find(self, sentence_text):
        """ Uses previously generated hash tree to search sentence for nutrient names

        input:
            sentence: sentence to search for nutrient names

        returns:
            list of nutrient_names
        """
        diseases_names = self.hash_tree.search(sentence_text)
        output = [(name, self.disease_dictionary[name]) for name in diseases_names]
        return output

