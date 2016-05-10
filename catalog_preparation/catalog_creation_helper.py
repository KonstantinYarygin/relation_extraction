import re

import numpy as np
import pandas as pd
from nltk import word_tokenize

from ohmygut.core.constants import plural_dict, RANK_EXCLUSIONS
from ohmygut.core.tools import untokenize


def generate_short_names_bact(name_data):
    name_data_shortable = name_data[(name_data['rank'] == 'species') &
                                    (name_data['name'].apply(lambda x: len(x.split()) == 2)) &
                                    (name_data['name'].apply(lambda x: x[0].isupper()))].copy()
    name_data_shortable['name'] = name_data_shortable['name'].apply(lambda x: x[0] + '. ' + x.split()[1])
    name_data_shortable = name_data_shortable.drop_duplicates(subset=['name'])
    return name_data_shortable


def generate_plyral_bact(name_data):
    name_data_plurable = name_data[(name_data['rank'].isin(['genus']) &
                                    (name_data['name'].apply(lambda x: len(x.split()) < 2)))]
    plyral_names = pd.DataFrame(columns=list(name_data_plurable))
    for key in plural_dict.keys():
        index = name_data_plurable['name'].apply(lambda x: bool(re.search(key + '\\b', x)))
        new_names = name_data_plurable[index].copy()
        new_names['name'] = new_names['name'].apply(lambda x: re.sub(key + '\\b', plural_dict[key], x))
        plyral_names = pd.concat([new_names, plyral_names])
    return plyral_names


def generate_cases(name_data):
    name_data_case = name_data.copy()
    name_data_case['name'] = name_data_case['name'].apply(lambda x: x.lower())
    return name_data_case


def generate_excessive_dictionary_bact(df_names):
    # abbreviation
    bact_short_names = generate_short_names_bact(df_names)
    df_names_full = pd.merge(bact_short_names, df_names, on=list(df_names), how='outer')

    # plural
    bact_plural_names = generate_plyral_bact(df_names)
    df_names_full = pd.merge(bact_plural_names, df_names_full, on=list(df_names_full), how='outer')

    # cases
    bact_cases_names = generate_cases(df_names_full)
    df_names_full = pd.merge(bact_cases_names, df_names_full, on=list(df_names_full), how='outer')
    return df_names_full


def clear_ids_by_rank_bact(ids, ncbi_nodes, rank_ex=RANK_EXCLUSIONS):
    ids_types = ncbi_nodes[ncbi_nodes['id'].isin(ids)]['rank'].values
    ids = ids[~np.in1d(ids_types, rank_ex)]
    ids_types = ncbi_nodes[ncbi_nodes['id'].isin(ids)]['rank'].values
    return pd.DataFrame({'id': ids, 'rank': ids_types})


def get_bind_ids_bact(ids, ncbi_nodes, is_get_child_id=False, rank_ex=RANK_EXCLUSIONS):
    if is_get_child_id:
        bind_ids = np.unique(ncbi_nodes[ncbi_nodes['parent_id'].isin(ids)]['id'].values)
    else:
        bind_ids = np.unique(ncbi_nodes[ncbi_nodes['id'].isin(ids)]['parent_id'].values)
    binded_types = ncbi_nodes[ncbi_nodes['id'].isin(bind_ids)]['rank'].values
    bind_ids = bind_ids[~np.in1d(binded_types, rank_ex)]
    new_ids = np.array(bind_ids)
    while len(bind_ids) != 0:
        if is_get_child_id:
            bind_ids = np.unique(ncbi_nodes[ncbi_nodes['parent_id'].isin(bind_ids)]['id'].values)
        else:
            bind_ids = np.unique(ncbi_nodes[ncbi_nodes['id'].isin(bind_ids)]['parent_id'].values)
        binded_types = ncbi_nodes[ncbi_nodes['id'].isin(bind_ids)]['rank'].values
        bind_ids = bind_ids[~np.in1d(binded_types, rank_ex)]
        new_ids = np.append(new_ids, bind_ids)
    new_ids = np.unique(new_ids)
    ranks = ncbi_nodes[ncbi_nodes['id'].isin(new_ids)]['rank'].values
    return pd.DataFrame({'id': new_ids, 'rank': ranks})


def remove_literally(data, names):
    data = data[~data['name'].isin(names)]
    return data


def all_cases_of_cases(data, do_lower=True, do_upper=True):
    index = data['name'].apply(lambda x: x.isupper())
    data_names = data[~index].copy()
    data_names['name'] = data_names['name'].apply(lambda x: word_tokenize(x))

    first_capital = data_names.copy()
    first_capital['name'] = first_capital['name'].apply(lambda x: untokenize([x[0].capitalize()] +
                                                                             [x_i.lower() for x_i in x[1:]]))
    all_capital = data_names.copy()
    all_capital['name'] = all_capital['name'].apply(lambda x: untokenize([x_i[0].capitalize() + x_i[1:] for x_i in x]))
    all_low = pd.DataFrame(columns=list(data_names))
    all_upper = pd.DataFrame(columns=list(data_names))
    if do_lower:
        all_low = data_names.copy()
        all_low['name'] = all_low['name'].apply(lambda x: untokenize([x_i.lower() for x_i in x]))
    if do_upper:
        all_upper = data_names.copy()
        all_upper['name'] = all_upper['name'].apply(lambda x: untokenize([x_i.upper() for x_i in x]))

    return pd.concat([first_capital, all_capital, all_low, all_upper])
