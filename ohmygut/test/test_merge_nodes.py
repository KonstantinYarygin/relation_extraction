import unittest
import pickle
import os

from time import time
import networkx as nx

from nltk.parse.stanford import StanfordDependencyParser
from nltk.tokenize import StanfordTokenizer
from nltk.tag import StanfordPOSTagger

from nltk.stem.lancaster import LancasterStemmer
from ohmygut.core.analyzer import merge_nodes
from ohmygut.core.sentence import Sentence
from ohmygut.core.sentence_processing import SentenceParser, ParserOutput

script_dir = os.path.dirname(os.path.realpath(__file__))
stanford_tokenizer = StanfordTokenizer(
    path_to_jar=os.path.join(script_dir, '../../stanford_parser/stanford-parser.jar')
)

stanford_dependency_parser = StanfordDependencyParser(
    path_to_jar=os.path.join(script_dir, '../../stanford_parser/stanford-parser.jar'),
    path_to_models_jar=os.path.join(script_dir, '../../stanford_parser/stanford-parser-3.5.2-models.jar'),
    model_path=os.path.join(script_dir, '../../stanford_parser/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'),
)

sentence_parser = SentenceParser(stanford_dependency_parser, stanford_tokenizer)

class TestCase(unittest.TestCase):
    def test_merge_nodes_1(self):

        bacterial_names = ['bb cc dd']
        disease_names = ['bb aa']

        nx_graph = nx.DiGraph()
        nx_graph.add_nodes_from([1, 2, 3, 4, 5])
        nx_graph.add_edges_from([
            (1, 2, {'rel': '1 -> 2'}),
            (1, 4, {'rel': '1 -> 4'}),
            (2, 3, {'rel': '2 -> 3'}),
            (2, 4, {'rel': '2 -> 4'}),
            (4, 5, {'rel': '4 -> 5'})]
        )
        words = {1: 'bb', 2: 'aa', 3: 'bb', 4: 'cc', 5: 'dd'}
        tags  = {1: 'T1', 2: 'T2', 3: 'T3', 4: 'T4', 5: 'T5'}
        parser_output = ParserOutput("a text", nx_graph, words, tags)

        merge_nodes(
            tokenizer = stanford_tokenizer,
            bacterial_names = bacterial_names,
            disease_names = disease_names,
            nutrient_names = [],
            food_names = [],
            parser_output = parser_output
        )

        edges = parser_output.nx_graph.edges()
        words = parser_output.words
        tags = parser_output.tags

        edges_expected = [(1, 3)]
        words_expected = {1: 'bb aa', 3: 'bb cc dd'}
        tags_expected = {1: 'DISEASE', 3: 'BACTERIUM'}

        self.assertEqual(edges_expected, edges)
        self.assertEqual(words_expected, words)
        self.assertEqual(tags_expected, tags)

    def test_merge_nodes_2(self):

        with open(os.path.join(script_dir, 'resource/sentence_for_merge_test.pkl'), 'rb') as f:
            sentence = pickle.load(f)

        bacterial_names = [name for name, ncbi_id in sentence.bacteria]
        disease_names   = [name for name, doid_id in sentence.diseases]
        nutrient_names  = [name for name, idname in sentence.nutrients]
        food_names      = [name for name, food_group in sentence.food]

        merge_nodes(
            tokenizer=stanford_tokenizer,
            bacterial_names=bacterial_names,
            disease_names=disease_names,
            nutrient_names=nutrient_names,
            food_names=food_names,
            parser_output=sentence.parser_output
        )

        edges = sentence.parser_output.nx_graph.edges()
        words = sentence.parser_output.words
        tags = sentence.parser_output.tags

        edges_expected = [(3, 4), (4, 1), (5, 4), (8, 5), (10, 11), (11, 5), (13, 5), (15, 5), (18, 5), (20, 22), (21, 22), (22, 5), (24, 5), (26, 28), (27, 28), (28, 5), (30, 5), (32, 33), (33, 5), (35, 5), (37, 41), (38, 41), (39, 41), (40, 41), (41, 5), (43, 5), (45, 46), (46, 5), (48, 5), (50, 52), (51, 52), (52, 5), (53, 52), (54, 56), (55, 56), (56, 52), (58, 5), (60, 61), (61, 5), (63, 5), (65, 66), (66, 5), (68, 5), (70, 72), (71, 72), (72, 5), (74, 5), (76, 78), (77, 78), (78, 5), (80, 5), (82, 86), (83, 86), (84, 86), (85, 86), (86, 5), (88, 89), (89, 5), (91, 93), (92, 93), (93, 5), (95, 5), (97, 102), (99, 102), (100, 102), (101, 102), (102, 5), (104, 5), (106, 110), (107, 110), (108, 110), (109, 110), (110, 5), (112, 5), (114, 117), (115, 117), (116, 117), (117, 5), (119, 5), (121, 125), (122, 125), (123, 125), (124, 125), (125, 5)]
        words_expected = {1: 'NAFLD', 2: ':', 3: 'Non-alcoholic', 4: 'fatty', 5: 'liver disease', 7: ';', 8: 'NASH', 9: ':', 10: 'Non-alcoholic', 11: 'steatohepatitis', 12: ';', 13: 'HCC', 14: ':', 15: 'Hepatocellular carcinoma', 17: ';', 18: 'FXR', 19: ':', 20: 'Farnesoid', 21: 'X', 22: 'receptor', 23: ';', 24: 'SHP', 25: ':', 26: 'Small', 27: 'hetrodimer', 28: 'partner', 29: ';', 30: 'CA', 31: ':', 32: 'Cholic', 33: 'acid', 34: ';', 35: 'NTCP', 36: ':', 37: 'Na', 38: '/', 39: 'taurocholate', 40: 'cotransporter', 41: 'polypeptide', 42: ';', 43: 'CYP7A1', 44: ':', 45: '7', 46: 'alpha-hydroxylase', 47: ';', 48: 'CDCArg', 49: ':', 50: 'L-Arginine', 51: 'ethyl', 52: 'ester', 53: 'and', 54: 'chenodeoxycholic', 55: 'acid', 56: 'conjugate', 57: ';', 58: 'CDCA', 59: ':', 60: 'Chenodeoxycholic', 61: 'acid', 62: ';', 63: 'UDCA', 64: ':', 65: 'Urosodeoxycholic', 66: 'acid', 67: ';', 68: 'LFD', 69: ':', 70: 'Low', 71: 'fat', 72: 'diet', 73: ';', 74: 'HFD', 75: ':', 76: 'High', 77: 'fat', 78: 'diet', 79: ';', 80: 'TGR5', 81: ':', 82: 'G', 83: 'protein-coupled', 84: 'bile', 85: 'acid', 86: 'receptor', 87: ';', 88: 'SGPT', 89: 'ALT', 90: ':', 91: 'Serum', 92: 'glutamic-pyruvic', 93: 'transaminase', 94: ';', 95: 'SGOT', 96: ':', 97: 'AST', 98: ',', 99: 'Serum', 100: 'glutamic', 101: 'oxaloacetic', 102: 'transaminase', 103: ';', 104: 'PGC1α', 105: ':', 106: 'Proliferator-activated', 107: 'receptor', 108: 'gamma', 109: 'coactivator', 110: '1-alpha', 111: ';', 112: 'PPARα', 113: ':', 114: 'Peroxisome', 115: 'proliferator-activated', 116: 'receptor', 117: 'alpha', 118: ';', 119: 'SREBP1c', 120: ':', 121: 'Sterol', 122: 'regulatory', 123: 'element-binding', 124: 'protein', 125: '1c', 126: '.'}
        tags_expected = {1: 'NNP', 2: 'NO_TAG', 3: 'JJ', 4: 'NN', 5: 'DISEASE', 7: 'NO_TAG', 8: 'NNP', 9: 'NO_TAG', 10: 'JJ', 11: 'NNS', 12: 'NO_TAG', 13: 'NNP', 14: 'NO_TAG', 15: 'DISEASE', 17: 'NO_TAG', 18: 'NNP', 19: 'NO_TAG', 20: 'NNP', 21: 'NNP', 22: 'NNP', 23: 'NO_TAG', 24: 'NNP', 25: 'NO_TAG', 26: 'JJ', 27: 'NN', 28: 'NN', 29: 'NO_TAG', 30: 'NNP', 31: 'NO_TAG', 32: 'JJ', 33: 'NN', 34: 'NO_TAG', 35: 'NNP', 36: 'NO_TAG', 37: 'NNP', 38: 'NNP', 39: 'JJ', 40: 'NN', 41: 'NN', 42: 'NO_TAG', 43: 'NNP', 44: 'NO_TAG', 45: 'CD', 46: 'NN', 47: 'NO_TAG', 48: 'NNP', 49: 'NO_TAG', 50: 'JJ', 51: 'NN', 52: 'NN', 53: 'CC', 54: 'JJ', 55: 'NN', 56: 'NN', 57: 'NO_TAG', 58: 'NNP', 59: 'NO_TAG', 60: 'JJ', 61: 'NN', 62: 'NO_TAG', 63: 'NNP', 64: 'NO_TAG', 65: 'JJ', 66: 'NN', 67: 'NO_TAG', 68: 'NNP', 69: 'NO_TAG', 70: 'NNP', 71: 'NUTRIENT', 72: 'NN', 73: 'NO_TAG', 74: 'NNP', 75: 'NO_TAG', 76: 'JJ', 77: 'NUTRIENT', 78: 'NN', 79: 'NO_TAG', 80: 'NNP', 81: 'NO_TAG', 82: 'CD', 83: 'JJ', 84: 'JJ', 85: 'NN', 86: 'NN', 87: 'NO_TAG', 88: 'NNP', 89: 'NNP', 90: 'NO_TAG', 91: 'NNP', 92: 'JJ', 93: 'NN', 94: 'NO_TAG', 95: 'NNP', 96: 'NO_TAG', 97: 'NNS', 98: 'NO_TAG', 99: 'NNP', 100: 'JJ', 101: 'NN', 102: 'NN', 103: 'NO_TAG', 104: 'NNS', 105: 'NO_TAG', 106: 'JJ', 107: 'NN', 108: 'NN', 109: 'NN', 110: 'NNS', 111: 'NO_TAG', 112: 'NN', 113: 'NO_TAG', 114: 'JJ', 115: 'JJ', 116: 'NN', 117: 'NNS', 118: 'NO_TAG', 119: 'NNS', 120: 'NO_TAG', 121: 'JJ', 122: 'JJ', 123: 'JJ', 124: 'NN', 125: 'NNS', 126: 'NO_TAG'}

        self.assertListEqual(edges_expected, edges)
        self.assertEqual(words_expected, words)
        self.assertEqual(tags_expected, tags)

    def test_merge_nodes_3(self):

        sentence_text = 'The study found that • children reported greater liking of the high-sugar cereals and consumed almost twice the amount per eating occasion compared with those served the low-sugar cereals (61.3 vs. 34.6 g); • children offered low-sugar cereals added more table sugar than those eating high-sugar cereals, and the total sugar content (from cereal and added sugar) was almost twice as high as with the high-sugar cereals (24.4 vs. 12.5 g; < 0.001); • there was no difference in the amount of milk consumed with the 2 types of cereals, nor the total energy consumed at the breakfast meal; and • children in the low-sugar group were more likely to put fresh fruit on their breakfast cereal compared with the high-sugar cereal condition (54% vs. 8%; = 0.05).'
        diseases = []
        nutrients = [('table sugar', 'Sucrose'), ('sugar', 'Sucrose'), ('sugar', 'Sucrose')]
        bacteria = []
        food = [('cereals', 'Breakfast Cereals'), ('cereals', 'Breakfast Cereals'), ('cereals', 'Breakfast Cereals'), ('cereals', 'Breakfast Cereals'), ('cereals', 'Breakfast Cereals'), ('milk', 'Dairy and Egg Products'), ('cereals', 'Breakfast Cereals')]

        parser_output = sentence_parser.parse_sentence(sentence_text)

        bacterial_names = [name for name, ncbi_id in bacteria]
        disease_names   = [name for name, doid_id in diseases]
        nutrient_names  = [name for name, idname in nutrients]
        food_names      = [name for name, food_group in food]

        merge_nodes(
            tokenizer=stanford_tokenizer,
            bacterial_names=bacterial_names,
            disease_names=disease_names,
            nutrient_names=nutrient_names,
            food_names=food_names,
            parser_output=parser_output
        )
        edges = parser_output.nx_graph.edges()
        words = parser_output.words
        tags = parser_output.tags

        edges_expected = [(1, 2), (2, 3), (4, 7), (5, 6), (6, 7), (7, 3), (8, 9), (9, 7), (10, 13), (11, 13), (12, 13), (13, 9), (14, 7), (15, 7), (16, 17), (17, 15), (18, 19), (19, 15), (20, 21), (21, 19), (22, 21), (23, 25), (24, 25), (25, 21), (26, 25), (27, 29), (28, 29), (29, 26), (31, 29), (32, 31), (33, 34), (34, 31), (37, 38), (38, 39), (39, 3), (40, 41), (41, 42), (42, 39), (43, 44), (44, 42), (46, 50), (47, 50), (48, 50), (49, 50), (50, 42), (52, 39), (53, 56), (54, 56), (55, 56), (56, 68), (58, 62), (59, 62), (60, 59), (61, 59), (62, 56), (64, 68), (65, 66), (66, 68), (67, 68), (68, 39), (69, 73), (70, 73), (71, 73), (72, 73), (73, 68), (75, 73), (76, 78), (77, 78), (78, 75), (80, 78), (81, 80), (84, 86), (85, 86), (86, 3), (87, 88), (88, 86), (89, 91), (90, 91), (91, 88), (92, 93), (93, 91), (94, 93), (95, 98), (96, 98), (97, 98), (98, 94), (99, 100), (100, 98), (102, 91), (103, 105), (104, 105), (105, 91), (106, 105), (107, 110), (108, 110), (109, 110), (110, 106), (112, 3), (113, 114), (114, 121), (115, 118), (116, 118), (117, 118), (118, 114), (119, 121), (120, 121), (121, 3), (122, 123), (123, 121), (124, 125), (125, 123), (126, 129), (127, 129), (128, 129), (129, 123), (130, 135), (131, 135), (132, 135), (133, 135), (134, 135), (135, 123), (137, 138), (138, 135), (139, 141), (140, 141), (141, 138), (143, 144), (144, 141)]
        words_expected = {1: 'The', 2: 'study', 3: 'found', 4: 'that', 5: '•', 6: 'children', 7: 'reported', 8: 'greater', 9: 'liking', 10: 'of', 11: 'the', 12: 'high-sugar', 13: 'cereals', 14: 'and', 15: 'consumed', 16: 'almost', 17: 'twice', 18: 'the', 19: 'amount', 20: 'per', 21: 'eating', 22: 'occasion', 23: 'compared', 24: 'with', 25: 'those', 26: 'served', 27: 'the', 28: 'low-sugar', 29: 'cereals', 30: '-LRB-', 31: '61.3', 32: 'vs.', 33: '34.6', 34: 'g', 35: '-RRB-', 36: ';', 37: '•', 38: 'children', 39: 'offered', 40: 'low-sugar', 41: 'cereals', 42: 'added', 43: 'more', 44: 'table sugar', 46: 'than', 47: 'those', 48: 'eating', 49: 'high-sugar', 50: 'cereals', 51: ',', 52: 'and', 53: 'the', 54: 'total', 55: 'sugar', 56: 'content', 57: '-LRB-', 58: 'from', 59: 'cereal', 60: 'and', 61: 'added', 62: 'sugar', 63: '-RRB-', 64: 'was', 65: 'almost', 66: 'twice', 67: 'as', 68: 'high', 69: 'as', 70: 'with', 71: 'the', 72: 'high-sugar', 73: 'cereals', 74: '-LRB-', 75: '24.4', 76: 'vs.', 77: '12.5', 78: 'g', 79: ';', 80: '<', 81: '0.001', 82: '-RRB-', 83: ';', 84: '•', 85: 'there', 86: 'was', 87: 'no', 88: 'difference', 89: 'in', 90: 'the', 91: 'amount', 92: 'of', 93: 'milk', 94: 'consumed', 95: 'with', 96: 'the', 97: '2', 98: 'types', 99: 'of', 100: 'cereals', 101: ',', 102: 'nor', 103: 'the', 104: 'total', 105: 'energy', 106: 'consumed', 107: 'at', 108: 'the', 109: 'breakfast', 110: 'meal', 111: ';', 112: 'and', 113: '•', 114: 'children', 115: 'in', 116: 'the', 117: 'low-sugar', 118: 'group', 119: 'were', 120: 'more', 121: 'likely', 122: 'to', 123: 'put', 124: 'fresh', 125: 'fruit', 126: 'on', 127: 'their', 128: 'breakfast', 129: 'cereal', 130: 'compared', 131: 'with', 132: 'the', 133: 'high-sugar', 134: 'cereal', 135: 'condition', 136: '-LRB-', 137: '54', 138: '%', 139: 'vs.', 140: '8', 141: '%', 142: ';', 143: '=', 144: '0.05', 145: '-RRB-', 146: '.'}
        tags_expected = {1: 'DT', 2: 'NN', 3: 'VBD', 4: 'IN', 5: 'JJ', 6: 'NNS', 7: 'VBD', 8: 'JJR', 9: 'NN', 10: 'IN', 11: 'DT', 12: 'JJ', 13: 'FOOD', 14: 'CC', 15: 'VBD', 16: 'RB', 17: 'RB', 18: 'DT', 19: 'NN', 20: 'IN', 21: 'VBG', 22: 'NN', 23: 'VBN', 24: 'IN', 25: 'DT', 26: 'VBN', 27: 'DT', 28: 'JJ', 29: 'FOOD', 30: 'NO_TAG', 31: 'CD', 32: 'CC', 33: 'CD', 34: 'NN', 35: 'NO_TAG', 36: 'NO_TAG', 37: 'JJ', 38: 'NNS', 39: 'VBD', 40: 'JJ', 41: 'FOOD', 42: 'VBD', 43: 'JJR', 44: 'NUTRIENT', 46: 'IN', 47: 'DT', 48: 'JJ', 49: 'JJ', 50: 'FOOD', 51: 'NO_TAG', 52: 'CC', 53: 'DT', 54: 'JJ', 55: 'NUTRIENT', 56: 'NN', 57: 'NO_TAG', 58: 'IN', 59: 'NN', 60: 'CC', 61: 'VBN', 62: 'NUTRIENT', 63: 'NO_TAG', 64: 'VBD', 65: 'RB', 66: 'RB', 67: 'RB', 68: 'JJ', 69: 'RB', 70: 'IN', 71: 'DT', 72: 'JJ', 73: 'FOOD', 74: 'NO_TAG', 75: 'CD', 76: 'IN', 77: 'CD', 78: 'NN', 79: 'NO_TAG', 80: 'NNP', 81: 'CD', 82: 'NO_TAG', 83: 'NO_TAG', 84: 'RB', 85: 'EX', 86: 'VBD', 87: 'DT', 88: 'NN', 89: 'IN', 90: 'DT', 91: 'NN', 92: 'IN', 93: 'FOOD', 94: 'VBN', 95: 'IN', 96: 'DT', 97: 'CD', 98: 'NNS', 99: 'IN', 100: 'FOOD', 101: 'NO_TAG', 102: 'CC', 103: 'DT', 104: 'JJ', 105: 'NN', 106: 'VBN', 107: 'IN', 108: 'DT', 109: 'NN', 110: 'NN', 111: 'NO_TAG', 112: 'CC', 113: 'JJ', 114: 'NNS', 115: 'IN', 116: 'DT', 117: 'JJ', 118: 'NN', 119: 'VBD', 120: 'RBR', 121: 'JJ', 122: 'TO', 123: 'VB', 124: 'JJ', 125: 'NN', 126: 'IN', 127: 'PRP$', 128: 'NN', 129: 'NN', 130: 'VBN', 131: 'IN', 132: 'DT', 133: 'JJ', 134: 'NN', 135: 'NN', 136: 'NO_TAG', 137: 'CD', 138: 'NN', 139: 'IN', 140: 'CD', 141: 'NN', 142: 'NO_TAG', 143: 'SYM', 144: 'CD', 145: 'NO_TAG', 146: 'NO_TAG'}

        self.assertListEqual(edges_expected, edges)
        self.assertEqual(words_expected, words)
        self.assertEqual(tags_expected, tags)

if __name__ == '__main__':
    unittest.main()
