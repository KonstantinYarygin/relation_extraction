# -*- coding: utf-8 -*-
from traceback import format_exc

from ohmygut.core import constants
from ohmygut.core.tools import get_sentences, memory_usage_psutil


def main(article_data_sources, writers, sentence_finder, data_sources_to_skip=0, sentences_to_skip=0):
    data_source_names = list(map(lambda x: str(x), article_data_sources))
    constants.logger.info("data sources: %s" % data_source_names)
    total_sentence_number = 0
    for i in range(data_sources_to_skip, len(article_data_sources)):
        article_data_source = article_data_sources[i]

        articles = article_data_source.get_articles()
        # todo: sort to be able to continue
        sentences_titles_journals_tuple = ((sentence, article.title, article.journal) for article in articles
                                           for sentence in get_sentences(article.text))

        constants.logger.info("start looping sentences with data source №%i %s" % (i + 1, str(article_data_source)))
        sentence_number = sentences_to_skip
        for _ in range(sentences_to_skip):
            next(sentences_titles_journals_tuple)
        sentences_to_skip = 0

        for sentence_text, article_title, article_journal in sentences_titles_journals_tuple:
            try:
                sentence = sentence_finder.get_sentence(sentence_text, article_title, article_journal)
            except Exception:
                constants.logger.info(format_exc())
                constants.logger.info("sentence with error: %s" % sentence_text)
                constants.logger.info("got error in sentence loop; continue")
                continue
            if not sentence:
                continue

            for writer in writers:
                writer.write(sentence)

            sentence_number += 1
            constants.logger.info("memory usage: %f" % memory_usage_psutil())
            constants.logger.info("sentence № %i, data source № %i\n%s" % (sentence_number, i, sentence))
            constants.logger.info("=" * 80)
            constants.logger.info("=" * 80)

        total_sentence_number += sentence_number
        constants.logger.info("finish looping sentences with %s\n" % str(article_data_source))
    constants.pattern_logger.info('total number sentences: %i' % total_sentence_number)
