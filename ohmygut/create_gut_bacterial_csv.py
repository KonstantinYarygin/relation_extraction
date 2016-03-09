import re

import numpy as np
import pandas as pd

from ohmygut.core.constants import FIELD_NAME, NCBI_COLS_NAMES, NCBI_NUM_NAMES, NCBI_NUM_NODES, NCBI_COLS_NODES, \
    CLASS_EXCLUSIONS, FIELD_CLASS, FIELD_ID, CHUNK_SIZE, FIELD_PARENT_ID, FIELD_RANK, RANK_EXCLUSIONS, TEMPLATE_CONTIG, \
    FIELD_UNIQUE_NAME, TEMPLATE_SEP


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


def create_gut_bacterial_csv(nodes_ncbi_path, names_ncbi_path, gut_bact_list_path, output_csv_path):
    gut_names = pd.read_table(gut_bact_list_path, usecols=[0], names=[FIELD_NAME], skiprows=1)
    ncbi_names_iter = pd.read_table(names_ncbi_path, names=NCBI_COLS_NAMES, usecols=NCBI_NUM_NAMES, header=None,
                                    chunksize=CHUNK_SIZE)
    ncbi_nodes = pd.read_table(nodes_ncbi_path, names=NCBI_COLS_NODES, usecols=NCBI_NUM_NODES, header=None)
    ncbi_names = pd.concat([chunk[~(chunk[FIELD_CLASS].isin(CLASS_EXCLUSIONS))]
                            for chunk in ncbi_names_iter])

    gut_ids = get_id_from_bact_list(bact_list=gut_names, ncbi_names=ncbi_names)
    gut_id_type = get_parent_id(child_ids=gut_ids, ncbi_nodes=ncbi_nodes)

    gut_names = ncbi_names[ncbi_names[FIELD_ID].isin(gut_id_type[FIELD_ID].tolist())]
    gut_names = pd.merge(gut_names, gut_id_type, how='left', on=[FIELD_ID], copy=False)

    gut_names.to_csv(output_csv_path, index=False)


output_csv_path = '../data/bacteria/gut_catalog.csv'
gut_bact_list_path = '../data/bacteria/taxonomy_HMP_2013_NR_fixed.txt'

names_path = '../data/bacteria/taxdump/names.dmp'
nodes_path = '../data/bacteria/taxdump/nodes.dmp'

if __name__ == '__main__':
    create_gut_bacterial_csv(nodes_path, names_path, gut_bact_list_path, output_csv_path)
