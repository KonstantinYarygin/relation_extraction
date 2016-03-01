# TODO: refactor
import numpy as np
from nltk import LancasterStemmer

from ohmygut.core.constants import PATH_NUTR_NAME, PATH_FIELD_TAG, PATH_FIELD_WORD, PATH_FIELD_REL, PATH_BACT_NAME, \
    PATH_FIELD_IND


def find_pattern_1(path, verbs):
    verb_ids = find_verbs(path[PATH_FIELD_WORD], verbs)
    nutr_id = path[PATH_FIELD_TAG].index(PATH_NUTR_NAME)

    is_there_pattern = False
    for verb_id in verb_ids:
        is_bact_near_verb = ((nutr_id - verb_id) == 1)
        is_binding_obj = ('obj' in path[PATH_FIELD_REL][verb_id])
        is_verb_a_verb = path[PATH_FIELD_TAG][verb_id].startswith('V')
        if is_bact_near_verb & is_binding_obj & is_verb_a_verb:
            is_there_pattern = True
    return is_there_pattern


def find_pattern_1_1(path, verbs):
    verb_ids = find_verbs(path[PATH_FIELD_WORD], verbs)
    nutr_id = path[PATH_FIELD_TAG].index(PATH_NUTR_NAME)

    is_there_pattern = False
    for verb_id in verb_ids:
        is_nutr_near_verb_2 = ((nutr_id - verb_id) == 2)
        is_binding_obj = ('obj' in path[PATH_FIELD_REL][verb_id])
        is_verb_a_verb = path[PATH_FIELD_TAG][verb_id].startswith('V')
        if is_nutr_near_verb_2 & is_binding_obj & is_verb_a_verb:
            is_there_pattern = True
    return is_there_pattern


def find_pattern_2(path, verbs, graph, word_dict):
    verb_ids = find_verbs(path[PATH_FIELD_WORD], verbs)
    bact_id = path[PATH_FIELD_TAG].index(PATH_BACT_NAME)

    is_there_pattern = False
    for verb_id in verb_ids:
        is_bact_near_verb_3 = ((verb_id-bact_id) < 3)
        is_binding_by = find_bindings(graph, word_dict, ind=path[PATH_FIELD_IND][verb_id-1], list_words=['by'])
        is_verb_a_vbn = path[PATH_FIELD_TAG][verb_id]=='VBN'
        if is_bact_near_verb_3 & is_binding_by & is_verb_a_vbn:
            is_there_pattern = True
    return is_there_pattern


def find_verbs(words, verbs):
    stemmer = LancasterStemmer()
    words_s = [stemmer.stem(word) for word in words]
    verbs_s = [stemmer.stem(verb) for verb in verbs]
    ind = [i for (i, x) in enumerate(words_s) if x in set(verbs_s).intersection(words_s)]
    return ind


def find_bindings(graph, word_dict, ind, list_words):
    graph = graph.to_undirected()
    ind_connected = list(graph[ind].keys())
    words_connected = [word_dict[i] for i in ind_connected]
    stemmer = LancasterStemmer()
    words_connected = [stemmer.stem(word) for word in words_connected]
    list_words = [stemmer.stem(word) for word in list_words]
    index = [i for (i, x) in enumerate(words_connected) if x in set(list_words).intersection(words_connected)]
    return (len(index)>0)