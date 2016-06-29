import re

import pandas as pd

from analysis.obo import Parser
from catalog_preparation.catalog_creation_helper import remove_literally, all_cases_of_cases


def parse_obo(obo_path):
    parser = Parser(obo_path)
    disease_data = pd.DataFrame(columns=['id', 'name', 'group', 'obsolete'])
    # take each stanza, take it's synonyms and write it down into DataFrame!
    # stanza is entry in OBO format; see spec: https://oboformat.googlecode.com/svn/trunk/doc/GO.format.obo-1_2.html
    for stanza in parser.stanzas():
        if stanza.name != 'Term':
            # 'Term' contains disease info
            continue
        name = stanza.tags['name'][0].value
        disease_id = stanza.tags['id'][0].value
        try:
            is_obsolete = stanza.tags['is_obsolete'][0].value
        except:
            is_obsolete = 'false'
        try:
            synonyms = [synonym.value for synonym in stanza.tags['synonym']]
        except:
            synonyms = []
        try:
            groups = [group.value for group in stanza.tags['is_a']]
        except:
            groups = ['NA']

        names = [name] + synonyms

        # apostrophe1_names = [name.replace('\'', '’') for name in names if '\'' in name]
        # apostrophe2_names = [name.replace('’', '\'') for name in names if '’' in name]
        names = [re.sub('[’\']', '', name) for name in names]

        for disease_name in names:
            for group in groups:
                entry = {'id': disease_id,
                         'name': disease_name,
                         'group': group,
                         'obsolete': is_obsolete}
                disease_data = disease_data.append(entry, ignore_index=True)
    return disease_data

obo_path = "../data/diseases/doid.obo"
output_path = '../data/diseases/diseases_catalog.csv'

if __name__ == '__main__':
    disease_data = parse_obo(obo_path)
    disease_data = remove_literally(disease_data, ['disease'])
    disease_data_cases = all_cases_of_cases(disease_data)
    disease_data = pd.merge(disease_data, disease_data_cases, on=list(disease_data), how='outer')
    disease_data = disease_data.drop_duplicates()
    disease_data.to_csv(output_path, index=False, sep='\t')