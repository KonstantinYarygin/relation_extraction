# -*- coding: utf-8 -*-
import sys
from traceback import format_exc

from ohmygut.core import constants
from ohmygut.core.catalog.all_bacteria_catalog import ALL_BACTERIA_TAG
from ohmygut.core.catalog.catalog import EntityCollection
from ohmygut.core.catalog.diseases_catalog import DISEASE_TAG
from ohmygut.core.catalog.gut_bacteria_catalog import BACTERIA_TAG
from ohmygut.core.catalog.nutrients_catalog import NUTRIENT_TAG
from ohmygut.core.catalog.usda_food_catalog import FOOD_TAG
from ohmygut.core.constants import SENTENCE_LENGTH_THRESHOLD
from ohmygut.core.sentence import Sentence
from ohmygut.core.tools import get_sentences, remove_entity_overlapping, check_if_more_than_one_list_not_empty


def main(article_data_sources, gut_bacteria_catalog, nutrients_catalog, diseases_catalog, food_catalog, writers,
         sentence_finder, data_sources_to_skip=0, sentences_to_skip=0):
    sentences = []
    data_source_names = list(map(lambda x: str(x), article_data_sources))
    constants.logger.info("data sources: %s" % data_source_names)
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
                sentence = sentence_finder.get_sentence(sentence_text, article_title, article_journal,
                                                        gut_bacteria_catalog,
                                                        nutrients_catalog, diseases_catalog, food_catalog)
            except Exception:
                constants.logger.info(format_exc())
                constants.logger.info("got error in sentence loop; continue")
                continue
            if not sentence:
                continue

            for writer in writers:
                writer.write(sentence)

            sentence_number += 1
            constants.logger.info("sentence № %i, data source № %i\n%s" % (sentence_number, i, sentence))
            constants.logger.info("=" * 80)
            sentences.append(sentence)

        constants.logger.info("finish looping sentences with %s\n" % str(article_data_source))
    constants.pattern_logger.info('total number sentences: %d' % len(sentences))


class SentenceFinder(object):
    def __init__(self, tokenizer, sentence_parser, sentence_analyzer, all_bacteria_catalog):
        super().__init__()
        self.sentence_analyzer = sentence_analyzer
        self.all_bacteria_catalog = all_bacteria_catalog
        self.sentence_parser = sentence_parser
        self.tokenizer = tokenizer

    # todo: test me
    def get_sentence(self, sentence_text, article_title, article_journal,
                     bacteria_catalog, nutrients_catalog, diseases_catalog, food_catalog):

        if len(sentence_text) > SENTENCE_LENGTH_THRESHOLD:
            return None

        # todo: test me
        bacteria = bacteria_catalog.find(sentence_text)
        nutrients = nutrients_catalog.find(sentence_text)
        diseases = diseases_catalog.find(sentence_text)
        food = food_catalog.find(sentence_text)

        # if len(bacteria.entities) == 0:
        #     return None
        # todo: test me
        if not (check_if_more_than_one_list_not_empty([bacteria.entities, nutrients.entities]) or
                    check_if_more_than_one_list_not_empty([bacteria.entities, diseases.entities]) or
                    check_if_more_than_one_list_not_empty([bacteria.entities, food.entities])):
            return None

        all_bacteria = self.all_bacteria_catalog.find(sentence_text)
        bacteria.entities = bacteria.entities + all_bacteria.entities
        entity_collections = remove_entity_overlapping(sentence_text,
                                                       [bacteria, nutrients, diseases, food],
                                                       self.tokenizer)

        # ======= todo: refactor
        # put entity collections to dict by tag
        collections_by_tag = {collection.tag: collection for collection in entity_collections}
        bacteria = collections_by_tag[BACTERIA_TAG]
        nutrients = collections_by_tag[NUTRIENT_TAG]
        diseases = collections_by_tag[DISEASE_TAG]
        food = collections_by_tag[FOOD_TAG]

        # separate all several-words-names by underscope (_)
        for entity in bacteria.entities + nutrients.entities + diseases.entities + food.entities:
            dashed_name = entity.name.replace(' ', '_')
            sentence_text = sentence_text.replace(entity.name, dashed_name)
            entity.name = dashed_name

        # clean bacterias: ALL_BACTERIA_TAG means it's not in gut catalog
        good_bacteria = [x for x in bacteria.entities if ALL_BACTERIA_TAG not in x.additional_tags]
        bacteria = EntityCollection(good_bacteria, BACTERIA_TAG)

        # ======= refactor

        # if len(bacteria.entities) == 0:
        #     return None
        if not (check_if_more_than_one_list_not_empty([bacteria.entities, nutrients.entities]) or
                    check_if_more_than_one_list_not_empty([bacteria.entities, diseases.entities]) or
                    check_if_more_than_one_list_not_empty([bacteria.entities, food.entities])):
            return None

        parser_output = self.sentence_parser.parse_sentence(sentence_text, bacteria.entities +
                                                            nutrients.entities +
                                                            diseases.entities +
                                                            food.entities)

        paths = self.sentence_analyzer.analyze_sentence(parser_output)

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
