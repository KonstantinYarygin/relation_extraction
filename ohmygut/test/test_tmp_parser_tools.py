import unittest

import networkx as nx
import numpy as np
from nltk import LancasterStemmer

from ohmygut.core.analyzer import ShortestPath
from ohmygut.core.pattern_finder import PatternFinder, find_bindings


class MyTestCase(unittest.TestCase):
    def test_find_words(self):
        words = ['ab', 'cd', 'kl', 'mn', 'degrades', 'utilise', 'utilises', 'like', 'produces', 'degraded']
        verb_list = ['produce', 'degrade', 'utilise']
        target = PatternFinder({'verbs': verb_list}, LancasterStemmer())
        expected = [4, 5, 6, 8, 9]
        actual = target.find_words(words, verb_list)
        self.assertEqual(actual, expected)

    def test_find_words_values(self):
        words = ['ab', 'cd', 'kl', 'mn', 'degrades', 'utilise', 'utilises', 'like', 'produces', 'degraded']
        verb_list = ['produce', 'degrade', 'utilise']
        target = PatternFinder({'verbs': verb_list}, LancasterStemmer())
        expected = [[4, 5, 6, 8, 9], ['degrade', 'utilise', 'utilise', 'produce', 'degrade']]
        actual = target.find_words(words, verb_list, return_value=True)
        self.assertEqual(actual, expected)

    def test_find_bindings(self):
        [sentence_text, G, words, path] = get_text_G_words_path_2()
        actual = find_bindings(sentence_graph=G, sentence_words=words, graph_index=25)
        expected = ['by', 'many', 'produced', 'Lactococcus lactis']
        np.testing.assert_equal(np.array(actual).sort(), np.array(expected).sort())

    def test_find_bindings_types(self):
        [sentence_text, G, words, path] = get_text_G_words_path_2()
        actual = find_bindings(sentence_graph=G, sentence_words=words, graph_index=25, types=True)
        expected = ['case', 'nmod', 'nmod', 'amod']
        np.testing.assert_equal(np.array(actual).sort(), np.array(expected).sort())

    def test_find_pattern_1(self):
        input_path = get_true_sentence_pattern_1()
        verb_dict = {'verbs': ['hydrolyze']}
        target = PatternFinder(verb_dict, LancasterStemmer())
        expected = [('pattern 1', 'hydrolyze')]
        actual = target.find_patterns(input_path)
        self.assertEqual(actual, expected)

    def test_find_pattern_1_1(self):
        input_path = get_true_sentence_pattern_1_1()
        verb_list = {'verbs': ['utilize']}
        target = PatternFinder(verb_list, LancasterStemmer())
        expected = [('pattern 1.1', 'utilize')]
        actual = target.find_patterns(input_path)
        self.assertEqual(actual, expected)

    def test_find_pattern_1_false(self):
        input_path = get_true_sentence_pattern_1()
        verb_list = {'verbs': ['utilize']}
        target = PatternFinder(verb_list, LancasterStemmer())
        expected = []
        actual = target.find_patterns(input_path)
        self.assertEqual(actual, expected)

    def test_find_pattern_1_empty(self):
        input_path = get_true_sentence_pattern_1()
        verb_list = {}
        target = PatternFinder(verb_list, LancasterStemmer())
        expected = []
        actual = target.find_patterns(input_path)
        self.assertEqual(actual, expected)

    def test_find_pattern_2(self):
        [sentence_text, G, words, path] = get_text_G_words_path_2()
        verb_list = {'verbs': ['produce']}
        target = PatternFinder(verb_list, LancasterStemmer())
        expected = [('pattern 2', 'produce')]
        actual = target.find_patterns(path, sentence_graph=G, sentence_words=words)
        self.assertEqual(actual, expected)

    def test_find_pattern_2_1(self):
        [sentence_text, G, words, path] = get_text_G_words_path_2_1()
        verb_list = {'verbs': ['produce', 'utilize']}
        target = PatternFinder(verb_list, LancasterStemmer())
        expected = [('pattern 2.1', 'utilize')]
        actual = target.find_patterns(path, sentence_graph=G, sentence_words=words)
        self.assertEqual(actual, expected)

    def test_find_pattern_3(self):
        [sentence_text, G, words, path] = get_text_G_words_path_3()
        verb_list = {'verbs': ['produce', 'utilize']}
        target = PatternFinder(verb_list, LancasterStemmer())
        expected = [('pattern 3', ['produce'])]
        actual = target.find_patterns(path, sentence_graph=G, sentence_words=words)
        self.assertEqual(actual, expected)

    def test_find_pattern_4(self):
        [sentence_text, G, words, path] = get_text_G_words_path_4()
        verb_list = {'verbs': ['look']}
        target = PatternFinder(verb_list, LancasterStemmer())
        expected = [('pattern 4', [])]
        actual = target.find_patterns(path, sentence_graph=G, sentence_words=words)
        self.assertEqual(actual, expected)

    def test_find_pattern_5(self):
        input_path = get_true_sentance_pattern_5()
        verb_list = {'verbs': ['degrade']}
        target = PatternFinder(verb_list, LancasterStemmer())
        expected = [('pattern 5', 'degrade')]
        actual = target.find_patterns(input_path)
        self.assertEqual(actual, expected)

    def test_find_pattern_6(self):
        input_path = get_true_sentance_pattern_6()
        verb_list = {'verbs': ['produce', 'degrade']}
        target = PatternFinder(verb_list, LancasterStemmer())
        expected = [('pattern 6', 'produce')]
        actual = target.find_patterns(input_path)
        self.assertEqual(actual, expected)

    def test_find_pattern_5_6(self):
        input_path = get_true_sentance_pattern_5_6()
        verb_list = {'verbs': ['produce', 'degrade']}
        target = PatternFinder(verb_list, LancasterStemmer())
        expected = [('pattern 6', 'degrade'), ('pattern 5', 'degrade')]
        actual = target.find_patterns(input_path)
        np.testing.assert_equal(np.array(actual).sort(), np.array(expected).sort())


