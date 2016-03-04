# -*- coding: utf-8 -*-
# import pandas as pd
import datetime
import pickle
from ohmygut.core import constants
from ohmygut.core.constants import PATH_FIELD_IND, PATH_FIELD_WORD, PATH_FIELD_REL, PATH_FIELD_TAG
from ohmygut.core.sentence import Sentence
from ohmygut.core.tools import get_sentences, remove_entity_overlapping


def save_parsing_result_xml(sentence, save_path):
    filename = (
    sentence.article_title.split(' ')[0] + '_%s.pickle' % (datetime.datetime.now().strftime("%H_%M_%S-%d_%m_%y")))
    filename = save_path + '/' + filename
    with open(filename, 'wb') as f:
        pickle.dump(sentence, f)


def main_get_patterns(article_data_source, bacteria_catalog, nutrients_catalog, sentence_parser,
                      sentence_analyzer, save_path):
    articles = article_data_source.get_articles()
    sentences_titles_journals_tuple = ((sentence, article.title, article.journal) for article in articles
                                       for sentence in get_sentences(article.text))
    n = 0
    for sentence_text, article_title, article_journal in sentences_titles_journals_tuple:
        bacteria = bacteria_catalog.find(sentence_text)
        nutrients = nutrients_catalog.find(sentence_text)
        diseases = []

        if sum(map(bool, [bacteria, nutrients, diseases])) < 2:
            continue

        bacteria, nutrients, diseases = remove_entity_overlapping(sentence_text, bacteria, nutrients, diseases,
                                                                  sentence_analyzer.get_tokenizer())

        if sum(map(bool, [bacteria, nutrients, diseases])) < 2:
            print('a test change')
            continue

        parser_output = sentence_parser.parse_sentence(sentence_text)
        if not parser_output:
            continue

        sentence = Sentence(text=sentence_text,
                            article_title=article_title,
                            bacteria=bacteria,
                            nutrients=nutrients,
                            diseases=diseases,
                            parse_result=parser_output,
                            journal=article_journal)

        pathes = sentence_analyzer.analyze(sentence)

        if len(pathes) > 0:
            log_paths(sentence, pathes)

        print(sentence)
        n += 1
        print("sentence № %i" % n)
        save_parsing_result_xml(sentence, save_path)


def log_paths(sentence, paths):
    constants.pattern_logger.info(sentence.text)
    constants.pattern_logger.info(sentence.bacteria)
    constants.pattern_logger.info(sentence.nutrients)
    constants.pattern_logger.info('')

    for path in paths:
        constants.pattern_logger.info(path[PATH_FIELD_WORD])
        constants.pattern_logger.info(path['type'])
        constants.pattern_logger.info('')
    constants.pattern_logger.info('=' * 100)
    constants.pattern_logger.info('')

    constants.large_pattern_logger.info(sentence.text)
    constants.large_pattern_logger.info(sentence.bacteria)
    constants.large_pattern_logger.info(sentence.nutrients)
    constants.large_pattern_logger.info('')
    constants.large_pattern_logger.info(sentence.parse_result.words)
    constants.large_pattern_logger.info(sentence.parse_result.tags)
    constants.large_pattern_logger.info(sentence.parse_result.nx_graph)
    constants.large_pattern_logger.info([(i, j, sentence.parse_result.nx_graph[i][j]['rel']) for i, j in
                                         sentence.parse_result.nx_graph.edges()])
    constants.large_pattern_logger.info('')

    for path in paths:
        constants.large_pattern_logger.info(path[PATH_FIELD_WORD])
        constants.large_pattern_logger.info(path[PATH_FIELD_REL])
        constants.large_pattern_logger.info(path[PATH_FIELD_TAG])
        constants.large_pattern_logger.info(path[PATH_FIELD_IND])
        constants.large_pattern_logger.info(path['type'])
        constants.large_pattern_logger.info('')

    constants.large_pattern_logger.info('=' * 100)
    constants.large_pattern_logger.info('')
