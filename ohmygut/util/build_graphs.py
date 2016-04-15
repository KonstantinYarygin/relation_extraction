# take sentences - one by line
# build graph
# save to data frame: sentence \t graph
# what is the format for a graph?
import ast
import os
import sys

import time

import pickle

import multiprocessing
import pandas as pd
from nltk import StanfordTokenizer
from nltk.parse.stanford import StanfordDependencyParser
import networkx as nx

from ohmygut.core.analyzer import analyze_sentence
from ohmygut.core.constants import logger
from ohmygut.core.sentence_processing import SentenceParser
from ohmygut.core.tools import check_if_more_than_one_list_not_empty
from ohmygut.paths import stanford_jar_path, stanford_models_jar_path, stanford_lex_parser_path


# a function to run parse/analyze in parallel
def parse_analyze(parser, stanford_tokenizer, text, names):
    start = time.time()
    # todo: make more obvious (use dict?)
    bacteria_names = names[0]
    nutrient_names = names[1]
    diseases_names = names[2]
    food_names = names[3]
    parser_output = parser.parse_sentence(text)
    analyze_output = analyze_sentence(bacterial_names=bacteria_names, nutrient_names=nutrient_names,
                                      disease_names=diseases_names, food_names=food_names,
                                      parser_output=parser_output, tokenizer=stanford_tokenizer,
                                      pattern_finder=None)
    end = time.time()
    logger.info("===\nparsed/analyzed: %s, \ntime: %f" % (text, end - start))
    return [parser_output, analyze_output]


if __name__ == '__main__':
    output_file = "build-graphs-output.csv"
    file = sys.argv[1]
    sentences_data = pd.read_csv(file, sep='\t')
    # ast.literal_eval(...) - to parse python lists
    # .tolist()[0] - to transform pandas Series to list of one str element and take this one element
    sentences_dictionary = {item: [ast.literal_eval(group["bacteria"].tolist()[0]),
                                   ast.literal_eval(group["nutrients"].tolist()[0]),
                                   ast.literal_eval(group["diseases"].tolist()[0]),
                                   ast.literal_eval(group["food"].tolist()[0])] for item, group in
                            sentences_data.groupby("text")}

    if not os.path.exists("out"):
        os.mkdir("out")

    stanford_tokenizer = StanfordTokenizer(path_to_jar=stanford_jar_path)
    stanford_dependency_parser = StanfordDependencyParser(path_to_jar=stanford_jar_path,
                                                          path_to_models_jar=stanford_models_jar_path,
                                                          model_path=stanford_lex_parser_path)

    parser = SentenceParser(stanford_dependency_parser, stanford_tokenizer)

    logger.info("start parse sentences")
    names_dictionary = {}
    logger.info("total number of sentences before filter: %i" % len(sentences_dictionary))
    # 1. prepare names
    for key, value in sentences_dictionary.items():
        # key is sentence text
        # value[0] is bacteria
        # value[1] is nutrient
        # value[2] is disease
        # value[3] is food
        # todo: make more obviuos (use a dict?)

        # filter:
        # 562 is E. coli
        # 1496 is Clostridium difficile
        # 590 is Salmonella
        # todo: make "black lists" of entities
        bacteria_names = [item[0] for item in value[0] if item[1] not in [562,
                                                                          1496,
                                                                          590]]  # item[0] is name, item[1] is code
        if len(bacteria_names) == 0:
            continue

        nutrient_names = [item[0] for item in value[1]]
        diseases_names = [item[0] for item in value[2]]
        food_names = [item[0] for item in value[3] if item[0] not in ["water", "Water"]]
        if not check_if_more_than_one_list_not_empty([bacteria_names, nutrient_names, diseases_names, food_names]):
            continue

        names_dictionary[key] = [bacteria_names, nutrient_names, diseases_names, food_names]
    logger.info("total number of sentences after filter: %i" % len(names_dictionary))

    # 2. parse/analyze paralleled
    start = time.time()
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
    logger.info("running parse/analyze with %i threads" % (multiprocessing.cpu_count() - 1))
    results = [pool.apply_async(parse_analyze, args=(parser,
                                                     stanford_tokenizer,
                                                     key,
                                                     value)) for key, value in names_dictionary.items()]
    parse_analyze_outputs = [p.get() for p in results]
    pool.close()
    end = time.time()
    logger.info("total parse/analyze time: %f" % (end - start))

    # 3. write the results
    i = 0
    sentence_number = len(names_dictionary)
    f = open(output_file, 'w')
    for parse_output, analyze_output in parse_analyze_outputs:
        paths_found = 0
        for output in analyze_output.items():
            shortest_paths = output[1]
            if len(shortest_paths) == 0:
                continue

            for path in shortest_paths:
                tags = path.tags
                words = path.words
                length = len(path.nodes_indexes)
                name_from = path.words[0]
                name_to = path.words[-1]
                tag_from = path.tags[0]
                tag_to = path.tags[-1]
                # writing results to csv
                row = "%s\t%i\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (parse_output.text,
                                                                        length,
                                                                        name_from, name_to,
                                                                        tag_from, tag_to,
                                                                        words, tags,
                                                                        parse_output.words, parse_output.tags,
                                                                        parse_output.nx_graph.adj)

                f.write(row)
                paths_found += 1
            # pickling results
            parser_output_filename = os.path.join("out", "parser-out-%i.pkl" % i)
            analyze_output_filename = os.path.join("out", "analyze-out-%i.pkl" % i)
            with open(parser_output_filename, 'wb') as fpkl:
                pickle.dump(parse_output, fpkl)
            with open(analyze_output_filename, 'wb') as fpkl:
                pickle.dump(analyze_output, fpkl)

        i += 1
        logger.info("===\nwriting sentence %i of %i, paths found: %i" % (i, sentence_number, paths_found))
        logger.info(parse_output.text)

    f.close()
