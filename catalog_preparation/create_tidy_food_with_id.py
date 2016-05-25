import os

import inflect
import numpy
import pandas as pd

food_list_path = os.path.join('..', 'data', 'food', 'food_dict.csv')
output_csv_path = os.path.join('..', 'data', 'food', 'food_tidy_dict.csv')

def create_all_vars(food_list_final):
    inflect_engine = inflect.engine()
    # pluralize
    prebiotic_plural = [inflect_engine.plural(prebiotic) for prebiotic in food_list_final]
    food_list_final = food_list_final + prebiotic_plural

    # lower
    prebiotic_lower = [prebiotic.lower() for prebiotic in food_list_final]
    food_list_final = food_list_final + prebiotic_lower

    # capitalize
    prebiotic_capitalized = [prebiotic.capitalize() for prebiotic in food_list_final]
    food_list_final = food_list_final + prebiotic_capitalized

    # upper
    prebiotic_upper = [prebiotic.upper() for prebiotic in food_list_final]
    food_list_final = food_list_final + prebiotic_upper

    # remove 2-letters words
    food_list_final = [prebiotic for prebiotic in food_list_final if len(prebiotic) > 2]

    # capitalize all 3-letters words
    #food_list_3_letter_capitalized = [prebiotic.upper() for prebiotic in food_list_final if len(prebiotic) == 3]
    #food_list_final = [prebiotic for prebiotic in food_list_final if len(prebiotic) != 3]
    #food_list_final = food_list_final + food_list_3_letter_capitalized

    # remove SOS
    food_list_final = [prebiotic for prebiotic in food_list_final if prebiotic.lower() != 'sos']
    return food_list_final

if __name__ == '__main__':
    food_list_final = []

    food_list = pd.read_table(food_list_path, sep='\t')
    food_list['type']= 'sci_name'
    food_syn_lists = food_list['synonims'].apply(
        lambda x: list() if not (isinstance(x, str)) else str.split(x, ', '))
    food_syn = pd.DataFrame()
    for food_syn_list, i, trans in zip(food_syn_lists, food_list['id'], food_list['translation']):
        dt = pd.DataFrame({'name': food_syn_list,
                           'id': [i]*len(food_syn_list),
                           'type': ['synonim']*len(food_syn_list),
                           'translation': [trans]*len(food_syn_list)})
        food_syn = food_syn.append(dt)
    food_syn = food_syn.append(food_list[['name', 'id', 'type', 'translation']])

    food_dt = pd.DataFrame()
    for food, id, type, trans in zip(food_syn['name'], food_syn['id'], food_syn['type'], food_syn['translation']):
        food_new = create_all_vars([food])
        food_new_dt = pd.DataFrame({'name': food_new,
                           'id': [id]*len(food_new),
                           'type': [type]*len(food_new),
                           'translation': [trans]*len(food_new)})
        food_dt = food_dt.append(food_new_dt)


    food_dt = food_dt.drop_duplicates()
    food_dt.to_csv(output_csv_path, index=False)


