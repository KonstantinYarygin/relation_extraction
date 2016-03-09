import os
import re
import subprocess

import numpy as np
import pandas as pd

FIELD_STRAIN = 'strain'

from ohmygut.core.constants import FIELD_NAME, NCBI_COLS_NAMES, NCBI_NUM_NAMES, NCBI_NUM_NODES, NCBI_COLS_NODES, \
    CLASS_EXCLUSIONS, FIELD_CLASS, FIELD_ID, CHUNK_SIZE, FIELD_PARENT_ID, FIELD_RANK, RANK_EXCLUSIONS, TEMPLATE_CONTIG, \
    TEMPLATE_SEP


def get_parent_ids(child_ids, ncbi_nodes):
    ids = np.array([])
    parents_ids = np.array(child_ids)
    while len(parents_ids) != 0:
        ids = np.append(ids, parents_ids)
        parents_ids = np.unique(ncbi_nodes[ncbi_nodes[FIELD_ID].isin(parents_ids)][FIELD_PARENT_ID].values)
        parents_types = ncbi_nodes[ncbi_nodes[FIELD_ID].isin(parents_ids)][FIELD_RANK].values
        parents_ids = parents_ids[~np.in1d(parents_types, RANK_EXCLUSIONS)]
    ids = np.unique(ids)
    ranks = ncbi_nodes[ncbi_nodes[FIELD_ID].isin(ids)][FIELD_RANK].values
    return pd.DataFrame({FIELD_ID: ids, FIELD_RANK: ranks})


def get_children_ids(parent_ids, ncbi_nodes):
    ids = np.array([])
    children_ids = np.array(parent_ids)
    while len(children_ids) != 0:
        children_ids = np.unique(ncbi_nodes[ncbi_nodes[FIELD_PARENT_ID].isin(children_ids)][FIELD_ID].values)
        children_types = ncbi_nodes[(ncbi_nodes[FIELD_ID].isin(children_ids))][FIELD_RANK].values
        children_ids = children_ids[~np.in1d(children_types, RANK_EXCLUSIONS)]
        ids = np.append(ids, children_ids)
    ids = np.unique(ids)
    ranks = ncbi_nodes[ncbi_nodes[FIELD_ID].isin(ids)][FIELD_RANK].values
    return pd.DataFrame({FIELD_ID: ids, FIELD_RANK: ranks})


def get_species_ids(bact_list, ncbi_names):
    bact_list = pd.merge(bact_list, ncbi_names, how='left', on=[FIELD_NAME], copy=False)
    gut_species_ids = (bact_list[np.isfinite(bact_list[FIELD_ID].values)].drop_duplicates(FIELD_ID)[FIELD_ID].tolist())
    gut_species_ids.sort()

    bact_list_unresolved = pd.DataFrame(bact_list[np.isnan(bact_list[FIELD_ID].values)][FIELD_NAME])
    unresolved_names = bact_list_unresolved[FIELD_NAME].copy()
    bact_list_unresolved[FIELD_NAME] = bact_list_unresolved[FIELD_NAME].apply(lambda x: x.split(' ')[0])
    bact_list_unresolved = pd.merge(bact_list_unresolved, ncbi_names, how='left', on=[FIELD_NAME], copy=False)
    gut_classes_ids = bact_list_unresolved[np.isfinite(bact_list_unresolved[FIELD_ID].values)
                       ].drop_duplicates(FIELD_ID)[FIELD_ID].tolist()
    gut_classes_ids.sort()
    return gut_species_ids, gut_classes_ids, unresolved_names


def prepare_gut_bact_list_tyaht(gut_bact_list_path):
    bact_list = pd.read_table(gut_bact_list_path, usecols=[0], names=[FIELD_NAME])
    bact_list[FIELD_NAME] = bact_list[FIELD_NAME].apply(lambda x: re.sub(TEMPLATE_CONTIG, '', x))
    bact_list[FIELD_NAME] = bact_list[FIELD_NAME].apply(lambda x: re.sub(TEMPLATE_SEP, '', x))
    return bact_list


def get_gut_bact_list(gut_bact_list_path):
    os.system("sed 's/OTU.*NN=//g' " + gut_bact_list_path +
              " | sed 's/\t.*//g' | sed 's/_/ /1' | sed 's/|D=.*//g' | sed 's/_.*//g' > tmp_HIT.txt")
    os.system("grep '\[.*\].*' tmp_HIT.txt | sed 's/.*\[//g' | sed 's/\]//g' >> tmp_HIT.txt")
    os.system("grep '\.*[.*\].*' tmp_HIT.txt | sed 's/\[.*\]//g' >> tmp_HIT.txt")
    os.system("sed -i '/\]/d' tmp_HIT.txt")
    bact_list = pd.read_table('tmp_HIT.txt', names=[FIELD_NAME]).drop_duplicates()
    os.system("sudo rm tmp_HIT.txt")
    return bact_list


def create_gut_bacterial_csv(nodes_ncbi_path, names_ncbi_path, gut_bact_list_path, output_csv_path):
    gut_names = get_gut_bact_list(gut_bact_list_path)
    ncbi_names_iter = pd.read_table(names_ncbi_path, names=NCBI_COLS_NAMES, usecols=NCBI_NUM_NAMES, header=None,
                                    chunksize=CHUNK_SIZE)
    ncbi_nodes = pd.read_table(nodes_ncbi_path, names=NCBI_COLS_NODES, usecols=NCBI_NUM_NODES, header=None)
    ncbi_names = pd.concat([chunk[~(chunk[FIELD_CLASS].isin(CLASS_EXCLUSIONS))]
                            for chunk in ncbi_names_iter])

    [gut_species_ids, gut_class_ids, unresolved_names] = get_species_ids(bact_list=gut_names, ncbi_names=ncbi_names)

    gut_ids = gut_species_ids + gut_class_ids
    gut_ids_table = get_parent_ids(child_ids=gut_ids, ncbi_nodes=ncbi_nodes)
    gut_strain_ids = get_children_ids(gut_species_ids, ncbi_nodes)

    gut_ids_table = pd.concat([gut_ids_table, gut_strain_ids]).drop_duplicates(FIELD_ID)

    gut_names = ncbi_names[ncbi_names[FIELD_ID].isin(gut_ids_table[FIELD_ID].tolist())]
    gut_names = pd.concat([gut_names,
                           pd.DataFrame({FIELD_ID: None,
                                         FIELD_CLASS: 'scientific name',
                                         FIELD_NAME: unresolved_names})],
                          ignore_index=True)
    gut_names = pd.merge(gut_names, gut_ids_table, how='left', on=FIELD_ID, copy=False).drop_duplicates(FIELD_NAME)
    gut_names.loc[gut_names[FIELD_RANK].isnull(), FIELD_RANK] = 'species'
    gut_names.to_csv(output_csv_path, index=False)


output_csv_path = '../data/bacteria/gut_catalog.csv'
gut_bact_list_path = '../data/bacteria/HITdb_taxonomy_qiime.txt'

names_path = '../data/bacteria/taxdump/names.dmp'
nodes_path = '../data/bacteria/taxdump/nodes.dmp'

if __name__ == '__main__':
    create_gut_bacterial_csv(nodes_path, names_path, gut_bact_list_path, output_csv_path)