def get_true_sentence_pattern_1():
    return ShortestPath(edge_rels=['acl:relcl', 'dobj', 'acl', 'dobj'],
                 words=['Actinobacteria', 'have', 'ability', 'hydrolyze', 'cellulose'],
                 tags=['BACTERIUM', 'VBP', 'NN', 'VB', 'NUTRIENT'],
                 nodes_indexes=[1, 2, 3, 4, 5])


def get_true_sentence_pattern_1_1():
    return ShortestPath(edge_rels=['nsubj', 'xcomp', 'dobj', 'conj'],
                        words=['E. aphidicola', 'able', 'utilize', 'inositol', 'sorbitol'],
                        tags=['BACTERIUM', 'JJ', 'VB', 'JJ', 'NUTRIENT'],
                        nodes_indexes=[1, 2, 3, 4, 5])


def get_text_G_words_path_2():
    sentence_text = 'Sugar, a polycyclic antibacterial peptide 34 amino acid residues long, is one of ' \
                    'the most studied bacteriocins and is produced by many strains of Lactococcus lactis.'
    G = nx.DiGraph([])
    G.add_nodes_from(range(1, 28))
    G.add_edges_from([(1, 14, {'rel': 'nsubj'}), (3, 5, {'rel': 'det'}), (4, 5, {'rel': 'amod'}),
                      (5, 6, {'rel': 'nsubj'}), (6, 14, {'rel': 'parataxis'}), (7, 10, {'rel': 'nummod'}),
                      (8, 10, {'rel': 'amod'}), (9, 10, {'rel': 'compound'}),
                      (10, 6, {'rel': 'dobj'}), (11, 6, {'rel': 'advmod'}), (13, 14, {'rel': 'cop'}),
                      (15, 19, {'rel': 'case'}), (16, 19, {'rel': 'det'}), (17, 19, {'rel': 'amod'}),
                      (18, 19, {'rel': 'nummod'}), (19, 14, {'rel': 'nmod'}), (20, 14, {'rel': 'cc'}),
                      (21, 22, {'rel': 'auxpass'}), (22, 14, {'rel': 'conj'}), (23, 25, {'rel': 'case'}),
                      (24, 25, {'rel': 'amod'}), (25, 22, {'rel': 'nmod'}), (26, 27, {'rel': 'case'}),
                      (27, 25, {'rel': 'nmod'})])
    words = {1: 'Sugar', 3: 'a', 4: 'polycyclic', 5: 'antibacterial',
             6: 'peptide', 7: '34', 8: 'amino', 9: 'acid', 10: 'residues',
             11: 'long', 13: 'is', 14: 'one', 15: 'of', 16: 'the', 17: 'most',
             18: 'studied', 19: 'bacteriocins', 20: 'and', 21: 'is', 22: 'produced',
             23: 'by', 24: 'many', 25: 'strains', 26: 'of', 27: 'Lactococcus lactis'}

    path = ShortestPath(edge_rels=['nmod', 'nmod', 'conj', 'nsubj'],
                        words=['Lactococcus lactis', 'strains', 'produced', 'one', 'Sugar'],
                        tags=['BACTERIUM', 'NNS', 'VBN', 'CD', 'NUTRIENT'],
                        nodes_indexes=[27, 25, 22, 14, 1])
    return [sentence_text, G, words, path]


