import pandas as pd

from analysis.obo import Parser

parser = Parser("../data/diseases/doid.obo")
disease_data = pd.DataFrame(columns=['id', 'name', 'subset'])
# take each stanza, take it's synonyms and write it down into DataFrame!
# stanza is entry in OBO format; see spec: https://oboformat.googlecode.com/svn/trunk/doc/GO.format.obo-1_2.html
for stanza in parser.stanzas():
    name = stanza.tags['name'][0].value
    disease_id = stanza.tags['id'][0].value
    try:
        subsets = [subset.value for subset in stanza.tags['subset']]
    except:
        subsets = ['NA']
    try:
        synonyms = [synonym.value for synonym in stanza.tags['synonyms']]
    except:
        synonyms = []

    names = [name] + synonyms
    entries = []
    for disease_name in names:
        for subset in subsets:
            # id, name, subset
            entry = {'id': disease_id, 'name': disease_name, 'subset': subset}
            disease_data = disease_data.append(entry, ignore_index=True)

disease_data.to_csv("disease.csv", index=False, sep='\t')
