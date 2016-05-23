

class PatternFinder(object):
    def __init__(self, verb_ontology, stemmer):
        self.__stemmer = stemmer
        self.__verb_ontology = verb_ontology
        self.__verb_list = [verb for verb_list in verb_ontology.values() for verb in verb_list]
        self.__relation_type_by_verb = {verb: type for type in verb_ontology for verb in verb_ontology[type]}

    def find_words(self, words, templates, return_value=False):
        words_stems = [self.__stemmer.stem(word) for word in words]
        templates_stems = [self.__stemmer.stem(template) for template in templates]
        ind = [i for (i, x) in enumerate(words_stems) if x in set(templates_stems).intersection(words_stems)]
        if return_value:
            template = [templates[templates_stems.index(words_stems[i])] for i in ind]
            return [ind, template]
        else:
            return ind

    def find_bindings(self, sentence_graph, sentence_words, graph_index, types=False):
        graph = sentence_graph.to_undirected()
        ind_connected = list(graph[graph_index].keys())
        if types:
            connections = [(sentence_words[i], graph[graph_index][i]['rel']) for i in ind_connected]
        else:
            connections = [sentence_words[i] for i in ind_connected]
        return connections

    def find_patterns(self, path, sentence_graph=None, sentence_words=None):
        [trigger_stem_ids, triggers] = self.find_words(path.words, self.__verb_list, return_value=True)
        nutr_id = path.tags.index('NUTRIENT')
        bact_id = path.tags.index('BACTERIUM')
        dist_nutr_bact = nutr_id - bact_id

        patterns_verbs = []
        for trigger_id, trigger in zip(trigger_stem_ids, triggers):
            trigger_tag = path.tags[trigger_id]
            trigger_word = path.words[trigger_id]
            trigger_edge_aft = path.edge_rels[trigger_id]

            pattern_verb = []

            if self.is_pattern_1(trigger_id, nutr_id, trigger_tag, trigger_edge_aft):
                pattern_verb = ['pattern 1', trigger, self.__relation_type_by_verb[trigger]]

            elif self.is_pattern_1_1(trigger_id, nutr_id, trigger_tag, trigger_edge_aft):
                pattern_verb = ['pattern 1.1', trigger, self.__relation_type_by_verb[trigger]]

            elif self.is_pattern_2(trigger_id, bact_id, trigger_tag, sentence_graph, sentence_words, path):
                pattern_verb = ['pattern 2', trigger, self.__relation_type_by_verb[trigger]]

            elif self.is_pattern_2_1(trigger_id, bact_id, trigger_tag, sentence_graph, sentence_words, path):
                pattern_verb = ['pattern 2.1', trigger, self.__relation_type_by_verb[trigger]]

            elif self.is_pattern_5(trigger_id, nutr_id, trigger_word):
                pattern_verb = ['pattern 5', trigger, self.__relation_type_by_verb[trigger]]

            elif self.is_pattern_6(trigger_id, nutr_id, trigger_tag):
                pattern_verb = ['pattern 6', trigger, self.__relation_type_by_verb[trigger]]

            if pattern_verb:
                pattern_type, trigger, trigger_type = pattern_verb
                nutr_binds = self.find_bindings(sentence_graph, sentence_words, path.nodes_indexes[nutr_id], types=True)

                if trigger_type == 'metabolize_general':
                    if ('to', 'case') in nutr_binds or \
                       ('into', 'case') in nutr_binds:
                        trigger_type = 'produce_general'
                        trigger = trigger + ' to'
                elif trigger_type == 'produce_general':
                    if ('from', 'case') in nutr_binds:
                        trigger_type = 'metabolize_general'
                        trigger = trigger + ' from'
                pattern_verb = [pattern_type, trigger, trigger_type]
                patterns_verbs.append(pattern_verb)

        return patterns_verbs

    def is_pattern_1(self, trigger_id, nutr_id, trigger_tag, trigger_edge_aft):
        dist_condition = abs(trigger_id - nutr_id) == 1
        tag_condition = trigger_tag.startswith('V')
        rel_condition = 'obj' in trigger_edge_aft
        return dist_condition and tag_condition and rel_condition

    def is_pattern_1_1(self, trigger_id, nutr_id, trigger_tag, trigger_edge_aft):
        dist_condition = abs(trigger_id - nutr_id) == 2
        tag_condition = trigger_tag.startswith('V')
        rel_condition = 'obj' in trigger_edge_aft
        return dist_condition and tag_condition and rel_condition

    def is_pattern_2(self, trigger_id, bact_id, trigger_tag, sentence_graph, sentence_words, path):
        second_word_binds = self.find_bindings(sentence_graph, sentence_words, path.nodes_indexes[bact_id + 1])

        dist_condition = abs(bact_id - trigger_id) < 3
        tag_condition = trigger_tag == 'VBN'
        by_condition = 'by' in second_word_binds
        return dist_condition and tag_condition and by_condition

    def is_pattern_2_1(self, trigger_id, bact_id, trigger_tag, sentence_graph, sentence_words, path):
        bact_word_binds = self.find_bindings(sentence_graph, sentence_words, path.nodes_indexes[bact_id])

        dist_condition = abs(bact_id - trigger_id) < 3
        tag_condition = trigger_tag == 'VBN'
        by_condition = 'by' in bact_word_binds
        return dist_condition and tag_condition and by_condition

    def is_pattern_5(self, trigger_id, nutr_id, trigger_word):
        dist_condition = abs(nutr_id - trigger_id) == 1
        er_condition = trigger_word.endswith('er') or trigger_word.endswith('ers')
        return dist_condition and er_condition

    def is_pattern_6(self, trigger_id, nutr_id, trigger_tag):
        dist_condition = abs(nutr_id - trigger_id) == 1
        noun_condition = trigger_tag.startswith('N')
        return dist_condition and noun_condition
