# -*- coding: utf-8 -*-
import os

from ohmygut.core import constants
from ohmygut.core.analyzer import analyze_sentence
from ohmygut.core.constants import pattern_logger, large_pattern_logger
from ohmygut.core.sentence import Sentence
from ohmygut.core.tools import get_sentences, remove_entity_overlapping, sentences_to_data_frame, serialize_result, \
    check_if_more_than_one_list_not_empty, get_output_dir_path


def main(article_data_sources,
         bacteria_catalog, nutrients_catalog, diseases_catalog,
         sentence_parser, tokenizer, pattern_finder,
         data_sources_to_skip=0, sentences_to_skip=0):

    output_dir = get_output_dir_path()

    sentences = []
    data_source_names = list(map(lambda x: str(x), article_data_sources))
    constants.logger.info("data sources: %s" % data_source_names)
    for i in range(data_sources_to_skip, len(article_data_sources)):
        article_data_source = article_data_sources[i]

        articles = article_data_source.get_articles()
        sentences_titles_journals_tuple = ((sentence, article.title, article.journal) for article in articles
                                           for sentence in get_sentences(article.text))

        constants.logger.info("start looping sentences with data source №%i %s" % (i+1, str(article_data_source)))
        sentence_number = sentences_to_skip
        for _ in range(sentences_to_skip):
            next(sentences_titles_journals_tuple)

        for sentence_text, article_title, article_journal in sentences_titles_journals_tuple:
            sentence_number += 1

            bacteria = bacteria_catalog.find(sentence_text)
            nutrients = nutrients_catalog.find(sentence_text)
            diseases = diseases_catalog.find(sentence_text)

            if not check_if_more_than_one_list_not_empty([bacteria, nutrients, diseases]):
                continue

            bacteria, nutrients, diseases = remove_entity_overlapping(sentence_text,
                                                                      bacteria, nutrients, diseases,
                                                                      tokenizer)

            if not check_if_more_than_one_list_not_empty([bacteria, nutrients, diseases]):
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

            constants.logger.info("sentence № %i\n%s" % (sentence_number, sentence))
            constants.logger.info("=" * 80)

            sentences.append(sentence)
            serialize_result(sentence, output_dir, sentence_number)
        constants.logger.info("finish looping sentences with %s\n" % str(article_data_source))

    constants.pattern_logger.info('total number sentences: %d' % len(sentences))
    data = sentences_to_data_frame(sentences)
    data.to_csv(os.path.join(output_dir, 'sentences.csv'), index=False)


def log_paths(sentence, paths):
    # todo: почему не объединять вывод? например:
    # pattern_logger.info('%s \n %s \n %s \n' % (sentence.text, sentence.bacteria, sentence.nutrients))

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


