from ohmygut.core.constants import PATH_NUTR_NAME, PATH_FIELD_TAG, PATH_FIELD_WORD, PATH_FIELD_REL, PATH_BACT_NAME, \
    PATH_FIELD_IND


# TODO: refactor
class PatternFinder(object):
    def __init__(self, stemmer, verb_stem_list):
        self.__stemmer = stemmer
        self.verb_stem_list = verb_stem_list

    def find_patterns(self, path, sentence_graph, sentence_words):
        verb_stem_ids = find_words(path[PATH_FIELD_WORD], self.verb_stem_list)
        nutr_id = path[PATH_FIELD_TAG].index(PATH_NUTR_NAME)
        bact_id = path[PATH_FIELD_TAG].index(PATH_BACT_NAME)
        patterns_verbs = []

        for verb_stem_id in verb_stem_ids:
            dist_nutr_verb = nutr_id - verb_stem_id
            dist_bact_verb = verb_stem_id - bact_id
            verb_stem_bind = path[PATH_FIELD_REL][verb_stem_id]
            verb_stem_type = path[PATH_FIELD_TAG][verb_stem_id]

            if pattern_1_requirement: patterns_verbs.append(('pattern_1', verb_stem_id))


def pattern_1_requirement(dist_nutr_verb, verb_stem_bind, verb_stem_type):
    return ((dist_nutr_verb == 1) &
            ('obj' in verb_stem_bind) &
            verb_stem_type.startswith('V'))

def pattern_1_1_requirement(dist_nutr_verb, verb_stem_bind, verb_stem_type):
    return ((dist_nutr_verb == 2) &
            ('obj' in verb_stem_bind) &
            verb_stem_type.startswith('V'))


def find_pattern_1(path, verbs):
    verb_ids = find_words(path[PATH_FIELD_WORD], verbs)
    nutr_id = path[PATH_FIELD_TAG].index(PATH_NUTR_NAME)

    verb_pattern = []
    is_there_pattern = False
    for verb_id in verb_ids:
        is_bact_near_verb = ((nutr_id - verb_id) == 1)
        is_binding_obj = ('obj' in path[PATH_FIELD_REL][verb_id])
        is_verb_a_verb = path[PATH_FIELD_TAG][verb_id].startswith('V')
        if is_bact_near_verb & is_binding_obj & is_verb_a_verb:
            is_there_pattern = True
            verb_pattern.append(path[PATH_FIELD_WORD][verb_id])
    return [is_there_pattern, verb_pattern]


def find_pattern_1_1(path, verbs):
    verb_ids = find_words(path[PATH_FIELD_WORD], verbs)
    nutr_id = path[PATH_FIELD_TAG].index(PATH_NUTR_NAME)

    verb_pattern = []
    is_there_pattern = False
    for verb_id in verb_ids:
        is_nutr_near_verb_2 = ((nutr_id - verb_id) == 2)
        is_binding_obj = ('obj' in path[PATH_FIELD_REL][verb_id])
        is_verb_a_verb = path[PATH_FIELD_TAG][verb_id].startswith('V')
        if is_nutr_near_verb_2 & is_binding_obj & is_verb_a_verb:
            is_there_pattern = True
            verb_pattern.append(path[PATH_FIELD_WORD][verb_id])
    return [is_there_pattern, verb_pattern]


def find_pattern_2(path, verbs, graph, word_dict):
    verb_ids = find_words(path[PATH_FIELD_WORD], verbs)
    bact_id = path[PATH_FIELD_TAG].index(PATH_BACT_NAME)

    verb_pattern = []
    is_there_pattern = False
    for verb_id in verb_ids:
        is_bact_near_verb_3 = ((verb_id - bact_id) < 3)
        is_binding_by = find_bindings(graph, word_dict, ind=path[PATH_FIELD_IND][verb_id - 1], list_words=['by'])
        is_verb_a_vbn = (path[PATH_FIELD_TAG][verb_id] == 'VBN')
        if is_bact_near_verb_3 & is_binding_by & is_verb_a_vbn:
            is_there_pattern = True
            verb_pattern.append(path[PATH_FIELD_WORD][verb_id])
    return [is_there_pattern, verb_pattern]


