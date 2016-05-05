import unittest

from ohmygut.core.catalog.all_bacteria_catalog import ALL_BACTERIA_TAG
from ohmygut.core.catalog.diseases_catalog import DISEASE_TAG
from ohmygut.core.catalog.gut_bacteria_catalog import BACTERIA_TAG
from ohmygut.core.catalog.nutrients_catalog import NUTRIENT_TAG
from ohmygut.core.catalog.usda_food_catalog import FOOD_TAG
from ohmygut.core.main import SentenceFinder


class TestCase(unittest.TestCase):
    def test_if_tags(self):
        target = SentenceFinder(tokenizer=None, sentence_parser=None, sentence_analyzer=None, all_bacteria_catalog=None,
                                tags_to_search=[BACTERIA_TAG],
                                tags_optional_to_search=[FOOD_TAG, DISEASE_TAG, NUTRIENT_TAG])
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, FOOD_TAG]))
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, DISEASE_TAG]))
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, NUTRIENT_TAG]))
        self.assertFalse(target.check_if_tags([BACTERIA_TAG, ALL_BACTERIA_TAG]))
        self.assertFalse(target.check_if_tags([BACTERIA_TAG]))

        target = SentenceFinder(tokenizer=None, sentence_parser=None, sentence_analyzer=None, all_bacteria_catalog=None,
                                tags_to_search=[BACTERIA_TAG],
                                tags_optional_to_search=[])
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, FOOD_TAG]))
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, DISEASE_TAG]))
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, NUTRIENT_TAG]))
        self.assertTrue(target.check_if_tags([BACTERIA_TAG, ALL_BACTERIA_TAG]))
        self.assertTrue(target.check_if_tags([BACTERIA_TAG]))
        self.assertFalse(target.check_if_tags([FOOD_TAG, DISEASE_TAG]))


if __name__ == '__main__':
    unittest.main()
