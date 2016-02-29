# TODO: refactor
import numpy as np
from nltk import LancasterStemmer


def find_pattern_1(path, verbs):
    verb_ids = find_verbs(path['words'], verbs)
    nutr_id = path['tags'].index('NUTRIENT')

    is_there_pattern = False
    for verb_id in verb_ids:
        if ((nutr_id - verb_id) == 1 &
            ('obj' in path['edge_rels'][verb_id])):
            is_there_pattern = True
    return is_there_pattern



def find_verbs(words, verbs):
    stemmer = LancasterStemmer()
    words_s = [stemmer.stem(word) for word in words]
    verbs_s = [stemmer.stem(verb) for verb in verbs]
    ind = [i for (i, x) in enumerate(words_s) if x in set(verbs_s).intersection(words_s)]
    return ind
