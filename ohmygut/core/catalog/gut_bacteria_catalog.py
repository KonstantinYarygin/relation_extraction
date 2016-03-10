import re
from time import time

import numpy as np
import pandas as pd

from ohmygut.core.catalog.catalog import Catalog
from ohmygut.core.constants import TEMPLATE_CONTIG, TEMPLATE_SEP, CLASS_EXCLUSIONS, CHUNK_SIZE, \
    NCBI_COLS_NODES, NCBI_COLS_NAMES, NCBI_NUM_NAMES, NCBI_NUM_NODES, FIELD_NAME, \
    FIELD_ID, FIELD_RANK, FIELD_PARENT_ID, FIELD_CLASS, RANK_EXCLUSIONS, CLASS_SCIENTIFIC, RANK_SPECIES, plural_dict
from ohmygut.core.hash_tree import HashTree


class GutBacteriaCatalog(Catalog):
    """Object holding NCBI ontology"""

    def __init__(self, gut_bact_path):
        self.gut_bact_path = gut_bact_path
        self.__scientific_names = None
        self.__bact_id_dict = None
        self.__hash_tree = None

    def initialize(self, verbose=False):
        """Creation of catalog object
        input:
            :param verbose:
        creates:
            self.__scientific_names: dictionary with NCBI_id as key and scientific bacteria name as value
            self.__bact_id_dict: dictionary with various versions of bacterial names as keys and NCBI_id as value
            self.hash_tree_root: root node of hash tree
        """
        t1 = time()
        if verbose:
            print('Creating bacterial catalog...')

        gut_names = pd.read_table(self.gut_bact_path, sep=',')
        self.__scientific_names = {record_id: record[FIELD_NAME].tolist()[0] for record_id, record in
                                   gut_names[gut_names[FIELD_CLASS] == CLASS_SCIENTIFIC].groupby(FIELD_ID)}
        self.__bact_id_dict = {record_name: record[FIELD_ID].tolist()[0] for record_name, record in
                               gut_names.groupby(FIELD_NAME)}

        self.__generate_excessive_dictionary(name_data=gut_names)

        self.__hash_tree = HashTree(self.__bact_id_dict.keys())

        t2 = time()
        if verbose:
            print('Done. Total time: %.2f sec.' % (t2 - t1))

    def __generate_excessive_dictionary(self, name_data):
        """Generate variuos types of bacterial names that can occur in text:
            - Abbreviation (e.g. 'H. pylori' from 'Helicobacter pylori')
            - Plural form (e.g. 'Streptococci' from 'Streptococcus') #NOT IMPLEMENTED YET#

        Put all generated forms in self.__bact_id_dict
        """
        # abbreviation
        name_data_shortable = name_data[(name_data[FIELD_RANK] == RANK_SPECIES) &
                                        (name_data[FIELD_NAME].apply(lambda x: len(x.split()) == 2)) &
                                        (name_data[FIELD_NAME].apply(lambda x: x[0].isupper()))]
        bact_short_names_dict = {record_name[0] + '. ' + record_name.split()[1]: record[FIELD_ID].tolist()[0]
                                 for record_name, record in
                                 name_data_shortable[name_data_shortable[FIELD_RANK] == RANK_SPECIES].groupby(
                                     FIELD_NAME)}  # todo: check trutrutru

        self.__bact_id_dict.update(bact_short_names_dict)

        # plural
        name_data_plurable = name_data[(name_data[FIELD_RANK] not in ['class', 'order', 'family']) &
                                       (name_data[FIELD_CLASS] not in ['authority'])]
        for key in plural_dict.keys():
            for value in plural_dict[key]:
                bact_plural_dict = {
                ''.join(map(lambda x: re.sub(key + '\b', value), record.name.split(' '))): record[FIELD_ID].tolist()[0]
                for record_name, record in name_data_plurable.groupby(FIELD_NAME)}
                self.__bact_id_dict.update(bact_plural_dict)

    def find(self, sentence):
        """ Uses previously generated hash tree to search sentence for bacterial names

        input:
            sentence: sentence to search for bacterial names

        returns:
            list of (bactrium_name, NCBI_id) tuples found in sentence
            :param sentence:
        """

        bact_names = self.__hash_tree.search(sentence)
        bact_ids = [self.__bact_id_dict[name] for name in bact_names]
        output_list = list(zip(bact_names, bact_ids))
        return output_list

    def get_scientific_name(self, ncbi_id):
        return self.__scientific_names[ncbi_id]
