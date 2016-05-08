import unittest

from ohmygut.core.analyzer import SentenceAnalyzer
from ohmygut.core.catalog.all_bacteria_catalog import ALL_BACTERIA_TAG
from ohmygut.core.catalog.catalog import Catalog, EntityCollection, Entity
from ohmygut.core.catalog.diseases_catalog import DISEASE_TAG
from ohmygut.core.catalog.gut_bacteria_catalog import BACTERIA_TAG
from ohmygut.core.catalog.nutrients_catalog import NUTRIENT_TAG
from ohmygut.core.catalog.usda_food_catalog import FOOD_TAG
from ohmygut.core.sentence_finder import SentenceFinder
from ohmygut.core.sentence_processing import SentenceParser, SpacySentenceParser


class MockSentenceParser(SentenceParser):
    def parse_sentence(self, sentence, entities, tokens):
        pass


class MockCatalog(Catalog):
    def __init__(self, name, entities_number):
        super().__init__()
        self.entities_number = entities_number
        self.name = name

    def initialize(self):
        pass

    def find(self, sentence_text):
        entities = []
        for i in range(self.entities_number):
            entities.append(Entity("name%i%i" % (i, self.name), "code%i%i" % (i, self.name), "tag%i" % self.name))
        return EntityCollection(entities,
                                "tag%i" % self.name)

    def get_list(self):
        pass


class TestCase(unittest.TestCase):
    def test_if_tags(self):
        target = SentenceFinder(catalog_list=None, sentence_parser=None, sentence_analyzer=None,
                                tags_to_search=[BACTERIA_TAG],
                                tags_optional_to_search=[FOOD_TAG, DISEASE_TAG, NUTRIENT_TAG])
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, FOOD_TAG]))
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, DISEASE_TAG]))
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, NUTRIENT_TAG]))
        self.assertFalse(target.check_if_tags([BACTERIA_TAG, ALL_BACTERIA_TAG]))
        self.assertFalse(target.check_if_tags([BACTERIA_TAG]))

        target = SentenceFinder(catalog_list=[], sentence_parser=None, sentence_analyzer=None,
                                tags_to_search=[BACTERIA_TAG], tags_optional_to_search=[])
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, FOOD_TAG]))
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, DISEASE_TAG]))
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, NUTRIENT_TAG]))
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, ALL_BACTERIA_TAG]))
        self.assertTrue(target.check_if_tags([BACTERIA_TAG]))
        self.assertFalse(target.check_if_tags([FOOD_TAG, DISEASE_TAG]))

    def test_get_sentence(self):
        catalog1 = MockCatalog(1, 2)
        catalog2 = MockCatalog(2, 1)
        analyzer = SentenceAnalyzer()
        target = SentenceFinder(catalog_list=[catalog1, catalog2],
                                sentence_parser=SpacySentenceParser(),
                                sentence_analyzer=analyzer, tags_to_search=["tag1"],
                                tags_optional_to_search=["tag2"])
        text = "The name01 is the same as name11, but not name02"
        title = "title"
        journal = "journal"
        actual = target.get_sentence(text, title, journal)
        actual_collections = actual.entities_collections
        expected_collections = [EntityCollection([Entity("name01", "code01", "tag1"),
                                                  Entity("name11", "code11", "tag1")], "tag1"),
                                EntityCollection([Entity("name02", "code02", "tag2")], "tag2")]
        self.assertCountEqual(actual_collections, expected_collections)


if __name__ == '__main__':
    unittest.main()
