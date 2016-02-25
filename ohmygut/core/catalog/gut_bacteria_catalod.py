import difflib
import re
from collections import namedtuple
from time import time

import numpy as np
import pandas as pd
import csv

from ohmygut.core.catalog.catalog import Catalog
from ohmygut.core.hash_tree import HashTree


class GutBacteriaCatalog(Catalog):
    """Object holding NCBI ontology"""

    def __init__(self, gut_bact_path):
        self.gut_bact_path = gut_bact_path
        self.__scientific_names = None
        self.__bact_id_dict = None
        self.__hash_tree = None

    def initialize(self, nodes_ncbi_path, names_ncbi_path, gut_bact_list_path, verbose=False):
        """Creation of catalog object
        input:
            nodes_path: path to NCBI nodes.dmp file
            names_path: path to NCBI names.dmp file
            gut_bact_path: path to txt file with columns [org, genus, family, order, class, phylum], tab sep

        creates:
            txt file (self.gut_bact_path) with columns [org, synonims, id, genus, family, order, class, phylum], tab sep
        """
        t1 = time()
        if verbose:
            print('Creating bacterial catalog...')

        gut_names = pd.read_table(gut_bact_list_path, sep='\t', usecols=range(1), engine='python', names=['name'],
                                  skiprows=1)
        ncbi_names_iter = pd.read_table(names_ncbi_path, sep='\t\|\t', usecols=range(4),
                                        names=['id', 'unique_name', 'name', 'class'],
                                        engine='python', header=None, chunksize=100000)
        ncbi_nodes_iter = pd.read_table(nodes_ncbi_path, sep='\t\|\t', usecols=range(5), engine='python',
                                        chunksize=10000, names=['id', 'parent_id', 'rank', 'embl_code', 'div_id'])

        gut_ids = self.get_id_from_bact_list(bact_list=gut_names, ncbi_iterable=ncbi_names_iter)
        gut_id_type = self.get_parent_id(child_ids=gut_ids, node_iterable=ncbi_nodes_iter)

        name_class_exclusions = ['type material', 'genbank acronym', 'acronym']

        ncbi_names = pd.DataFrame(columns=['id', 'unique_name'])

        for chunk in ncbi_names_iter:
            index = ~(chunk['class'].isin(name_class_exclusions))
            ncbi_names = pd.concat(
                [ncbi_names, chunk[~(chunk['class'].isin(name_class_exclusions))][['id', 'unique_name']]])

        gut_names = ncbi_names[ncbi_names['id'].isin(gut_id_type['id'].tolist())]
        gut_names = pd.merge(gut_names, gut_id_type, how='left', on=['id'], copy=False)

        gut_names.to_csv('/projects/relation_extraction/data/bacteria/output.csv')

        t2 = time()
        if verbose:
            print('Done. Total time: %.2f sec.' % (t2 - t1))

    def __generate_excessive_dictionary(self, node_data, name_data):
        """Generate variuos types of bacterial names that can occur in text:
            - Abbreviation (e.g. 'H. pylori' from 'Helicobacter pylori')
            - Plural form (e.g. 'Streptococci' from 'Streptococcus') #NOT IMPLEMENTED YET#

        Put all generated forms in self.__bact_id_dict
        """
        species_ids = {record.id: 0 for record in node_data.values() if record.rank == 'species'}
        species_shortable_records = [record for record in name_data if record.id in species_ids and \
                                     record.name.count(' ') == 1 and \
                                     record.name[0].isupper()]
        # Strain name
        bact_short_names_dict = {record.name[0] + '. ' + record.name.split(' ')[1]: record.id for record in
                                 species_shortable_records}
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

    def get_id_from_bact_list(self, bact_list, ncbi_iterable):
        bact_list['regexp'] = bact_list['name'].apply(
            lambda x: re.sub('(_genome[\W\d_]*|_contig[\W\d_]*|_cont[0-9]+)', '', x))
        bact_list['regexp'] = bact_list['regexp'].apply(lambda x: re.sub('[\W_]+', '', x))
        bact_list['type'] = bact_list['name'].apply(lambda x: re.sub('[\W_]+.*', '', x))
        type_set = set(bact_list['type'].values)

        ncbi_names = pd.DataFrame(columns=['id', 'unique_name', 'type'])
        for chunk in ncbi_iterable:
            chunk['type'] = chunk['unique_name'].apply(lambda x: re.sub('[\W_]+.*', '', x))
            ncbi_names = pd.concat([ncbi_names, chunk[chunk['type'].isin(type_set)][['id', 'unique_name', 'type']]])

        ncbi_names['regexp'] = ncbi_names['unique_name'].apply(lambda x: re.sub('[\W_]+', '', x))
        bact_list = pd.merge(bact_list, ncbi_names, how='left', on=['regexp', 'type'], copy=False)
        is_there_bad_names = np.isnan(bact_list['id'].values).any()
        if is_there_bad_names:
            print('Some names from list are unresolved')

        gut_ids = bact_list[np.isfinite(bact_list['id'].values)]['id'].tolist()
        return gut_ids

    def get_parent_id(self, child_ids, node_iterable):
        ncbi_nodes = pd.concat([chunk[chunk['div_id'] == 0] for chunk in node_iterable])
        ranks = []
        ids = []
        parents_ranks = ncbi_nodes[ncbi_nodes['id'].isin(child_ids)]['rank']
        parents_ids = list(child_ids)

        while ('superkingdom' not in parents_ranks)&(len(parents_ranks)!=0):
            ids.extend(parents_ids)
            ranks.extend(parents_ranks)
            parents_ids = ncbi_nodes[ncbi_nodes['id'].isin(parents_ids)]['parent_id'].tolist()
            parents_ranks = ncbi_nodes[ncbi_nodes['id'].isin(parents_ids)]['rank'].tolist()
        return pd.DataFrame[{'id': ids, 'rank': ranks}]


def get_max_intersection(name, regexp_id_array):
    intersect_array = regexp_id_array['regexp'].apply(lambda x: len(set(name).intersection(x)))
    intersect_index = (intersect_array.idxmax())
    return intersect_index