def get_text_G_words_path_2_1():
    sentence_text = 'The Roseburia genus, which is significantly reduced in all IBD patients (including iCD), ' \
                    'and the Ruminococcaceae are further functionally connected in that the latter consume hydrogen ' \
                    'and produce sugar that can be utilized by Roseburia to produce byterate.'
    G = nx.DiGraph([])
    G.add_nodes_from(range(1, 43))
    G.add_edges_from([(1, 2, {'rel': 'det'}), (2, 3, {'rel': 'nsubj'}), (5, 8, {'rel': 'nsubjpass'}),
                      (6, 8, {'rel': 'auxpass'}), (7, 8, {'rel': 'advmod'}), (8, 3, {'rel': 'ccomp'}),
                      (9, 12, {'rel': 'case'}), (10, 12, {'rel': 'det'}), (11, 12, {'rel': 'compound'}),
                      (12, 8, {'rel': 'nmod'}), (14, 15, {'rel': 'case'}), (15, 8, {'rel': 'dep'}),
                      (18, 3, {'rel': 'cc'}), (19, 20, {'rel': 'det'}), (20, 24, {'rel': 'nsubjpass'}),
                      (21, 24, {'rel': 'auxpass'}), (22, 24, {'rel': 'advmod'}), (23, 24, {'rel': 'advmod'}),
                      (24, 3, {'rel': 'conj'}), (25, 24, {'rel': 'dep'}), (26, 29, {'rel': 'mark'}),
                      (27, 28, {'rel': 'det'}), (28, 29, {'rel': 'nsubj'}), (29, 24, {'rel': 'ccomp'}),
                      (30, 29, {'rel': 'dobj'}), (31, 29, {'rel': 'cc'}), (32, 29, {'rel': 'conj'}),
                      (33, 32, {'rel': 'dobj'}), (34, 37, {'rel': 'nsubjpass'}), (35, 37, {'rel': 'aux'}),
                      (36, 37, {'rel': 'auxpass'}), (37, 33, {'rel': 'acl:relcl'}), (38, 39, {'rel': 'case'}),
                      (39, 37, {'rel': 'nmod'}), (40, 41, {'rel': 'mark'}), (41, 37, {'rel': 'xcomp'}),
                      (42, 41, {'rel': 'dobj'})])
    words = {1: 'The', 2: 'Roseburia', 3: 'genus', 5: 'which', 6: 'is', 7: 'significantly', 8: 'reduced',
             9: 'in', 10: 'all', 11: 'IBD', 12: 'patients', 14: 'including', 15: 'iCD', 18: 'and', 19: 'the',
             20: 'Ruminococcaceae', 21: 'are', 22: 'further', 23: 'functionally', 24: 'connected', 25: 'in',
             26: 'that', 27: 'the', 28: 'latter', 29: 'consume', 30: 'hydrogen', 31: 'and', 32: 'produce',
             33: 'sugar', 34: 'that', 35: 'can', 36: 'be', 37: 'utilized', 38: 'by', 39: 'Roseburia', 40: 'to',
             41: 'produce', 42: 'byterate'}

    path = ShortestPath(edge_rels=['nmod', 'acl:relcl'],
                        words=['Roseburia', 'utilized', 'sugar'],
                        tags=['BACTERIUM', 'VBN', 'NUTRIENT'],
                        nodes_indexes=[39, 37, 33])
    return [sentence_text, G, words, path]


