import re
from ohmygut.core.constants import plural_dict


def sci_names(table_names):
    names_scientific = table_names.loc[(table_names['class'] == 'scientific name') &
                                       (~table_names['id'].isnull()),
                                       ['name', 'id']]

    return names_scientific


def generate_short_names(name_data):
    name_data_shortable = name_data[(name_data['rank'] == 'species') &
                                    (name_data['name'].apply(lambda x: len(x.split()) == 2)) &
                                    (name_data['name'].apply(lambda x: x[0].isupper()))].copy()
    name_data_shortable['name'] = name_data_shortable['name'].apply(lambda x: x[0] + '. ' + x.split()[1])
    name_data_shortable = name_data_shortable.drop_duplicates(subset=['name'])
    bact_short_names_dict = name_data_shortable[['name', 'id']].set_index('name').T.to_dict('records')[0]
    return bact_short_names_dict

def generate_plyral(name_data):
    name_data_plurable = name_data[(name_data['rank'].isin(['genus']) &
                                    (name_data['name'].apply(lambda x: len(x.split()) < 2)))]
    plural_bact_names = {}
    name_data_plurable.apply(lambda x: [plural_bact_names.update({name_var: x['id']}) for name_var in
                                        (re.sub(key + '\\b', plural_dict[key], x['name']) for key in
                                         plural_dict.keys() if bool(re.search(key + '\\b', x['name'])))],
                             axis=1)
    return plural_bact_names

