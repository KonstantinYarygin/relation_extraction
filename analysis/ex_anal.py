from collections import namedtuple, Counter
from itertools import product
import csv
import sys
import os

from ohmygut.core.catalog.bacteria_catalog import BacteriaCatalog
from ohmygut.core.catalog.nutrients_catalog import NutrientsCatalog
from ohmygut.core.catalog.diseases_catalog import DiseasesCatalog

bacteria_catalog = BacteriaCatalog(nodes_path='./data/bacteria/taxdump/nodes.dmp',
                                   names_path='./data/bacteria/taxdump/names.dmp')
bacteria_catalog.initialize(verbose=True)

nutrients_catalog = NutrientsCatalog(path='./data/nutrients/natalia_nitrients.txt')
nutrients_catalog.initialize(verbose=True)

diseases_catalog = DiseasesCatalog(doid_path='./data/diseases/doid.obo')
diseases_catalog.initialize(verbose=True)

output_record = namedtuple('output_record', ['sentence', 'title', 'bacteria', 'nutrients', 'diseases'])

with open('sentences.csv') as f:
    f.readline()
    data = csv.reader(f, delimiter=',')
    data = [record[:2] + list(map(eval, record[2:])) for record in data]
    data = [output_record(*record) for record in data]
bacteria_all = []
nutrients_all = []
diseases_all = []

bacteria_nutrients_pairs = []
nutrients_diseases_pairs = []
diseases_bacteria_pairs = []

for record in data:
    try:
        bacteria = list(set(bacteria_catalog.get_scientific_name(ncbi_id=ncbi_id) for bacteria_name, ncbi_id in record.bacteria))
    except:
        print(record)
        sys.exit()
    nutrients = list(set(record.nutrients))
    diseases = list(set(diseases_catalog.get_common_name(doid_id=doid_id) for disease_name, doid_id in record.diseases))
    bacteria_all.extend(bacteria)
    nutrients_all.extend(nutrients)
    diseases_all.extend(diseases)
    bacteria_nutrients_pairs.extend(list(product(bacteria, nutrients)))
    nutrients_diseases_pairs.extend(list(product(nutrients, diseases)))
    diseases_bacteria_pairs.extend(list(product(diseases, bacteria)))

bacteria_all = Counter(bacteria_all)
nutrients_all = Counter(nutrients_all)
diseases_all = Counter(diseases_all)
bacteria_nutrients_pairs = Counter(bacteria_nutrients_pairs)
nutrients_diseases_pairs = Counter(nutrients_diseases_pairs)
diseases_bacteria_pairs = Counter(diseases_bacteria_pairs)

with open('./analysis/bacteria.csv', 'w') as f:
    f.write('\n'.join('\t'.join(map(str, line)) for line in sorted(bacteria_all.items(), key=lambda x: int(x[1]), reverse=True)))
with open('./analysis/nutrients.csv', 'w') as f:
    f.write('\n'.join('\t'.join(map(str, line)) for line in sorted(nutrients_all.items(), key=lambda x: int(x[1]), reverse=True)))
with open('./analysis/diseases.csv', 'w') as f:
    f.write('\n'.join('\t'.join(map(str, line)) for line in sorted(diseases_all.items(), key=lambda x: int(x[1]), reverse=True)))

with open('./analysis/bacteria_nutrients_pairs.csv', 'w') as f:
    f.write('\n'.join('\t'.join([key[0], key[1], str(value)]) for key, value in sorted(bacteria_nutrients_pairs.items(), key=lambda x: int(x[1]), reverse=True)))
with open('./analysis/nutrients_diseases_pairs.csv', 'w') as f:
    f.write('\n'.join('\t'.join([key[0], key[1], str(value)]) for key, value in sorted(nutrients_diseases_pairs.items(), key=lambda x: int(x[1]), reverse=True)))
with open('./analysis/diseases_bacteria_pairs.csv', 'w') as f:
    f.write('\n'.join('\t'.join([key[0], key[1], str(value)]) for key, value in sorted(diseases_bacteria_pairs.items(), key=lambda x: int(x[1]), reverse=True)))
