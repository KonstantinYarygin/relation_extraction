# -*- coding: utf-8 -*-

from ohmygut.core import constants
from ohmygut.core.analyzer import analyze_sentence
from ohmygut.core.constants import SENTENCE_LENGTH_THRESHOLD
from ohmygut.core.sentence import Sentence
from ohmygut.core.tools import get_sentences, remove_entity_overlapping, check_if_more_than_one_list_not_empty


def main(article_data_sources,
         bacteria_catalog, nutrients_catalog, diseases_catalog, food_catalog,
         sentence_parser, tokenizer, pattern_finder, writers,
         data_sources_to_skip=0, sentences_to_skip=0, do_parse=True, do_analyze=True):
    sentences = []
    data_source_names = list(map(lambda x: str(x), article_data_sources))
    constants.logger.info("data sources: %s" % data_source_names)
    for i in range(data_sources_to_skip, len(article_data_sources)):
        article_data_source = article_data_sources[i]

        articles = article_data_source.get_articles()
        sentences_titles_journals_tuple = ((sentence, article.title, article.journal) for article in articles
                                           for sentence in get_sentences(article.text))

        constants.logger.info("start looping sentences with data source №%i %s" % (i + 1, str(article_data_source)))
        sentence_number = sentences_to_skip
        for _ in range(sentences_to_skip):
            next(sentences_titles_journals_tuple)

        for sentence_text, article_title, article_journal in sentences_titles_journals_tuple:

            try:
                sentence = find_sentence(sentence_text, article_title, article_journal,
                                         bacteria_catalog, nutrients_catalog, diseases_catalog, food_catalog,
                                         tokenizer, sentence_parser, pattern_finder, do_parse, do_analyze)
            except Exception as error:
                constants.logger.info(error)
                constants.logger.info("got error in sentence loop; continue")
                continue
            if not sentence:
                continue

            for writer in writers:
                writer.write(sentence)

            sentence_number += 1
            constants.logger.info("sentence № %i\n%s" % (sentence_number, sentence))
            constants.logger.info("=" * 80)
            sentences.append(sentence)


        constants.logger.info("finish looping sentences with %s\n" % str(article_data_source))
    constants.pattern_logger.info('total number sentences: %d' % len(sentences))


# todo: test me
def find_sentence(sentence_text, article_title, article_journal,
                  bacteria_catalog, nutrients_catalog, diseases_catalog, food_catalog,
                  tokenizer, sentence_parser, pattern_finder, do_parse=True, do_analyze=True):

    if len(sentence_text) > SENTENCE_LENGTH_THRESHOLD:
        return None

    # todo: test me
    bacteria = bacteria_catalog.find(sentence_text)
    nutrients = nutrients_catalog.find(sentence_text)
    diseases = diseases_catalog.find(sentence_text)
    food = food_catalog.find(sentence_text)

    # todo: test me
    if not (check_if_more_than_one_list_not_empty([bacteria, nutrients]) or
            check_if_more_than_one_list_not_empty([bacteria, diseases]) or
            check_if_more_than_one_list_not_empty([bacteria, food])):
        return None

    bacteria, nutrients, diseases, food = remove_entity_overlapping(sentence_text,
                                                              bacteria, nutrients, diseases, food,
                                                              tokenizer)

    if not (check_if_more_than_one_list_not_empty([bacteria, nutrients]) or
            check_if_more_than_one_list_not_empty([bacteria, diseases]) or
            check_if_more_than_one_list_not_empty([bacteria, food])):
        return None

    if do_parse:
        # todo: no need to be object?
        parser_output = sentence_parser.parse_sentence(sentence_text)
        if not parser_output:
            return None
    else:
        parser_output = ''

    if do_parse and do_analyze:
        paths = analyze_sentence(bacteria, nutrients, diseases, food,
                                 parser_output, tokenizer, pattern_finder)
    else:
        paths = ''

    sentence = Sentence(text=sentence_text,
                        article_title=article_title,
                        bacteria=bacteria,
                        nutrients=nutrients,
                        diseases=diseases,
                        food=food,
                        parser_output=parser_output,
                        journal=article_journal,
                        shortest_paths=paths)

    return sentence
