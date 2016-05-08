from time import time

import pandas as pd
from ohmygut.core.catalog.catalog import Catalog, Entity, EntityCollection
from ohmygut.core.constants import logger
from ohmygut.core.hash_tree import HashTree

BACTERIA_TAG = 'BACTERIA'


class GutBacteriaCatalog(Catalog):
    """Object holding NCBI ontology"""

    def get_list(self):
        pass

    def __str__(self):
        return "gut bacteria catalog"

    def __init__(self, gut_bact_path, initialized_all_bacteria_catalog):
        self.initialized_all_bacteria_catalog = initialized_all_bacteria_catalog
        self.gut_bact_path = gut_bact_path
        self.__scientific_names = None
        self.__bact_id_dict = None
        self.__hash_tree = None

    def initialize(self):
        """Creation of catalog object
        input:
            :param verbose:
        creates:
            self.__scientific_names: dictionary with NCBI_id as key and scientific bacteria name as value
            self.__bact_id_dict: dictionary with various versions of bacterial names as keys and NCBI_id as value
            self.hash_tree_root: root node of hash tree
        """
        t1 = time()
        logger.info('Creating bacterial catalog...')

        gut_names = pd.read_table(self.gut_bact_path, sep=',')
        gut_names_scientific = self.sci_names(table_names=gut_names)
        self.__scientific_names = gut_names_scientific.set_index('id').T.to_dict('records')[0]
        self.__bact_id_dict = gut_names[['name', 'id']].set_index('name').T.to_dict('records')[0]
        self.__hash_tree = HashTree(self.__bact_id_dict.keys())

        t2 = time()
        logger.info('Done creating bacterial catalog. Total time: %.2f sec.' % (t2 - t1))

    def find(self, sentence_text):
        """ Uses previously generated hash tree to search sentence for bacterial names

        input:
            sentence: sentence to search for bacterial names

        returns:
            list of (bactrium_name, NCBI_id) tuples found in sentence
            :param sentence_text:
        """

        bact_names = self.__hash_tree.search(sentence_text)
        if not bact_names:
            return EntityCollection([], BACTERIA_TAG)

        all_bacteria_collection = self.initialized_all_bacteria_catalog.find(sentence_text)
        all_bacteria_collection.entities = [entity for entity in all_bacteria_collection.entities if
                                            entity.name not in bact_names]
        bact_ids = [self.__bact_id_dict[name] for name in bact_names]
        output_list = list(zip(bact_names, bact_ids))

        bacteria_collection = EntityCollection([Entity(name, code, BACTERIA_TAG) for name, code in output_list],
                                               BACTERIA_TAG)
        bacteria_collection.entities.extend(all_bacteria_collection.entities)

        return bacteria_collection

    def get_scientific_name(self, ncbi_id):
        return self.__scientific_names[ncbi_id]

    def sci_names(self, table_names):
        names_scientific = table_names.loc[(table_names['class'] == 'scientific name') &
                                           (~table_names['id'].isnull()),
                                           ['name', 'id']].drop_duplicates(subset=['id'])
        return names_scientific
