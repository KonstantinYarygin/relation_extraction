import unittest
from ohmygut.core.tmp_parser_tools import find_pattern_1, find_verbs



class MyTestCase(unittest.TestCase):
    def test_find_pattern_1(self):
        input = get_true_sentance()
        verb_list = ['produce']
        expected = True
        actual = find_pattern_1(input, verb_list)
        self.assertEqual(actual, expected)

    def test_find_pattern_empty(self):
        input = get_true_sentance()
        verb_list = ['eat']
        expected = False
        actual = find_pattern_1(input, verb_list)
        self.assertEqual(actual, expected)

    def test_find_verbs(self):
        words = ['ab', 'cd', 'kl', 'mn', 'degrades', 'utilise', 'utilises', 'like', 'produces', 'degraded']
        verb_list = ['produce', 'degrade', 'utilise']
        expected = [4, 5, 6, 8, 9]
        actual = find_verbs(words, verb_list)
        self.assertEqual(actual, expected)

def get_true_sentance():
    return {'edge_rels': ['subj', 'yy', 'nobj'],
            'words': ['E. coli', 'nunu', 'produces', 'protein'],
            'tags': ['BACTERIUM', 'NN', 'VB', 'NUTRIENT']}

if __name__ == '__main__':
    unittest.main()
