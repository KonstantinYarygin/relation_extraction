import re
from time import time

from nltk.tokenize import word_tokenize

from ohmygut.core import constants
from ohmygut.core.catalog.catalog import Catalog
from ohmygut.core.hash_tree import HashTree
from ohmygut.core.tools import untokenize


class DiseasesCatalog(Catalog):
    def __str__(self):
        return "diseases catalog"

    def __init__(self, doid_path):
        self.__disease_dictionary = {}
        self.__doid_data = {}
        self.__hash_tree = None
        self.doid_path = doid_path

    def initialize(self):
        t1 = time()
        constants.logger.info('Creating diseases catalog...')

        with open(self.doid_path) as f:
            raw_data = ''.join(f.readlines()).split('\n\n')
            raw_data = [record.split('\n') for record in raw_data]
            raw_data = [record[1:] for record in raw_data if record[0] == '[Term]']
            raw_data = [[line.split(': ', 1) for line in record] for record in raw_data]
            features = {feature for record in raw_data for feature, value in record}
            self.__doid_data = {doid_id: {feature: [] for feature in features} for record in raw_data for
                                feature, doid_id in record if feature == 'id'}
            for record in raw_data:
                record_id = [doid_id for feature, doid_id in record if feature == 'id'][0]
                [self.__doid_data[record_id][feature].append(value) for feature, value in record]

        for doid_id, record in self.__doid_data.items():
            synonyms_clean = [re.search('\"(.*)\"\s(EXACT|NARROW|RELATED)', synonym).group(1).strip() for synonym in
                              record['synonym']]
            self.__disease_dictionary.update({synonym: doid_id for synonym in synonyms_clean})
            self.__disease_dictionary.update({name: doid_id for name in record['name']})

        self.__remove_disease_literally()

        self.__add_all_cases_of_cases()

        self.__hash_tree = HashTree(self.__disease_dictionary.keys())

        t2 = time()
        constants.logger.info('Done creating diseases catalog. Total time: %.2f sec.' % (t2 - t1))

    def __remove_disease_literally(self):
        """Removes 'disease' item from catalog"""
        del self.__disease_dictionary['disease']

    def __add_all_cases_of_cases(self):
        for name, doid_id in list(self.__disease_dictionary.items())[:]:
            word_list = word_tokenize(name)
            is_abbreviation_list = [word.isupper() for word in word_list]

            first_capital = untokenize(
                [word_list[0].capitalize() if not is_abbreviation_list[0] else word_list[0]] + word_list[1:])
            all_capital = untokenize([word.capitalize() if not is_abbreviation else word for word, is_abbreviation in
                                      zip(word_list, is_abbreviation_list)])
            all_lower = untokenize([word.lower() if not is_abbreviation else word for word, is_abbreviation in
                                    zip(word_list, is_abbreviation_list)])
            all_upper = name.upper()

            self.__disease_dictionary.update({all_lower: doid_id,
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
        diseases_names = self.__hash_tree.search(sentence_text)
        output = [(name, self.__disease_dictionary[name]) for name in diseases_names]
        return (output)

    def get_common_name(self, doid_id):
        return self.__doid_data[doid_id]['name'][0]
