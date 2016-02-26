
import re
from time import time

import numpy as np
import pandas as pd

from ohmygut.core.catalog.catalog import Catalog
from ohmygut.core.constants import TEMPLATE_CONTIG, TEMPLATE_SEP, CLASS_EXCLUSIONS, CHUNK_SIZE, \
    NCBI_COLS_NODES, NCBI_COLS_NAMES, NCBI_NUM_NAMES, NCBI_NUM_NODES, FIELD_NAME, FIELD_UNIQUE_NAME, \
    FIELD_ID, FIELD_RANK, FIELD_PARENT_ID, FIELD_CLASS, RANK_EXCLUSIONS, CLASS_SCIENTIFIC, RANK_SPECIES
from ohmygut.core.hash_tree import HashTree


def get_parent_id(child_ids, ncbi_nodes):
    ids = np.array([])
    parents_ids = np.array(child_ids)
    while len(parents_ids) != 0:
        ids = np.append(ids, parents_ids)
        parents_ids = np.unique(ncbi_nodes[(ncbi_nodes[FIELD_ID].isin(parents_ids))][FIELD_PARENT_ID].values)
        parents_types = ncbi_nodes[(ncbi_nodes[FIELD_ID].isin(parents_ids))][FIELD_RANK].values
        parents_ids = parents_ids[~np.in1d(parents_types, RANK_EXCLUSIONS)]
    ids = np.unique(ids)
    ranks = ncbi_nodes[ncbi_nodes[FIELD_ID].isin(ids)][FIELD_RANK].values
    return pd.DataFrame({FIELD_ID: ids, FIELD_RANK: ranks})


def get_id_from_bact_list(bact_list, ncbi_names):
    field_regex = 'regexp'
    bact_list[field_regex] = bact_list[FIELD_NAME].apply(lambda x: re.sub(TEMPLATE_CONTIG, '', x))
    bact_list[field_regex] = bact_list[field_regex].apply(lambda x: re.sub(TEMPLATE_SEP, '', x))

    ncbi_names[field_regex] = ncbi_names[FIELD_UNIQUE_NAME].apply(lambda x: re.sub(TEMPLATE_SEP, '', x))
    bact_list = pd.merge(bact_list, ncbi_names, how='left', on=[field_regex], copy=False).drop_duplicates(cols='id')

    is_there_bad_names = np.isnan(bact_list[FIELD_ID].values).any()
    if is_there_bad_names: print('Some names from list are unresolved')

    gut_ids = (bact_list[np.isfinite(bact_list[FIELD_ID].values)][FIELD_ID].tolist())
    gut_ids.sort()

    ncbi_names.drop(field_regex, axis=1, inplace=True)
    return gut_ids


class GutBacteriaCatalog(Catalog):
    """Object holding NCBI ontology"""

    def __init__(self, gut_bact_path):
        self.gut_bact_path = gut_bact_path
        self.__scientific_names = None
        self.__bact_id_dict = None
        self.__hash_tree = None

    def update(self, nodes_ncbi_path, names_ncbi_path, gut_bact_list_path, verbose=False):
        """Creation of catalog object
        input:
            :param nodes_ncbi_path: path to NCBI nodes.dmp file
            :param names_ncbi_path: path to NCBI names.dmp file
            :param gut_bact_list_path: path to txt file with columns [org, genus, family, order, class, phylum], tab sep
            :param verbose:

        creates:

            txt file (self.gut_bact_path) with columns [id,unique_name,rank], tab sep. Path: self.gut_bact_path

        """
        t1 = time()
        if verbose:
            print('Updating bacterial list...')

        gut_names = pd.read_table(gut_bact_list_path, usecols=[0], names=[FIELD_NAME], skiprows=1)
        ncbi_names_iter = pd.read_table(names_ncbi_path, names=NCBI_COLS_NAMES, usecols=NCBI_NUM_NAMES, header=None, chunksize=CHUNK_SIZE)
        ncbi_nodes = pd.read_table(nodes_ncbi_path, names=NCBI_COLS_NODES, usecols=NCBI_NUM_NODES, header=None)
        ncbi_names = pd.concat([chunk[~(chunk[FIELD_CLASS].isin(CLASS_EXCLUSIONS))]
                                for chunk in ncbi_names_iter])

        gut_ids = get_id_from_bact_list(bact_list=gut_names, ncbi_names=ncbi_names)
        gut_id_type = get_parent_id(child_ids=gut_ids, ncbi_nodes=ncbi_nodes)

        gut_names = ncbi_names[ncbi_names[FIELD_ID].isin(gut_id_type[FIELD_ID].tolist())]
        gut_names = pd.merge(gut_names, gut_id_type, how='left', on=[FIELD_ID], copy=False)

        gut_names.to_csv(self.gut_bact_path, index=False)

        t2 = time()
        if verbose:
            print('Done. Total time: %.2f sec.' % (t2 - t1))

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
        self.__scientific_names = {record_id: record[FIELD_UNIQUE_NAME].tolist()[0] for record_id, record in
                                   gut_names[gut_names[FIELD_CLASS] == CLASS_SCIENTIFIC].groupby(FIELD_ID)}
        self.__bact_id_dict = {record_name: record[FIELD_ID].tolist()[0] for record_name, record in
                               gut_names.groupby(FIELD_UNIQUE_NAME)}

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
        name_data = name_data[(name_data[FIELD_RANK] == RANK_SPECIES) &
                              (name_data[FIELD_UNIQUE_NAME].apply(lambda x: len(x.split())==2)) &
                              (name_data[FIELD_UNIQUE_NAME].apply(lambda x: x[0].isupper()))]
        #record.name.count(' ') == 1 and record.name[0].isupper()
        bact_short_names_dict = {record_name[0] + '. ' + record_name.split()[1]: record[FIELD_ID].tolist()[0]
                                 for record_name, record in
                                 name_data[name_data[FIELD_RANK] == RANK_SPECIES].groupby(FIELD_UNIQUE_NAME)}

        self.__bact_id_dict.update(bact_short_names_dict)

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
