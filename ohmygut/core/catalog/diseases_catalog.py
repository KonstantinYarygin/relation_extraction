from ohmygut.core.catalog.catalog import Catalog
from ohmygut.core.hash_tree import HashTree
from time import time
import re

class DiseasesCatalog(Catalog):
    """Object holding nutrient ontology"""

    def __init__(self, doid_path):
        self.doid_path = doid_path

    def initialize(self, verbose=False):
        t1 = time()
        if verbose:
            print('Creating diseases catalog...')

        with open(self.doid_path) as f:
            raw_data = ''.join(f.readlines()).split('\n\n')
            raw_data = [record.split('\n') for record in raw_data]
            raw_data = [record[1:] for record in raw_data if record[0] == '[Term]']
            raw_data = [[line.split(': ', 1) for line in record] for record in raw_data]
            features = {pair[0] for record in raw_data for pair in record}
            self.__doid_data = {pair[1]: {feature: [] for feature in features} for record in raw_data for pair in record if pair[0] == 'id'}
            for record in raw_data:
                record_id = [pair[1] for pair in record if pair[0] == 'id'][0]
                [self.__doid_data[record_id][pair[0]].append(pair[1]) for pair in record]

        self.__disease_dictionary = {}
        for doid_id, record in self.__doid_data.items():
            synonyms_clean = [re.search('\"(.*)\"\s(EXACT|NARROW|RELATED)', synonym).group(1).strip() for synonym in record['synonym']]
            self.__disease_dictionary.update({synonym: doid_id for synonym in synonyms_clean})
            self.__disease_dictionary.update({name: doid_id for name in record['name']})

        self.__remove_disease_literally()

        self.__hash_tree = HashTree(self.__disease_dictionary.keys())

        t2 = time()
        if verbose:
            print('Done. Total time: %.2f sec.' % (t2 - t1))

    def __remove_disease_literally(self):
        """Removes 'disease' item from catalog"""
        del self.__disease_dictionary['disease']

    def find(self, sentence):
        """ Uses previously generated hash tree to search sentence for nutrient names

        input:
            sentence: sentence to search for nutrient names

        returns:
            list of nutrient_names
        """
        diseases_names = self.__hash_tree.search(sentence)
        output = [(name, self.__disease_dictionary[name]) for name in diseases_names]
        return(output)

