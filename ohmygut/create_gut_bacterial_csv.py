import os

import numpy as np
import pandas as pd

FIELD_STRAIN = 'strain'

from ohmygut.core.constants import CLASS_EXCLUSIONS, CHUNK_SIZE, RANK_EXCLUSIONS

def get_parent_ids(id, ncbi_nodes, is_get_child_id=False):
    ids = np.array([])
    parents_ids = np.array(id)
    while len(parents_ids) != 0:
        if not is_get_child_id: ids = np.append(ids, parents_ids)
        if not is_get_child_id: parents_ids = np.unique(
            ncbi_nodes[ncbi_nodes['id'].isin(parents_ids)]['parent_id'].values)
        if is_get_child_id:  parents_ids = np.unique(
            ncbi_nodes[ncbi_nodes['parent_id'].isin(parents_ids)]['id'].values)
        parents_types = ncbi_nodes[ncbi_nodes['id'].isin(parents_ids)]['rank'].values
        parents_ids = parents_ids[~np.in1d(parents_types, RANK_EXCLUSIONS)]
        if is_get_child_id: ids = np.append(ids, parents_ids)
    ids = np.unique(ids)
    ranks = ncbi_nodes[ncbi_nodes['id'].isin(ids)]['rank'].values
    return pd.DataFrame({'id': ids, 'rank': ranks})


def get_species_ids(bact_list, ncbi_names):
    bact_list = pd.merge(bact_list, ncbi_names, how='left', on=['name'], copy=False)
    gut_species_ids = (bact_list[np.isfinite(bact_list['id'].values)].drop_duplicates('id')['id'].tolist())
    gut_species_ids.sort()
    bact_list_unresolved = pd.DataFrame(bact_list[np.isnan(bact_list['id'].values)]['name'])

    unresolved_names = bact_list_unresolved['name'].copy()
    bact_list_unresolved['name'] = bact_list_unresolved['name'].apply(lambda x: x.split(' ')[0])
    bact_list_unresolved = pd.merge(bact_list_unresolved, ncbi_names, how='left', on=['name'], copy=False)
    gut_classes_ids = \
    bact_list_unresolved[np.isfinite(bact_list_unresolved['id'].values)].drop_duplicates('id')[
        'id'].tolist()
    gut_classes_ids.sort()
    return gut_species_ids, gut_classes_ids, unresolved_names


def get_gut_bact_list(gut_bact_list_path):
    os.system("sed 's/OTU.*NN=//g' " + gut_bact_list_path +
              " | sed 's/\t.*//g' | sed 's/_/ /1' | sed 's/|D=.*//g' | sed 's/_.*//g' > tmp_HIT.txt")
    os.system("grep '\[.*\].*' tmp_HIT.txt | sed 's/.*\[//g' | sed 's/\]//g' >> tmp_HIT.txt")
    os.system("grep '\.*[.*\].*' tmp_HIT.txt | sed 's/\[.*\]//g' >> tmp_HIT.txt")
    os.system("sed -i '/\]/d' tmp_HIT.txt")
    bact_list = pd.read_table('tmp_HIT.txt', names=['name']).drop_duplicates()
    os.system("sudo rm tmp_HIT.txt")
    return bact_list


def create_gut_bacterial_csv(nodes_ncbi_path, names_ncbi_path, gut_bact_list_path, output_csv_path):
    gut_names = get_gut_bact_list(gut_bact_list_path)
    ncbi_names_iter = pd.read_table(names_ncbi_path, names=['id', 'name', 'class'], usecols=[0, 2, 6], header=None,
                                    chunksize=CHUNK_SIZE)
    ncbi_nodes = pd.read_table(nodes_ncbi_path, names=['id', 'parent_id', 'rank'], usecols=[0, 2, 4], header=None)
    ncbi_names = pd.concat([chunk[~(chunk['class'].isin(CLASS_EXCLUSIONS))]
                            for chunk in ncbi_names_iter])

    [gut_species_ids, gut_class_ids, unresolved_names] = get_species_ids(bact_list=gut_names, ncbi_names=ncbi_names)

    gut_ids = gut_species_ids + gut_class_ids
    gut_ids_table = get_parent_ids(gut_ids, ncbi_nodes)
    gut_strain_ids = get_parent_ids(gut_species_ids, ncbi_nodes, is_get_child_id=True)

    gut_ids_table = pd.concat([gut_ids_table, gut_strain_ids]).drop_duplicates('id')

    gut_names = ncbi_names[ncbi_names['id'].isin(gut_ids_table['id'].tolist())]
    gut_names = pd.concat([gut_names,
                           pd.DataFrame({'id': None,
                                         'class': 'scientific name',
                                         'name': unresolved_names})],
                          ignore_index=True)

    gut_names = pd.merge(gut_names, gut_ids_table, how='left', on='id', copy=False).drop_duplicates('name')
    gut_names.loc[gut_names['rank'].isnull(), 'rank'] = 'species'
    gut_names.to_csv(output_csv_path, index=False)


output_csv_path = '../data/bacteria/gut_catalog.csv'
gut_bact_list_path = '../data/bacteria/HITdb_taxonomy_qiime.txt'

names_path = '../data/bacteria/taxdump/names.dmp'
nodes_path = '../data/bacteria/taxdump/nodes.dmp'

if __name__ == '__main__':
    create_gut_bacterial_csv(nodes_path, names_path, gut_bact_list_path, output_csv_path)
