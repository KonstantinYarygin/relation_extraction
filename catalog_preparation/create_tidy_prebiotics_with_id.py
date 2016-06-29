import os

import inflect
import numpy
import pandas as pd

prebiotics_list_path = os.path.join('..', 'data', 'prebiotic', 'prebiotics_dict.csv')
output_csv_path = os.path.join('..', 'data', 'prebiotic', 'prebiotics_tidy_dict.csv')

def create_all_vars(prebiotics_final):
    inflect_engine = inflect.engine()
    # pluralize
    prebiotic_plural = [inflect_engine.plural(prebiotic) for prebiotic in prebiotics_final]
    prebiotics_final = prebiotics_final + prebiotic_plural

    # lower
    prebiotic_lower = [prebiotic.lower() for prebiotic in prebiotics_final]
    prebiotics_final = prebiotics_final + prebiotic_lower

    # capitalize
    prebiotic_capitalized = [prebiotic.capitalize() for prebiotic in prebiotics_final]
    prebiotics_final = prebiotics_final + prebiotic_capitalized

    # upper
    prebiotic_upper = [prebiotic.upper() for prebiotic in prebiotics_final]
    prebiotics_final = prebiotics_final + prebiotic_upper

    # remove 2-letters words
    prebiotics_final = [prebiotic for prebiotic in prebiotics_final if len(prebiotic) > 2]

    # capitalize all 3-letters words
    prebiotics_3_letter_capitalized = [prebiotic.upper() for prebiotic in prebiotics_final if len(prebiotic) == 3]
    prebiotics_final = [prebiotic for prebiotic in prebiotics_final if len(prebiotic) != 3]
    prebiotics_final = prebiotics_final + prebiotics_3_letter_capitalized

    # remove SOS
    prebiotics_final = [prebiotic for prebiotic in prebiotics_final if prebiotic.lower() != 'sos']
    return prebiotics_final

if __name__ == '__main__':
    prebiotics_final = []

    prebiotics = pd.read_table(prebiotics_list_path, sep='\t')
    prebiotics['type']='sci_name'
    prebiotics_syn_lists = prebiotics['synonims'].apply(
        lambda x: list() if not (isinstance(x, str)) else str.split(x, ', '))
    prebiotics_syn = pd.DataFrame()
    for prebiotics_syn_list, i, trans, cont in zip(prebiotics_syn_lists, prebiotics['id'],
                                                   prebiotics['translation'], prebiotics['contains']):
        dt = pd.DataFrame({'name': prebiotics_syn_list,
                           'id': [i]*len(prebiotics_syn_list),
                           'type': ['synonim']*len(prebiotics_syn_list),
                           'translation': [trans]*len(prebiotics_syn_list),
                           'contains': [cont]*len(prebiotics_syn_list)})
        prebiotics_syn = prebiotics_syn.append(dt)
    prebiotics_syn = prebiotics_syn.append(prebiotics[['name', 'id', 'type', 'translation', 'contains']])

    prebiotics_dt = pd.DataFrame()
    for prebiotic, id, type, trans, cont in zip(prebiotics_syn['name'], prebiotics_syn['id'], prebiotics_syn['type'],
                                          prebiotics_syn['translation'], prebiotics_syn['contains']):
        prebiotic_new = create_all_vars([prebiotic])
        prebiotic_new_dt = pd.DataFrame({'name': prebiotic_new,
                           'id': [id]*len(prebiotic_new),
                           'type': [type]*len(prebiotic_new),
                           'translation': [trans]*len(prebiotic_new),
                           'contains': [cont]*len(prebiotic_new)})
        prebiotics_dt = prebiotics_dt.append(prebiotic_new_dt)


    prebiotics_dt = prebiotics_dt.drop_duplicates()
    prebiotics_dt.to_csv(output_csv_path, index=False)


