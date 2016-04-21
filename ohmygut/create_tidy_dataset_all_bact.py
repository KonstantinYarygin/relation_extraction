import pandas as pd

from ohmygut.catalog_creation_helper import get_bind_ids_bact, generate_excessive_dictionary_bact

FIELD_STRAIN = 'strain'

from ohmygut.core.constants import CLASS_EXCLUSIONS, CHUNK_SIZE


def create_all_bact_catalog(nodes_ncbi_path):
    ids = get_bind_ids_bact([2], nodes_ncbi_path, is_get_child_id=True)
    return ids


def create_bacterial_df(nodes_ncbi_path, names_ncbi_path):
    ncbi_names_iter = pd.read_table(names_ncbi_path, names=['id', 'name', 'class'], usecols=[0, 2, 6], header=None,
                                    chunksize=CHUNK_SIZE)
    ncbi_nodes = pd.read_table(nodes_ncbi_path, names=['id', 'parent_id', 'rank'], usecols=[0, 2, 4], header=None)
    ncbi_names = pd.concat([chunk[~(chunk['class'].isin(CLASS_EXCLUSIONS))] for chunk in ncbi_names_iter])

    ids_all = create_all_bact_catalog(ncbi_nodes)
    names_all_bact = ncbi_names[ncbi_names['id'].isin(ids_all['id'].tolist())]
    names_all_bact = pd.merge(names_all_bact, ids_all, how='left', on='id', copy=False).drop_duplicates('name')

    names_all_bact = generate_excessive_dictionary_bact(names_all_bact)
    names_all_bact = names_all_bact.drop_duplicates(subset=['name'])
    names_all_bact['id'] = names_all_bact['id'].astype(int)
    return names_all_bact


output_csv_path_all = '../data/bacteria/all_bact_catalog.csv'
names_path = '../data/bacteria/taxdump/names.dmp'
nodes_path = '../data/bacteria/taxdump/nodes.dmp'

if __name__ == '__main__':
    names_all = create_bacterial_df(nodes_path, names_path)
    names_all.to_csv(output_csv_path_all, index=False)
