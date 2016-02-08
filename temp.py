with open('bacteria_nutrient_cooccur.tsv') as f:
    data = [line.strip().split('\t') for line in f.readlines()[1:]]
    data = [rec for rec in data if len(rec) == 4]

pairs_dict = {line: {'sents': set(), 'titles': set()} for line in ['|'.join(rec[2:]) for rec in data]}

for line in data:
    pairs_dict['|'.join(line[2:])]['sents'].add(line[1])
    pairs_dict['|'.join(line[2:])]['titles'].add(line[0])

out = [pair.split('|') + [len(pairs_dict[pair]['sents']), len(pairs_dict[pair]['titles'])] for pair in pairs_dict]
out.sort(reverse=True, key=lambda x: x[2])
print('bateria\tnutrient\tnum_of_sentences\tnum_of_articles')
for line in out:
    print('\t'.join(map(str, line)))