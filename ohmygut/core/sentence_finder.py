import spacy

from ohmygut.core.catalog.all_bacteria_catalog import ALL_BACTERIA_TAG, ALL_BACTERIA_COLLECTION
from ohmygut.core.catalog.catalog import EntityCollection
from ohmygut.core.catalog.gut_bacteria_catalog import BACTERIA_TAG, BACTERIA_COLLECTION
from ohmygut.core.constants import SENTENCE_LENGTH_THRESHOLD
from ohmygut.core.sentence import Sentence
from ohmygut.core.tools import remove_entity_overlapping


class SentenceFinder(object):
    def __init__(self, tokenizer, sentence_parser, sentence_analyzer,
                 tags_to_search, tags_optional_to_search, catalog_list):
        super().__init__()
        self.catalog_list = catalog_list
        self.tags_optional = set(tags_optional_to_search)
        self.tags = set(tags_to_search)
        self.sentence_analyzer = sentence_analyzer
        self.sentence_parser = sentence_parser
        self.tokenizer = tokenizer
        self.nlp = spacy.load('en')

    # todo: test me
    def get_sentence(self, sentence_text, article_title, article_journal):

        if len(sentence_text) > SENTENCE_LENGTH_THRESHOLD:
            return None

        entities_collections = []
        for catalog in self.catalog_list:
            found_entities = catalog.find(sentence_text)
            entities_collections.append(found_entities)

        tags_in_sentence = set([collection.tag for collection in entities_collections if len(collection.entities) > 0])

        if not self.check_if_tags(tags_in_sentence):
            return None

        tokens = self.nlp(sentence_text)
        tokens_words = [token.orth_ for token in tokens]
        collections_by_name = {collection.unique_name: collection for collection in entities_collections}

        # ======= todo: refactor
        # todo: make tag unique!
        # todo: make it as a separate step - like preprocessing
        if BACTERIA_COLLECTION in collections_by_name and ALL_BACTERIA_COLLECTION in collections_by_name:
            bacteria = collections_by_name[BACTERIA_COLLECTION]
            bacteria_names = set([entity.name for entity in bacteria.entities])
            all_bacteria = collections_by_name[ALL_BACTERIA_COLLECTION]
            all_bacteria.entities = [entity for entity in all_bacteria.entities if entity.name not in bacteria_names]
            bacteria.entities.extend(all_bacteria.entities)

            # remove ALL_BACTERIA entities: we dont need it
            del collections_by_name[ALL_BACTERIA_COLLECTION]
            entities_collections = [collection for collection in entities_collections if collection.unique_name != ALL_BACTERIA_COLLECTION]

        entities_collections = remove_entity_overlapping(entities_collections, tokens_words)
        # todo: a problem with name and tag!
        collections_by_tag = {collection.tag: collection for collection in entities_collections}
        entities_lists = [collection.entities for collection in entities_collections]
        all_entities_list = []
        for entity_list in entities_lists:
            all_entities_list = all_entities_list + entity_list

        # separate all several-words-names by underscope (_)
        for entity in all_entities_list:
            dashed_name = entity.name.replace(' ', '_')
            sentence_text = sentence_text.replace(entity.name, dashed_name)
            entity.name = dashed_name

        if BACTERIA_TAG in collections_by_tag:
            # clean bacterias: ALL_BACTERIA_TAG means it's not in gut catalog
            bacteria = collections_by_tag[BACTERIA_TAG]
            bad_bacteria = [x for x in bacteria.entities if ALL_BACTERIA_TAG in x.additional_tags]
            for bad_bact in bad_bacteria:
                bacteria.entities.remove(bad_bact)
            # clean_bacteria = EntityCollection(good_bacteria, BACTERIA_TAG)
            # collections_by_tag[BACTERIA_TAG] = clean_bacteria

        tags_in_sentence = set([collection.tag for collection in entities_collections if len(collection.entities) > 0])
        # ======= end refactor

        if not self.check_if_tags(tags_in_sentence):
            return None

        parser_output = self.sentence_parser.parse_sentence(sentence_text, all_entities_list, tokens)

        paths = self.sentence_analyzer.analyze_sentence(parser_output)

        sentence = Sentence(text=sentence_text,
                            article_title=article_title,
                            entities_collections=entities_collections,
                            parser_output=parser_output,
                            journal=article_journal,
                            shortest_paths=paths)

        return sentence

    def check_if_tags(self, tags_in_sentence):
        if not self.tags.issubset(tags_in_sentence):
            return False
        if len(self.tags_optional) != 0 and not any(tag_optional in tags_in_sentence for tag_optional in self.tags_optional):
            return False
        return True
