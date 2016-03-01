import unittest

import networkx as nx

from ohmygut.core.sentence_processing import SentenceParser
from ohmygut.core.tmp_parser_tools import find_pattern_1, find_verbs, find_bindings, find_pattern_2


class MyTestCase(unittest.TestCase):
    def test_find_pattern_1(self):
        input = get_true_sentance_pattern_1()
        verb_list = ['produce']
        expected = True
        actual = find_pattern_1(input, verb_list)
        self.assertEqual(actual, expected)

    def test_find_pattern_1_empty(self):
        input = get_true_sentance_pattern_1()
        verb_list = ['eat']
        expected = False
        actual = find_pattern_1(input, verb_list)
        self.assertEqual(actual, expected)

    def test_find_pattern_2(self):
        [sentence_text, G, words, path] = get_text_G_words_path_2()
        verb_list = ['produce']
        expected = True
        actual = find_pattern_2(path, verb_list, G, words)
        self.assertEqual(actual, expected)

    def test_find_verbs(self):
        words = ['ab', 'cd', 'kl', 'mn', 'degrades', 'utilise', 'utilises', 'like', 'produces', 'degraded']
        verb_list = ['produce', 'degrade', 'utilise']
        expected = [4, 5, 6, 8, 9]
        actual = find_verbs(words, verb_list)
        self.assertEqual(actual, expected)

    def test_find_bindings(self):
        [sentence_text, G, words, path] = get_text_G_words_path_2()
        actual = find_bindings(graph=G, word_dict=words, ind=5, list_words=['by'])
        expected = True
        self.assertEqual(actual, expected)


def get_true_sentance_pattern_1():
    return {'edge_rels': ['subj', 'yy', 'nobj'],
            'words': ['E. coli', 'nunu', 'produces', 'protein'],
            'tags': ['BACTERIUM', 'NN', 'VB', 'NUTRIENT'],
            'pos_path': [1, 2, 3, 4]}


def get_text_G_words_path_2():
    sentence_text = 'Protein is produced by Lactobacillus.'
    G = nx.DiGraph([])
    G.add_nodes_from([1, 2, 3, 4, 5])
    G.add_edges_from([(1, 3, {'rel': 'nsubjpass'}), (2, 3, {'rel': 'auxpass'}), (4, 5, {'rel': 'case'}),
                      (5, 3, {'rel': 'nmod'})])
    words = {1: 'Protein', 2: 'is', 3: 'produced', 4: 'by', 5: 'Lactobacillus'}
    path = {'edge_rels': ['nmod', 'nsubjpass'],
            'words': ['Lactobacillus', 'produced', 'Protein'],
            'tags': ['BACTERIUM', 'VBN', 'NUTRIENT'],
            'pos_path': [5, 3, 1]}
    return [sentence_text, G, words, path]


def get_graph_info():
    pass


if __name__ == '__main__':
    unittest.main()
