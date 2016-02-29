from datetime import time

import pandas as pd

from ohmygut.core.catalog.gut_bacteria_catalog import GutBacteriaCatalog, get_id_from_bact_list, get_parent_id
from ohmygut.core.constants import FIELD_NAME, NCBI_COLS_NAMES, NCBI_NUM_NAMES, NCBI_NUM_NODES, NCBI_COLS_NODES, \
    CLASS_EXCLUSIONS, FIELD_CLASS, FIELD_ID, CHUNK_SIZE


def update(nodes_ncbi_path, names_ncbi_path, gut_bact_list_path, gut_bact_path):
    t1 = time()

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

    gut_names.to_csv(gut_bact_path, index=False)

    t2 = time()


gut_bact_cat_path = '../data/bacteria/gut_catalog.csv'
gut_bact_list_path = '../data/bacteria/taxonomy_HMP_2013_NR_fixed.txt'

names_path = '../data/bacteria/taxdump/names.dmp'
nodes_path = '../data/bacteria/taxdump/nodes.dmp'

update(nodes_path, names_path, gut_bact_list_path, gut_bact_cat_path)