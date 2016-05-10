import os
import unittest

from ohmygut.core.catalog.all_bacteria_catalog import ALL_BACTERIA_TAG
from ohmygut.core.catalog.catalog import Entity, EntityCollection
from ohmygut.core.catalog.diseases_catalog import DISEASE_TAG
from ohmygut.core.catalog.gut_bacteria_catalog import BACTERIA_TAG
from ohmygut.core.catalog.nutrients_catalog import NUTRIENT_TAG
from ohmygut.core.sentence import Sentence
from ohmygut.core.tools import get_sentences, remove_entity_overlapping, remove_pmc_from_pmcid

script_dir = os.path.dirname(os.path.realpath(__file__))


class TestCase(unittest.TestCase):
    def test_get_sentences(self):
        test_text = "First sentence. Second sentence. Sentence with 2.0 number. Sentence with H. pylori. Good bye."
        expected = ["First sentence.", "Second sentence.", "Sentence with 2.0 number.", "Sentence with H. pylori.",
                    "Good bye."]
        actual = get_sentences(test_text)
        self.assertListEqual(expected, actual)

    def test_remove_entity_overlapping_empty(self):
        output = remove_entity_overlapping([EntityCollection([]), EntityCollection([])],
                                           tokens_words=['There', 'is', 'really', 'nothing'])

        expected = [EntityCollection([]), EntityCollection([])]

        self.assertCountEqual(expected[0].entities, output[0].entities)
        self.assertCountEqual(expected[1].entities, output[1].entities)

    def test_remove_entity_overlapping_2(self):
        bacteria = EntityCollection([Entity('M. tuberculosis', '111', BACTERIA_TAG),
                                     Entity('M. tuberculosis', '111', BACTERIA_TAG)], tag=BACTERIA_TAG)
        nutrients = EntityCollection([Entity('propionic', '123', NUTRIENT_TAG)], NUTRIENT_TAG)
        diseases = EntityCollection([Entity('tuberculosis', 'a', DISEASE_TAG),
                                     Entity('tuberculosis', 'a', DISEASE_TAG),
                                     Entity('tuberculosis', 'a', DISEASE_TAG),
                                     Entity('chronic obstructive syndrome', 'a1', DISEASE_TAG),
                                     Entity('obstructive syndrome', 'b1', DISEASE_TAG)], DISEASE_TAG)

        output = remove_entity_overlapping([bacteria, nutrients, diseases],
                                           tokens_words=['M.', 'tuberculosis', 'is', 'the', 'cause', 'of',
                                                         'tuberculosis', 'and', 'chronic',
                                                         'obstructive',
                                                         'syndrome', ',', 'also', 'M.', 'tuberculosis', 'is', 'a',
                                                         'propionic', 'acid', 'producer',
                                                         '.'])

        expected = [EntityCollection([bacteria.entities[0], bacteria.entities[1]], BACTERIA_TAG),
                    EntityCollection([diseases.entities[1], diseases.entities[3]], DISEASE_TAG),
                    EntityCollection([nutrients.entities[0]], NUTRIENT_TAG)]

        self.assertCountEqual(expected[0].entities, output[0].entities)
        self.assertCountEqual(expected[1].entities, output[1].entities)
        self.assertCountEqual(expected[2].entities, output[2].entities)

    def test_remove_entity_overlapping_3(self):
        bacteria = EntityCollection([Entity('M. tuberculosis', '111', BACTERIA_TAG),
                                     Entity('M. tuberculosis', '111', BACTERIA_TAG, [ALL_BACTERIA_TAG])], tag=BACTERIA_TAG)
        nutrients = EntityCollection([Entity('propionic', '123', NUTRIENT_TAG)], NUTRIENT_TAG)

        output = remove_entity_overlapping([bacteria, nutrients],
                                           tokens_words=['M.', 'tuberculosis', 'is', 'the', 'cause', 'of',
                                                         'tuberculosis', 'and', 'chronic',
                                                         'obstructive',
                                                         'syndrome', ',', 'also', 'is', 'a',
                                                         'propionic', 'acid', 'producer',
                                                         '.'])

        expected = [EntityCollection([bacteria.entities[0]], BACTERIA_TAG),
                    EntityCollection([nutrients.entities[0]], NUTRIENT_TAG)]

        self.assertCountEqual(expected[0].entities, output[0].entities)
        self.assertCountEqual(expected[1].entities, output[1].entities)

    def test_remove_entity_overlapping_4(self):
        bacteria = EntityCollection([Entity('tuberculosis', '111', BACTERIA_TAG),
                                     Entity('M. tuberculosis', '111', BACTERIA_TAG, [ALL_BACTERIA_TAG])], tag=BACTERIA_TAG)
        nutrients = EntityCollection([Entity('propionic', '123', NUTRIENT_TAG)], NUTRIENT_TAG)

        output = remove_entity_overlapping([bacteria, nutrients],
                                           tokens_words=['M.', 'tuberculosis', 'is', 'the', 'cause', 'of',
                                                         'tuberculosis', 'and', 'chronic',
                                                         'obstructive',
                                                         'syndrome', ',', 'also', 'is', 'a',
                                                         'propionic', 'acid', 'producer',
                                                         '.'])

        expected = [EntityCollection([bacteria.entities[1]], BACTERIA_TAG),
                    EntityCollection([nutrients.entities[0]], NUTRIENT_TAG)]

        self.assertCountEqual(expected[0].entities, output[0].entities)
        self.assertCountEqual(expected[1].entities, output[1].entities)
    # def test_remove_entity_overlapping_3(self):
    #     diseases = [('diabetes mellitus', 'DOID:9351'), ('diabetes mellitus', 'DOID:9351')]
    #     nutrients = [('starch', 'Starch'), ('glucose', 'Glucose')]
    #     bacteria = []
    #     food = []
    #
    #     bacteria_new, nutrients_new, diseases_new, food_new = remove_entity_overlapping(
    #         [bacteria, nutrients, diseases, food],
    #         tokens_words=['Intervention', 'trials', 'of', 'breakfast', 'cereals', 'and', 'diabetes', 'CHO', ',',
    #                       'carbohydrate', ';', 'FRS', ',', 'fast', 'release', 'starch', ';', 'GER', ',', 'gastric',
    #                       'emptying', 'rate', ';', 'GI', ',', 'glycemic', 'index', ';', 'GTT', ',', 'glucose',
    #                       'tolerance', 'test', ';', 'Hb', 'A', ',', 'glycated', 'hemoglobin', ';', 'IDDM', ',',
    #                       'insulin', 'dependent', 'diabetes', 'mellitus', ';', 'NIDDM', ',', 'non', '--',
    #                       'insulin-dependent', 'diabetes', 'mellitus', ';', 'RTEC', ',', 'ready-to-eat', 'breakfast',
    #                       'cereal', ';', 'SRS', ',', 'slow', 'release', 'starch', '.']
    #     )
    #     diseases_expected = [('diabetes mellitus', 'DOID:9351'), ('diabetes mellitus', 'DOID:9351')]
    #     nutrients_expected = [('starch', 'Starch'), ('glucose', 'Glucose')]
    #     bacteria_expected = []
    #     food_expected = []
    #
    #     self.assertListEqual(bacteria_expected, bacteria_new)
    #     self.assertListEqual(nutrients_expected, nutrients_new)
    #     self.assertListEqual(diseases_expected, diseases_new)
    #     self.assertListEqual(food_expected, food_new)

    def test_remove_pmc_from_pmcid(self):
        actual = remove_pmc_from_pmcid("PMC123456")
        self.assertEqual(actual, "123456")



if __name__ == '__main__':
    unittest.main()

