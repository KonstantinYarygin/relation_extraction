import pandas as pd

from ohmygut.catalog_creation_helper import get_bind_ids_bact, generate_excessive_dictionary_bact

FIELD_STRAIN = 'strain'

from ohmygut.core.constants import CLASS_EXCLUSIONS, CHUNK_SIZE, RANK_EXCLUSIONS


def create_all_bact_catalog(nodes_ncbi):
    ids = get_bind_ids_bact([2], nodes_ncbi, is_get_child_id=True)
    return ids


def replace_id_by_name(table, names, rank):
    table = pd.merge(table, names[['id', 'name']], left_on=rank, right_on='id')
    table.drop([rank, 'id'], axis=1, inplace=True)
    table.rename(columns={'name': rank}, inplace=True)
    return table


def create_scientific_table(nodes_ncbi, names_ncbi):
    ranks = nodes_ncbi['rank'].unique()
    phylums = get_bind_ids_bact([2, 2323], nodes_ncbi, is_get_child_id=True, rank_ex=ranks[ranks != 'phylum'])['id']
    classes = [pd.DataFrame({'phylum': phylum,
                             'class': get_bind_ids_bact([phylum], nodes_ncbi, is_get_child_id=True,
                                                        rank_ex=ranks[ranks != 'class'])['id']})
               for phylum in phylums.values]
    classes = pd.concat(classes)
    orders = [pd.DataFrame({'phylum': row['phylum'],
                            'class': row['class'],
                            'order': get_bind_ids_bact([row['class'], row['phylum']], nodes_ncbi, is_get_child_id=True,
                                                       rank_ex=ranks[ranks != 'order'])['id']})
              for i, row in classes.iterrows()]
    orders = pd.concat(orders)
    families = [pd.DataFrame({'phylum': row['phylum'],
                              'class': row['class'],
                              'order': row['order'],
                              'family': get_bind_ids_bact([row['order']],
                                                          nodes_ncbi, is_get_child_id=True,
                                                          rank_ex=ranks[ranks != 'family'])['id']})
                for i, row in orders.iterrows()]
    families = pd.concat(families)
    genuses = [pd.DataFrame({'phylum': row['phylum'],
                             'class': row['class'],
                             'order': row['order'],
                             'family': row['family'],
                             'genus': get_bind_ids_bact([row['family']],
                                                        nodes_ncbi, is_get_child_id=True,
                                                        rank_ex=ranks[ranks != 'genus'])['id']})
               for i, row in families.iterrows()]
    genuses = pd.concat(genuses)
    species = [pd.DataFrame({'phylum': row['phylum'],
                             'class': row['class'],
                             'order': row['order'],
                             'family': row['family'],
                             'genus': row['genus'],
                             'species': get_bind_ids_bact([row['genus']],
                                                          nodes_ncbi, is_get_child_id=True,
                                                          rank_ex=ranks[ranks != 'species'])['id']})
               for i, row in genuses.iterrows()]

    species = pd.concat(species)
    names_ncbi_sci = names_ncbi[names_ncbi['class'] == 'scientific name']

    species = replace_id_by_name(species, names_ncbi_sci, 'species')
    species = replace_id_by_name(species, names_ncbi_sci, 'genus')
    species = replace_id_by_name(species, names_ncbi_sci, 'family')
    species = replace_id_by_name(species, names_ncbi_sci, 'order')
    species = replace_id_by_name(species, names_ncbi_sci, 'class')
    species = replace_id_by_name(species, names_ncbi_sci, 'phylum')
    return species


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

    #description = create_scientific_table(ncbi_nodes, ncbi_names)
    return [names_all_bact]#, description]


output_csv_path_all = '../data/bacteria/all_bact_catalog.csv'
output_csv_path_description = '../data/bacteria/all_bact_catalog_descr.csv'
names_path = '../data/bacteria/taxdump/names.dmp'
nodes_path = '../data/bacteria/taxdump/nodes.dmp'

if __name__ == '__main__':
    [names_all] = create_bacterial_df(nodes_path, names_path)
    names_all.to_csv(output_csv_path_all, index=False)
    #description.to_csv(output_csv_path_description, index=False)
