

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

    def find_bindings(self, sentence_graph, sentence_words, graph_index, mode='w'):
        """
        modes:
            i: indicies
            w: words
            t: types
        """
        graph = sentence_graph.to_undirected()
        indicies = list(graph[graph_index].keys())
        types = [graph[graph_index][i]['rel'] for i in indicies]
        words = [sentence_words[i] for i in indicies]
        ret = []
        for char in mode:
            if char == 'i':
                ret.append(indicies)
            elif char == 't':
                ret.append(types)
            elif char == 'w':
                ret.append(words)
        if len(ret) == 1:
            return ret[0]
        else:
            return zip(*ret)

    def find_patterns(self, path, sentence_graph=None, sentence_words=None):
        # [trigger_stem_ids, triggers] = self.find_words(path.words, self.__verb_list, return_value=True)
        bact_path_id = path.tags.index('BACTERIUM')
        dis_path_id = path.tags.index('DISEASE')
        patterns_verbs = []

        pattern_1 = self.is_pattern_1(path, sentence_graph, sentence_words)
        if pattern_1:
            patterns_verbs.append(['pattern_1', pattern_1])

        pattern_2 = self.is_pattern_2(bact_path_id, dis_path_id, path)
        if pattern_2:
            patterns_verbs.append(['pattern_2', pattern_2])

        pattern_3 = self.is_pattern_3(dis_path_id, path)
        if pattern_3:
            patterns_verbs.append(['pattern_3', pattern_3])

        pattern_4 = self.is_pattern_4(sentence_graph, sentence_words, path)
        if pattern_4:
            patterns_verbs.append(['pattern_4', pattern_4])

        pattern_5 = self.is_pattern_5(bact_path_id, dis_path_id, sentence_graph, sentence_words, path)
        if pattern_5:
            patterns_verbs.append(['pattern_5', pattern_5])

        return patterns_verbs

    def is_pattern_0(self, bact_path_id, dis_path_id, path):
        words = path.words
        triggers = [
            'prevention',
            'enriched',
            'occurs',
            'factor',
            'exacebrate',
            'over-represented',
            'overrepresented',
            'under-represented',
            'underrepresented',
            'induce',
            'responsible',
            'mediates']
        [trigger_stem_ids, triggers] = self.find_words(path.words, triggers, return_value=True)
        return triggers

    def is_pattern_1(self, path, sentence_graph, sentence_words):
        triggers = {'presence', 'abundance', 'prevalence', 'amount',
            'occurrence', 'richness', 'proportion', 'incidence', 'quantity',
            'fraction', 'portion', 'percentage', 'carriage', 'number'}
        qual_neg = {'reduce', 'lower', 'diminish', 'decreased',
            'less', 'smaller'}
        qual_pos = {'increase', 'greater', 'enhanced', 'elevated',
            'higher', 'larger'}
        trigger_stems = {self.__stemmer.stem(trigger) for trigger in triggers}
        qual_neg_stems = {self.__stemmer.stem(qual) for qual in qual_neg}
        qual_pos_stems = {self.__stemmer.stem(qual) for qual in qual_pos}

        path_stems = [self.__stemmer.stem(word) for word in path.words]

        trigger_path_ids = [i for i, stem in enumerate(path_stems) if stem in trigger_stems]

        if not trigger_path_ids:
            return False

        trigger_path_id = trigger_path_ids[0]
        trigger_graph_id = path.nodes_indexes[trigger_path_id]
        trigger_binds = [bind for bind in self.find_bindings(sentence_graph, sentence_words, trigger_graph_id)]
        trigger_binds_stems = [self.__stemmer.stem(bind) for bind in trigger_binds]

        pos_qual = any(bind_stem in qual_pos_stems for bind_stem in trigger_binds_stems)
        neg_qual = any(bind_stem in qual_neg_stems for bind_stem in trigger_binds_stems)

        if pos_qual:
            return 'positive'
        elif neg_qual:
            return 'negative'
        else:
            return False


    def is_pattern_2(self, bact_path_id, dis_path_id, path):
        words_stems = [self.__stemmer.stem(word) for word in path.words]
        for index in range(bact_path_id+1, min(bact_path_id+3, dis_path_id)):
            if words_stems[index] == 'increas':
                return 'positive'
            if words_stems[index] == 'decreas':
                return 'negative'
        return False

    def is_pattern_3(self, dis_path_id, path):
        # cause provoke exacerbate induce initiate promote stimulate dampen
        # prevent attenuate inhibit ameliorate alleviate counteract mitigate protect suppress treat

        # Использцю префиксы потому что стеммер работает слишком радикально
        # например stem('prevent') == stem('prevalence') == 'prev'
        caus_prefixes = ['caus', 'provok', 'exacerb', 'induc', 'initia', 'promot', 'stimulat', 'damp']
        prev_prefixes = ['preven', 'attenuat', 'inhibit', 'ameliorat', 'alleviat', 'counteract', 'mitigat', 'protect', 'suppres', 'treat']

        caus_path_ids = [i for i, word in enumerate(path.words) if any(word.startswith(prefix) for prefix in caus_prefixes)]
        prev_path_ids = [i for i, word in enumerate(path.words) if any(word.startswith(prefix) for prefix in prev_prefixes)]

        if prev_path_ids:
            prev_path_id = max(prev_path_ids)
            dist_condition = abs(dis_path_id - prev_path_id) <= 2
            if dist_condition:
                return 'prevent'
        elif caus_path_ids:
            caus_path_id = max(caus_path_ids)
            dist_condition = abs(dis_path_id - caus_path_id) <= 2
            if dist_condition:
                return 'cause'
        return False

    def is_pattern_4(self, sentence_graph, sentence_words, path):
        words_stems = [self.__stemmer.stem(word) for word in path.words]
        corr_path_ids = [i for i, stem in enumerate(words_stems) if stem == 'correl']
        corr_graph_ids = [path.nodes_indexes[id] for id in corr_path_ids]
        corr_binds = [bind for id in corr_graph_ids for bind in self.find_bindings(sentence_graph, sentence_words, id)]
        corr_binds = {self.__stemmer.stem(bind) for bind in corr_binds}
        neg_stems = {'invers', 'neg'}

        corr_condition = bool(corr_path_ids)
        neg_condition = any(bind in neg_stems for bind in corr_binds)
        if corr_condition:
            if neg_condition:
                return 'negative'
            else:
                return 'positive'
        else:
            return False

    def is_pattern_5(self, bact_path_id, dis_path_id, sentence_graph, sentence_words, path):
        # cause provoke exacerbate induce initiate promote stimulate dampen
        # prevent attenuate inhibit ameliorate alleviate counteract mitigate protect suppress treat

        # Использцю префиксы потому что стеммер работает слишком радикально
        # например stem('prevent') == stem('prevalence') == 'prev'
        caus_prefixes = ['caus', 'provok', 'exacerb', 'induc', 'initia', 'promot', 'stimulat', 'damp']
        prev_prefixes = ['preven', 'attenuat', 'inhibit', 'ameliorat', 'alleviat', 'counteract', 'mitigat', 'protect', 'suppres', 'treat']

        dis_graph_id = path.nodes_indexes[dis_path_id]
        dis_binds = self.find_bindings(sentence_graph, sentence_words, dis_graph_id)

        caus_condition = any(bind.startswith(prefix) for bind in dis_binds for prefix in caus_prefixes)
        prev_condition = any(bind.startswith(prefix) for bind in dis_binds for prefix in prev_prefixes)
        dist_condition = abs(bact_path_id - dis_path_id) == 1

        if prev_condition and dist_condition:
            return 'prevent'
        elif caus_condition and dist_condition:
            return 'cause'
        else:
            return False
