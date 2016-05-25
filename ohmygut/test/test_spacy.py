import unittest

from ohmygut.core.catalog.catalog import EntityCollection, Entity
from ohmygut.core.catalog.diseases_catalog import DISEASE_TAG
from ohmygut.core.catalog.gut_bacteria_catalog import BACTERIA_TAG
from ohmygut.core.catalog.nutrients_catalog import NUTRIENT_TAG
from ohmygut.core.sentence_processing import SpacySentenceParser


class TestCase(unittest.TestCase):
    def test_something(self):
        parser = SpacySentenceParser()
        sentence = 'M._tuberculosis is the cause of tuberculosis and chronic_obstructive_syndrome, ' \
                   'also M._tuberculosis is a propionic acid producer.'
        bacteria = EntityCollection([Entity('M._tuberculosis', '111', BACTERIA_TAG),
                                     Entity('M._tuberculosis', '111', BACTERIA_TAG)], tag=BACTERIA_TAG)
        nutrients = EntityCollection([Entity('propionic', '123', NUTRIENT_TAG)])
        diseases = EntityCollection([Entity('tuberculosis', 'a', DISEASE_TAG),
                                     Entity('tuberculosis', 'a', DISEASE_TAG),
                                     Entity('tuberculosis', 'a', DISEASE_TAG),
                                     Entity('chronic_obstructive_syndrome', 'a1', DISEASE_TAG),
                                     Entity('obstructive_syndrome', 'b1', DISEASE_TAG)])
        not_overlapped_collections = [EntityCollection([bacteria.entities[0], bacteria.entities[1]]),
                                      EntityCollection([diseases.entities[1], diseases.entities[3]]),
                                      EntityCollection([nutrients.entities[0]])]

        parser_output = parser.parse_sentence(sentence, not_overlapped_collections[0].entities +
                                              not_overlapped_collections[1].entities +
                                              not_overlapped_collections[2].entities)

        expected_bact_tags = [0, 10]
        expected_nut_tags = [13]
        expected_dis_tags = [5, 7]
        actual_bact_tags = [i for i, tag in parser_output.tags.items() if tag == BACTERIA_TAG]
        actual_nut_tags = [i for i, tag in parser_output.tags.items() if tag == NUTRIENT_TAG]
        actual_dis_tags = [i for i, tag in parser_output.tags.items() if tag == DISEASE_TAG]

        self.assertCountEqual(expected_bact_tags, actual_bact_tags)
        self.assertCountEqual(expected_nut_tags, actual_nut_tags)
        self.assertCountEqual(expected_dis_tags, actual_dis_tags)

if __name__ == '__main__':
    unittest.main()
