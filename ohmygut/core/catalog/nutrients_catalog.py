from ohmygut.core import constants
from ohmygut.core.catalog.catalog import Catalog, Entity, EntityCollection
from ohmygut.core.hash_tree import HashTree
from time import time


NUTRIENT_TAG = 'NUTRIENT'

class NutrientsCatalog(Catalog):
    """Object holding nutrient ontology"""

    def __str__(self):
        return "nutrients catalog"

    def __init__(self, path):
        self.path = path

    def initialize(self, verbose=False):
        t1 = time()
        if verbose:
            print('Creating nutrients catalog...')

        with open(self.path) as nn:
            lines = [line.strip() for line in nn.readlines()]
            lines = [line for line in lines if line]
        nutrients_low = [line[0].lower() + line[1:] for line in lines]
        nutrients_upp = [line[0].upper() + line[1:] for line in lines]
        nutrients = nutrients_upp + nutrients_low
        nutrients = [nutr[:-5] if nutr.endswith(' acid') else nutr for nutr in nutrients]

        self.__nutrients = {nutrient: True for nutrient in nutrients}
        self.__hash_tree = HashTree(self.__nutrients.keys())

        t2 = time()
        if verbose:
            print('Done. Total time: %.2f sec.' % (t2 - t1))

    def find(self, sentence_text):
        """ Uses previously generated hash tree to search sentence for nutrient names

        input:
            sentence: sentence to search for nutrient names

        returns:
            list of nutrient_names
        """
        nutr_names = self.__hash_tree.search(sentence_text)
        return nutr_names


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

        with open(self.path) as f:
            f.readline()
            raw_data = (line.strip('\n').split('\t') for line in f.readlines())
        self.__nutrients_by_idname = {idname: names.split(';') for idname, names in raw_data}

        self.__generate_case_names()
        self.__remove_trash__instances()

        self.__idname_by_nutrient = {name: idname for idname in self.__nutrients_by_idname for name in
                                     self.__nutrients_by_idname[idname]}
        self.__hash_tree = HashTree(self.__idname_by_nutrient.keys())

        t2 = time()
        constants.logger.info('Done creating nutrients catalog. Total time: %.2f sec.' % (t2 - t1))

    def __generate_case_names(self):

        for idname in self.__nutrients_by_idname:
            names = self.__nutrients_by_idname[idname]
            case_names = [name[0].upper() + name[1:] for name in names if not name.isupper() and name[0].isalpha()] + \
                         [name[0].lower() + name[1:] for name in names if not name.isupper() and name[0].isalpha()] + \
                         [name for name in names if name.isupper() or not name[0].isalpha()]
            self.__nutrients_by_idname[idname] = case_names

    def __remove_trash__instances(self):
        del self.__nutrients_by_idname['Agar-agar']
        del self.__nutrients_by_idname['Protein']
        del self.__nutrients_by_idname['Pb']

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
