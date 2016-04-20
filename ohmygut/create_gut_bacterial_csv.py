import numpy as np
import pandas as pd

FIELD_STRAIN = 'strain'

from ohmygut.core.constants import CLASS_EXCLUSIONS, CHUNK_SIZE, RANK_EXCLUSIONS


def clear_ids_by_rank(ids, ncbi_nodes):
    ids_types = ncbi_nodes[ncbi_nodes['id'].isin(ids)]['rank'].values
    ids = ids[~np.in1d(ids_types, RANK_EXCLUSIONS)]
    ids_types = ncbi_nodes[ncbi_nodes['id'].isin(ids)]['rank'].values
    return pd.DataFrame({'id': ids, 'rank': ids_types})


def get_bind_ids(ids, ncbi_nodes, is_get_child_id=False):
    if is_get_child_id:
        bind_ids = np.unique(ncbi_nodes[ncbi_nodes['parent_id'].isin(ids)]['id'].values)
    else:
        bind_ids = np.unique(ncbi_nodes[ncbi_nodes['id'].isin(ids)]['parent_id'].values)
    binded_types = ncbi_nodes[ncbi_nodes['id'].isin(bind_ids)]['rank'].values
    bind_ids = bind_ids[~np.in1d(binded_types, RANK_EXCLUSIONS)]
    new_ids = np.array(bind_ids)
    while len(bind_ids) != 0:
        if is_get_child_id:
            bind_ids = np.unique(ncbi_nodes[ncbi_nodes['parent_id'].isin(bind_ids)]['id'].values)
        else:
            bind_ids = np.unique(ncbi_nodes[ncbi_nodes['id'].isin(bind_ids)]['parent_id'].values)
        binded_types = ncbi_nodes[ncbi_nodes['id'].isin(bind_ids)]['rank'].values
        bind_ids = bind_ids[~np.in1d(binded_types, RANK_EXCLUSIONS)]
        new_ids = np.append(new_ids, bind_ids)
    new_ids = np.unique(new_ids)
    ranks = ncbi_nodes[ncbi_nodes['id'].isin(new_ids)]['rank'].values
    return pd.DataFrame({'id': new_ids, 'rank': ranks})


def create_all_bact_catalog(nodes_ncbi_path):
    ids = get_bind_ids([2], nodes_ncbi_path, is_get_child_id=True)
    return ids


def create_gut_bacterial_csv(nodes_ncbi_path, names_ncbi_path, gut_bact_list_path, output_csv_path):
    SINTETIC_ID = 1000000000
    gut_names = pd.read_table(gut_bact_list_path, names=['name'], sep=',')
    ncbi_names_iter = pd.read_table(names_ncbi_path, names=['id', 'name', 'class'], usecols=[0, 2, 6], header=None,
                                    chunksize=CHUNK_SIZE)
    ncbi_nodes = pd.read_table(nodes_ncbi_path, names=['id', 'parent_id', 'rank'], usecols=[0, 2, 4], header=None)
    ncbi_names = pd.concat([chunk[~(chunk['class'].isin(CLASS_EXCLUSIONS))]
                            for chunk in ncbi_names_iter])

    ids_all = create_all_bact_catalog(ncbi_nodes)
    names_all = ncbi_names[ncbi_names['id'].isin(ids_all['id'].tolist())]
    names_all = pd.merge(names_all, ids_all, how='left', on='id', copy=False).drop_duplicates('name')

    gut_names_first = gut_names['name'].apply(lambda x: str.split(x, ' ')[0])
    gut_names = pd.merge(gut_names, ncbi_names[['name', 'id']], how='left', on='name')
    gut_names_unknown = gut_names[np.isnan(gut_names['id'])].copy()
    gut_names.loc[np.isnan(gut_names['id']), 'name'] = gut_names_first[np.isnan(gut_names['id'])]
    gut_names = pd.merge(gut_names[['name']], ncbi_names, how='left', on='name')
    gut_names_unknown = pd.concat([gut_names_unknown, gut_names[np.isnan(gut_names['id'])].copy()])
    gut_names_unknown['id'] = range(SINTETIC_ID, SINTETIC_ID + len(gut_names_unknown))
    gut_names_unknown['class'] = 'unknown'
    gut_names_unknown['rank'] = 'unknown'

    gut_names = gut_names[~np.isnan(gut_names['id'])]
    gut_names = gut_names[~np.isnan(gut_names['id'])]
    gut_names = gut_names.drop_duplicates(subset='id')

    gut_ids = clear_ids_by_rank(gut_names['id'].values, ncbi_nodes)

    gut_parent_ids = get_bind_ids(gut_ids['id'].values, ncbi_nodes)

    gut_ids_table = pd.concat([gut_parent_ids, gut_ids]).drop_duplicates('id')

    gut_names = ncbi_names[ncbi_names['id'].isin(gut_ids_table['id'].tolist())]

    gut_names = pd.merge(gut_names, gut_ids_table, how='left', on='id', copy=False).drop_duplicates('name')
    gut_names = pd.concat([gut_names, gut_names_unknown])
    gut_names.to_csv(output_csv_path, index=False)
    names_all.to_csv(output_csv_path_all, index=False)


output_csv_path = '../data/bacteria/gut_catalog.csv'
output_csv_path_all = '../data/bacteria/all_catalog.csv'
gut_bact_list_path = '../data/bacteria/bact_names_pull_new_base.csv'  # '../data/bacteria/HITdb_taxonomy_qiime.txt'

names_path = '../data/bacteria/taxdump/names.dmp'
nodes_path = '../data/bacteria/taxdump/nodes.dmp'

if __name__ == '__main__':
    create_gut_bacterial_csv(nodes_path, names_path, gut_bact_list_path, output_csv_path)
