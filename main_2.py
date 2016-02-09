from nltk.stem.lancaster import LancasterStemmer
from sentence_processing import SentenceGraphCreator
from itertools import product

stemmer = LancasterStemmer()

def is_produce(path):
    path['stemmed_path'] = [stemmer.stem(word) for word in path['path']]
    verb_produce = False
    noun_producer = False
    if 'produc' in path['stemmed_path']:
        indices = [i for i, x in enumerate(path['stemmed_path']) if x == 'produc']
        for index in indices:
            if path['tags'][index].startswith('V'):
                verb_produce = True
            if path['path'][index] == 'producer':
                noun_producer = True
    return(any((verb_produce, noun_producer)))
    # delivering

def is_metabolize(path):
    path['stemmed_path'] = [stemmer.stem(word) for word in path['path']]
    verb_metabolize = False
    if 'metabol' in path['stemmed_path']:
        indices = [i for i, x in enumerate(path['stemmed_path']) if x == 'metabol']
        for index in indices:
            if path['tags'][index].startswith('V'):
                verb_metabolize = True
    if 'util' in path['stemmed_path']:
        indices = [i for i, x in enumerate(path['stemmed_path']) if x == 'util']
        for index in indices:
            if path['tags'][index].startswith('V'):
                verb_metabolize = True
    if 'hydrolys' in path['stemmed_path']:
        indices = [i for i, x in enumerate(path['stemmed_path']) if x == 'hydrolys']
        for index in indices:
            if path['tags'][index].startswith('V'):
                verb_metabolize = True
    return(verb_metabolize)


with open('natalia_out.txt') as f:
    data = [line.strip() for line in f.readlines()]
    titles =          [x for x in data[::6]]
    tokenized_sents = [x.split('\t') for x in data[1::6]]
    bacteria_lists =  [x.split('\t') for x in data[2::6]]
    nutrients_lists = [x.split('\t') for x in data[3::6]]
    raw_graphs =      [x.split('\t') for x in data[4::6]]
    data = zip(titles, tokenized_sents, bacteria_lists, nutrients_lists, raw_graphs)


unique_nutr = {}
unique_titles = {}
print('\t'.join(['title', 'sentence', 'bacteria', 'nutrient']))
for title, tokenized_sent, bacteria_list, nutrients_list, graph_raw in list(data)[:]:
    # sent = sp.sentence.replace('-RSB-', ']').replace('-LSB-', '[').replace('-RRB-', ')').replace('-LRB-', '(')
    sp = SentenceGraphCreator(' '.join(tokenized_sent))
    pairs = product(bacteria_list, nutrients_list)
    for bact, nutr in pairs:
        try:
            path = sp.search_path(bact, nutr)
        except:
            path = {}
        if path:
            im = is_metabolize(path)
            ip = is_produce(path)
            if im or ip:
                print('\t'.join([title, sp.sentence, bact, nutr]))
                # print(bact, nutr)