def find_pattern_2_1(path, verbs, graph, word_dict):
    verb_ids = find_words(path[PATH_FIELD_WORD], verbs)
    bact_id = path[PATH_FIELD_TAG].index(PATH_BACT_NAME)
    nutr_id = path[PATH_FIELD_TAG].index(PATH_NUTR_NAME)

    verb_pattern = []
    is_there_pattern = False
    for verb_id in verb_ids:
        is_bact_near_verb = ((verb_id - bact_id) == 1)
        is_nutr_near_verb = ((nutr_id - verb_id) == 1)
        is_binding_by = find_bindings(graph, word_dict, ind=path[PATH_FIELD_IND][bact_id], list_words=['by'])
        is_verb_a_vbn = (path[PATH_FIELD_TAG][verb_id] == 'VBN')
        if is_bact_near_verb & is_nutr_near_verb & is_binding_by & is_verb_a_vbn:
            is_there_pattern = True
    return is_there_pattern


def find_pattern_3(path, verbs, graph, word_dict):
    known_ids = find_words(path[PATH_FIELD_WORD], ['known'])

    verb_pattern = []
    is_there_pattern = False
    for known_id in known_ids:
        is_binding_verb = find_bindings(graph, word_dict, ind=path[PATH_FIELD_IND][known_id], list_words=verbs)
        if is_binding_verb:
            is_there_pattern = True
    return is_there_pattern


def find_pattern_4(path, verbs, graph, word_dict):
    bact_id = path[PATH_FIELD_TAG].index(PATH_BACT_NAME)
    nutr_id = path[PATH_FIELD_TAG].index(PATH_NUTR_NAME)

    verb_pattern = []
    is_there_pattern = False
    is_bact_near_nutr = ((nutr_id - bact_id) == 1)
    is_binding_obj = find_bindings_types(graph, word_dict, ind=path[PATH_FIELD_IND][nutr_id], list_types=['subj'])
    if is_binding_obj & is_bact_near_nutr:
        is_there_pattern = True
    return is_there_pattern


def find_pattern_5(path, verbs):
    verb_ids = find_words(path[PATH_FIELD_WORD], verbs)
    nutr_id = path[PATH_FIELD_TAG].index(PATH_NUTR_NAME)

    verb_pattern = []
    is_there_pattern = False
    for verb_id in verb_ids:
        is_nutr_near_verb = ((nutr_id - verb_id) == 1)
        is_verb_a_er = ('er' in path[PATH_FIELD_WORD][verb_id])
        if is_verb_a_er & is_nutr_near_verb:
            is_there_pattern = True
    return is_there_pattern


def find_pattern_6(path, verbs):
    verb_ids = find_words(path[PATH_FIELD_WORD], verbs)
    nutr_id = path[PATH_FIELD_TAG].index(PATH_NUTR_NAME)

    verb_pattern = []
    is_there_pattern = False
    for verb_id in verb_ids:
        is_nutr_near_verb = ((nutr_id - verb_id) == 1)
        is_verb_a_noun = path[PATH_FIELD_TAG][verb_id].startswith('N')
        if is_verb_a_noun & is_nutr_near_verb:
            is_there_pattern = True
    return is_there_pattern


def find_words(words, word_list):
    stemmer = LancasterStemmer()
    words_s = [stemmer.stem(word) for word in words]
    verbs_s = [stemmer.stem(verb) for verb in word_list]
    ind = [[i, x] for (i, x) in enumerate(words_s) if x in set(verbs_s).intersection(words_s)]
    return ind


def find_bindings(graph, word_dict, ind, list_words):
    graph = graph.to_undirected()
    ind_connected = list(graph[ind].keys())
    words_connected = [word_dict[i] for i in ind_connected]
    stemmer = LancasterStemmer()
    words_connected = [stemmer.stem(word) for word in words_connected]
    list_words = [stemmer.stem(word) for word in list_words]
    index = [i for (i, x) in enumerate(words_connected) if x in set(list_words).intersection(words_connected)]
    return (len(index) > 0)


def find_bindings_types(graph, word_dict, ind, list_types):
    graph = graph.to_undirected()
    ind_connected = list(graph[ind].keys())
    types_connected = [graph[ind][i]['rel'] for i in ind_connected]
    result = False
    for type in list_types:
        if any([type in x for x in types_connected]):
            result = True
    return result
