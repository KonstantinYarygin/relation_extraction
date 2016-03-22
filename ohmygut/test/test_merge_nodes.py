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
        parser_output = ParserOutput(nx_graph, words, tags)

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

        sentence_text = 'Intervention trials of breakfast cereals and diabetes CHO, carbohydrate; FRS, fast release starch; GER, gastric emptying rate; GI, glycemic index; GTT, glucose tolerance test; Hb A, glycated hemoglobin; IDDM, insulin dependent diabetes mellitus; NIDDM, non–insulin-dependent diabetes mellitus; RTEC, ready-to-eat breakfast cereal; SRS, slow release starch.'
        diseases = [('diabetes mellitus', 'DOID:9351'), ('diabetes mellitus', 'DOID:9351')]
        nutrients = [('starch', 'Starch'), ('glucose', 'Glucose')]
        bacteria = []
        food = []

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

if __name__ == '__main__':
    unittest.main()
