# take sentences - one by line
# build graph
# save to data frame: sentence \t graph
# what is the format for a graph?
import sys

import time
from nltk import StanfordTokenizer
from nltk.parse.stanford import StanfordDependencyParser
import networkx as nx

from ohmygut.core.analyzer import analyze_sentence
from ohmygut.core.sentence_processing import SentenceParser
from ohmygut.paths import stanford_jar_path, stanford_models_jar_path, stanford_lex_parser_path


if __name__ == '__main__':
    output_file = "build-graphs-output.csv"
    file = sys.argv[1]
    with open(file) as g:
        sentences = g.readlines()

    stanford_tokenizer = StanfordTokenizer(path_to_jar=stanford_jar_path)

    stanford_dependency_parser = StanfordDependencyParser(path_to_jar=stanford_jar_path,
                                                          path_to_models_jar=stanford_models_jar_path,
                                                          model_path=stanford_lex_parser_path)

    parser = SentenceParser(stanford_dependency_parser, stanford_tokenizer)
    f = open(output_file, 'w')
    print("start parse sentences")
    i = 0
    sentence_number = len(sentences)
    # TODO: make try/except
    # TODO: make universal: analyze not only BACT-DISEASE
    for sentence in sentences:
        start = time.time()
        i += 1
        text, bacteria, disease = sentence.split('\t')
        bacteria_list = bacteria.replace('\n', '').split(';')
        disease_list = disease.replace('\n', '').split(';')
        parser_output = parser.parse_sentence(text)
        analyze_output = analyze_sentence(bacterial_names=bacteria_list, nutrient_names=[],
                                          disease_names=disease_list, food_names=[],
                                          parser_output=parser_output, tokenizer=stanford_tokenizer,
                                          pattern_finder=None)
        shortest_path = analyze_output['BACTERIUM-DISEASE'][0]
        tags = shortest_path.tags
        words = shortest_path.words
        length = len(shortest_path.nodes_indexes)
        row = "%s\t%i\t%s\t%s\t%s\t%s\n" % (text, length, bacteria_list, disease_list, words, tags)
        f.write(row)
        end = time.time()
        print("\nsentence %i of %i, time %f" % (i, sentence_number, end-start))
        print(text)

    f.close()