def get_text_G_words_path_3():
    sentence_text = 'Lactobacillus species are known to produce antimicrobial substances, including bacteriocins,' \
                    ' lactic acid, and hydrogen peroxide.'
    G = nx.DiGraph([])
    G.add_nodes_from(range(1, 19))
    G.add_edges_from([(1, 2, {'rel': 'compound'}), (2, 4, {'rel': 'nsubjpass'}), (3, 4, {'rel': 'auxpass'}),
                      (5, 6, {'rel': 'mark'}), (6, 4, {'rel': 'xcomp'}), (7, 8, {'rel': 'amod'}),
                      (8, 6, {'rel': 'dobj'}), (10, 11, {'rel': 'case'}), (11, 4, {'rel': 'nmod'}),
                      (13, 14, {'rel': 'amod'}), (14, 11, {'rel': 'conj'}), (16, 11, {'rel': 'cc'}),
                      (17, 18, {'rel': 'compound'}), (18, 11, {'rel': 'conj'})])

    words = {1: 'Lactobacillus', 2: 'species', 3: 'are', 4: 'known', 5: 'to', 6: 'produce', 7: 'antimicrobial',
             8: 'substances', 10: 'including', 11: 'bacteriocins', 13: 'lactic', 14: 'acid', 16: 'and',
             17: 'sugar', 18: 'peroxide'}

    path = ShortestPath(edge_rels=['compound', 'nsubjpass', 'nmod', 'conj', 'compound'],
                        words=['Lactobacillus', 'species', 'known', 'bacteriocins', 'peroxide', 'sugar'],
                        tags=['BACTERIUM', 'NNS', 'VBN', 'NNS', 'NN', 'NUTRIENT'],
                        nodes_indexes=[1, 2, 4, 11, 18, 17])
    return [sentence_text, G, words, path]


def get_text_G_words_path_4():
    sentence_text = 'E. coli sugar always looks good'
    G = nx.DiGraph([])
    G.add_nodes_from(range(1, 7))
    G.add_edges_from([(1, 3, {'rel': 'compound'}), (3, 5, {'rel': 'nsubj'}), (4, 5, {'rel': 'advmod'}),
                      (6, 5, {'rel': 'xcomp'})])
    words = {1: 'E. coli', 3: 'sugar', 4: 'always', 5: 'looks', 6: 'good'}
    path = ShortestPath(edge_rels=['compound'],
                        words=['E. coli', 'sugar'],
                        tags=['BACTERIUM', 'NUTRIENT'],
                        nodes_indexes=[1, 3])
    return [sentence_text, G, words, path]


def get_true_sentance_pattern_5():
    return ShortestPath(edge_rels=['dep', 'ccomp', 'nsubj'],
                        words=['Rikenellaceae', 'fermenters', 'degraders', 'cellulose'],
                        tags=['BACTERIUM', 'NNS', 'VBZ', 'NUTRIENT'],
                        nodes_indexes=[12, 8, 44, 20])


def get_true_sentance_pattern_6():
    return ShortestPath(edge_rels=['nsubj', 'dobj', 'compound'],
                        words=['E. coli', 'require', 'production', 'sugar'],
                        tags=['BACTERIUM', 'VBP', 'NN', 'NUTRIENT'],
                        nodes_indexes=[1, 4, 6, 5])

def get_true_sentance_pattern_5_6():
    return ShortestPath(edge_rels=['dep', 'ccomp', 'nsubj'],
                        words=['Rikenellaceae', 'fermenters', 'degraders', 'cellulose'],
                        tags=['BACTERIUM', 'NNS', 'NN', 'NUTRIENT'],
                        nodes_indexes=[12, 8, 44, 20])


def get_graph_info():
    pass


if __name__ == '__main__':
    unittest.main()
