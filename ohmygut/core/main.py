# -*- coding: utf-8 -*-
import datetime
import pickle

import pandas as pd

from ohmygut.core import constants
from ohmygut.core.analyzer import analyze_sentence
from ohmygut.core.constants import pattern_logger, large_pattern_logger
from ohmygut.core.sentence import Sentence
from ohmygut.core.tools import get_sentences, remove_entity_overlapping


def sentences_to_data_frame(sentences):
    data_list = map(lambda x: [x.text,
                               x.article_title,
                               x.journal,
                               str(x.bacteria),
                               str(x.nutrients),
                               str(x.diseases),
                               str(x.parser_output)
                               ], sentences)
    data = pd.DataFrame(list(data_list),
                        columns=['text', 'article_title', 'journal',
                                 'bacteria', 'nutrients', 'diseases', 'parser_output'])
    return data


def serialize_result(sentence, save_path):
    filename = (
        sentence.journal.split(' ')[0] + '_%s.pkl' % (datetime.datetime.now().strftime("%H_%M_%S-%d_%m_%y")))
    filename = save_path + '/' + filename
    with open(filename, 'wb') as f:
        pickle.dump(sentence, f)


def main(article_data_source, bacteria_catalog, nutrients_catalog, diseases_catalog, sentence_parser,
         save_path, tokenizer, pattern_finder):
    articles = article_data_source.get_articles()
    sentences_titles_journals_tuple = ((sentence, article.title, article.journal) for article in articles
                                       for sentence in get_sentences(article.text))
    sentences = []
    n = 0
    for sentence_text, article_title, article_journal in sentences_titles_journals_tuple:
        bacteria = bacteria_catalog.find(sentence_text)
        nutrients = nutrients_catalog.find(sentence_text)
        diseases = diseases_catalog.find(sentence_text)

        if sum(map(bool, [bacteria, nutrients, diseases])) < 2:
            continue

        bacteria, nutrients, diseases = remove_entity_overlapping(sentence_text, bacteria, nutrients, diseases,
                                                                  tokenizer)

        if sum(map(bool, [bacteria, nutrients, diseases])) < 2:
            continue

        parser_output = sentence_parser.parse_sentence(sentence_text)
        if not parser_output:
            continue

        sentence = Sentence(text=sentence_text,
                            article_title=article_title,
                            bacteria=bacteria,
                            nutrients=nutrients,
                            diseases=diseases,
                            parser_output=parser_output,
                            journal=article_journal)

        pathes = analyze_sentence(sentence, tokenizer, pattern_finder)

        if len(pathes) > 0:
            log_paths(sentence, pathes)

        constants.logger.info(sentence)
        n += 1
        constants.logger.info("sentence № %i" % n)
        sentences.append(sentence)
        constants.logger.info("=" * 80)

        serialize_result(sentence, save_path)

    constants.pattern_logger.info('total number sentences: %d' % n)
    constants.large_pattern_logger.info('total number sentences: %d' % n)
    data = sentences_to_data_frame(sentences)
    data.to_csv('sentences%s.csv' % (datetime.datetime.now().strftime("%H_%M_%S-%d_%m_%y")))


def log_paths(sentence, paths):
    pattern_logger.info(sentence.text)
    pattern_logger.info(sentence.bacteria)
    pattern_logger.info(sentence.nutrients)
    pattern_logger.info('')

    for path in paths:
        pattern_logger.info(path.words)
        pattern_logger.info(path.type)
        pattern_logger.info('')
    pattern_logger.info('=' * 100)
    pattern_logger.info('')

    large_pattern_logger.info(sentence.text)
    large_pattern_logger.info(sentence.bacteria)
    large_pattern_logger.info(sentence.nutrients)
    large_pattern_logger.info('')
    large_pattern_logger.info(sentence.parser_output.words)
    large_pattern_logger.info(sentence.parser_output.tags)
    large_pattern_logger.info(sentence.parser_output.nx_graph)
    large_pattern_logger.info([(i, j, sentence.parser_output.nx_graph[i][j]['rel']) for i, j in
                                         sentence.parser_output.nx_graph.edges()])
    large_pattern_logger.info('')

    for path in paths:
        large_pattern_logger.info(path.words)
        large_pattern_logger.info(path.edge_rels)
        large_pattern_logger.info(path.tags)
        large_pattern_logger.info(path.nodes_indexes)
        large_pattern_logger.info(path.type)
        large_pattern_logger.info('')

    large_pattern_logger.info('=' * 100)
    large_pattern_logger.info('')
