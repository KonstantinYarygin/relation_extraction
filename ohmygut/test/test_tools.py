import os
import unittest

from ohmygut.core.catalog.catalog import Entity, EntityCollection
from ohmygut.core.catalog.diseases_catalog import DISEASE_TAG
from ohmygut.core.catalog.gut_bacteria_catalog import BACTERIA_TAG
from ohmygut.core.catalog.nutrients_catalog import NUTRIENT_TAG
from ohmygut.core.sentence import Sentence
from ohmygut.core.tools import get_sentences, remove_entity_overlapping

script_dir = os.path.dirname(os.path.realpath(__file__))


class TestCase(unittest.TestCase):
    def test_get_sentences(self):
        test_text = "First sentence. Second sentence. Sentence with 2.0 number. Sentence with H. pylori. Good bye."
        expected = ["First sentence.", "Second sentence.", "Sentence with 2.0 number.", "Sentence with H. pylori.",
                    "Good bye."]
        actual = get_sentences(test_text)
        self.assertListEqual(expected, actual)

    def test_remove_entity_overlapping_empty(self):
        sentence = 'There is really nothing'

        class MockTokenizer():
            def tokenize(self):
                tokens = ['There', 'is', 'really', 'nothing']
                return tokens

        output = remove_entity_overlapping(sentence, [EntityCollection([], 'tag1'), EntityCollection([], 'tag2')],
                                           stanford_tokenizer=MockTokenizer)

        expected = [EntityCollection([], 'tag1'), EntityCollection([], 'tag2')]

        self.assertCountEqual(expected[0].entities, output[0].entities)
        self.assertCountEqual(expected[1].entities, output[1].entities)

    def test_remove_entity_overlapping_2(self):
        sentence = 'M. tuberculosis is the cause of tuberculosis and chronic obstructive syndrome, ' \
                   'also M. tuberculosis is a propionic acid producer.'
        bacteria = EntityCollection([Entity('M. tuberculosis', '111', BACTERIA_TAG),
                                     Entity('M. tuberculosis', '111', BACTERIA_TAG)], tag=BACTERIA_TAG)
        nutrients = EntityCollection([Entity('propionic', '123', NUTRIENT_TAG)], NUTRIENT_TAG)
        diseases = EntityCollection([Entity('tuberculosis', 'a', DISEASE_TAG),
                                     Entity('tuberculosis', 'a', DISEASE_TAG),
                                     Entity('tuberculosis', 'a', DISEASE_TAG),
                                     Entity('chronic obstructive syndrome', 'a1', DISEASE_TAG),
                                     Entity('obstructive syndrome', 'b1', DISEASE_TAG)], DISEASE_TAG)

        class MockTokenizer():
            def tokenize(self):
                tokens = ['M.', 'tuberculosis', 'is', 'the', 'cause', 'of', 'tuberculosis', 'and', 'chronic',
                          'obstructive',
                          'syndrome', ',', 'also', 'M.', 'tuberculosis', 'is', 'a', 'propionic', 'acid', 'producer',
                          '.']
                return tokens

        output = remove_entity_overlapping(sentence, [bacteria, nutrients, diseases],
                                           stanford_tokenizer=MockTokenizer)

        expected = [EntityCollection([bacteria.entities[0], bacteria.entities[1]], BACTERIA_TAG),
                    EntityCollection([diseases.entities[1], diseases.entities[3]], DISEASE_TAG),
                    EntityCollection([nutrients.entities[0]], NUTRIENT_TAG)]

        self.assertCountEqual(expected[0].entities, output[0].entities)
        self.assertCountEqual(expected[1].entities, output[1].entities)
        self.assertCountEqual(expected[2].entities, output[2].entities)

    def test_remove_entity_overlapping_3(self):
        sentence = 'Intervention trials of breakfast cereals and diabetes CHO, carbohydrate; ' \
                   'FRS, fast release starch; GER, gastric emptying rate; GI, glycemic index; ' \
                   'GTT, glucose tolerance test; Hb A, glycated hemoglobin; IDDM, insulin dependent ' \
                   'diabetes mellitus; NIDDM, non–insulin-dependent diabetes mellitus; RTEC, ' \
                   'ready-to-eat breakfast cereal; SRS, slow release starch.'
        diseases = [('diabetes mellitus', 'DOID:9351'), ('diabetes mellitus', 'DOID:9351')]
        nutrients = [('starch', 'Starch'), ('glucose', 'Glucose')]
        bacteria = []
        food = []

        class MockTokenizer():
            def tokenize(self):
                tokens = ['Intervention', 'trials', 'of', 'breakfast', 'cereals', 'and', 'diabetes', 'CHO', ',',
                          'carbohydrate', ';', 'FRS', ',', 'fast', 'release', 'starch', ';', 'GER', ',', 'gastric',
                          'emptying', 'rate', ';', 'GI', ',', 'glycemic', 'index', ';', 'GTT', ',', 'glucose',
                          'tolerance', 'test', ';', 'Hb', 'A', ',', 'glycated', 'hemoglobin', ';', 'IDDM', ',',
                          'insulin', 'dependent', 'diabetes', 'mellitus', ';', 'NIDDM', ',', 'non', '--',
                          'insulin-dependent', 'diabetes', 'mellitus', ';', 'RTEC', ',', 'ready-to-eat', 'breakfast',
                          'cereal', ';', 'SRS', ',', 'slow', 'release', 'starch', '.']
                return tokens

        bacteria_new, nutrients_new, diseases_new, food_new = remove_entity_overlapping(
            sentence, bacteria, nutrients, diseases, food, stanford_tokenizer=MockTokenizer
        )
        diseases_expected = [('diabetes mellitus', 'DOID:9351'), ('diabetes mellitus', 'DOID:9351')]
        nutrients_expected = [('starch', 'Starch'), ('glucose', 'Glucose')]
        bacteria_expected = []
        food_expected = []

        self.assertListEqual(bacteria_expected, bacteria_new)
        self.assertListEqual(nutrients_expected, nutrients_new)
        self.assertListEqual(diseases_expected, diseases_new)
        self.assertListEqual(food_expected, food_new)


if __name__ == '__main__':
    unittest.main()
