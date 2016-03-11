
class PatternFinder(object):
    def __init__(self, stemmer, verb_ontology):
        self.__stemmer = stemmer
        self.__verb_ontology = verb_ontology
        self.__verb_list = [verb for verb_list in verb_ontology.items() for verb in verb_list]

    def find_words(self, words, templates, return_value=False):
        words_stems = [self.__stemmer.stem(word) for word in words]
        templates_stems = [self.__stemmer.stem(template) for template in templates]
        ind = [i for (i, x) in enumerate(words_stems) if x in set(templates_stems).intersection(words_stems)]
        if return_value:
            template = [templates[templates_stems.index(words_stems[i])] for i in ind]
            return [ind, template]
        else:
            return ind

    def find_patterns(self, path, sentence_graph=None, sentence_words=None):
        [verb_stem_ids, verbs] = self.find_words(path.word, self.__verb_list, return_value=True)
        nutr_id = path.tags.index('NUTRIENT')
        bact_id = path.tags.index('BACTERIUM')
        dist_nutr_bact = nutr_id - bact_id
        patterns_verbs = []

        for verb_id, verb_name in zip(verb_stem_ids, verbs):
            dist_nutr_verb = nutr_id - verb_id
            dist_bact_verb = verb_id - bact_id

            if pattern_1_requirement(dist_nutr_verb, path.edge_rels[verb_id], path.tags[verb_id]):
                patterns_verbs.append(('pattern 1', verb_name))
            if pattern_1_1_requirement(dist_nutr_verb, path.edge_rels[verb_id], path.tags[verb_id]):
                patterns_verbs.append(('pattern 1.1', verb_name))
            if pattern_5_requirement(dist_nutr_verb, path.word[verb_id]):
                patterns_verbs.append(('pattern 5', verb_name))
            if pattern_6_requirement(dist_nutr_verb, path.tags[verb_id]):
                patterns_verbs.append(('pattern 6', verb_name))

        if sentence_graph:
            bact_by_binding = self.find_words(find_bindings(sentence_graph, sentence_words,
                                                            path.nodes_indexes[bact_id]), ['by'])
            bact_plus_1_by_binding = self.find_words(find_bindings(sentence_graph, sentence_words,
                                                                   path.nodes_indexes[bact_id + 1]), ['by'])
            nutr_type_binding = find_bindings(sentence_graph, sentence_words,
                                                        path.nodes_indexes[nutr_id], types=True)

            if pattern_4_requirement(dist_nutr_bact, nutr_type_binding):
                patterns_verbs.append(('pattern 4', []))

            for verb_id, verb_name in zip(verb_stem_ids, verbs):
                if pattern_2_requirement(dist_bact_verb, bact_plus_1_by_binding, path.tags[verb_id]):
                    patterns_verbs.append(('pattern 2', verb_name))
                if pattern_2_1_requirement(dist_bact_verb, bact_by_binding, path.tags[verb_id]):
                    patterns_verbs.append(('pattern 2.1', verb_name))

            known_ids = self.find_words(path.word, ['known'])
            for known_id in known_ids:
                known_id_binds = find_bindings(sentence_graph, sentence_words, path.nodes_indexes[known_id])
                [verb_ids, verbs] = self.find_words(known_id_binds, self.__verb_list, return_value=True)
                if pattern_3_requirement(verb_ids):
                    patterns_verbs.append(('pattern 3', verbs))

        return patterns_verbs


def pattern_1_requirement(dist_nutr_verb, verb_stem_bind, verb_type):
    return ((dist_nutr_verb == 1) &
            ('obj' in verb_stem_bind) &
            verb_type.startswith('V'))


def pattern_1_1_requirement(dist_nutr_verb, verb_stem_bind, verb_type):
    return ((dist_nutr_verb == 2) &
            ('obj' in verb_stem_bind) &
            verb_type.startswith('V'))


def pattern_2_requirement(dist_bact_verb, bact_plus_1_by_binding, verb_type):
    return ((dist_bact_verb < 3) &
            (verb_type == 'VBN') &
            (len(bact_plus_1_by_binding) > 0))


def pattern_2_1_requirement(dist_bact_verb, bact_by_binding, verb_type):
    return ((dist_bact_verb < 3) &
            (verb_type == 'VBN') &
            (len(bact_by_binding) > 0))


def pattern_3_requirement(known_verb_binding):
    return len(known_verb_binding) > 0


def pattern_4_requirement(dist_nutr_bact, nutr_type_binding):
    return ((dist_nutr_bact == 1) &
            any(['subj' in x for x in nutr_type_binding]))


def pattern_5_requirement(dist_nutr_verb, verb):
    return ((dist_nutr_verb == 1) &
            ('er' in verb))


def pattern_6_requirement(dist_nutr_verb, verb_type):
    return ((dist_nutr_verb == 1) &
            verb_type.startswith('N'))


def find_bindings(sentence_graph, sentence_words, graph_index, types=False):
    graph = sentence_graph.to_undirected()
    ind_connected = list(graph[graph_index].keys())
    if types:
        connections = [graph[graph_index][i]['rel'] for i in ind_connected]
    else:
        connections = [sentence_words[i] for i in ind_connected]
    return connections
