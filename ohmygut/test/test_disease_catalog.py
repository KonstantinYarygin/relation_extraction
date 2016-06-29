import os
import unittest

from ohmygut.core.catalog.catalog import Entity
from ohmygut.core.catalog.diseases_catalog import DiseasesCatalog, DISEASE_TAG

script_dir = os.path.dirname(os.path.realpath(__file__))
resource_dir = os.path.join(script_dir, "resource")


class TestCase(unittest.TestCase):
    def test_with_apostrophe(self):
        catalog_path = os.path.join(resource_dir, "disease_catalog.csv")
        target = DiseasesCatalog(catalog_path)
        target.initialize()
        expected_dict = {
            "angiosarcoma": "DOID:0001816",
            "ANGIOSARCOMA": "DOID:0001816",
            "Angiosarcoma": "DOID:0001816",
            "hemangiosarcoma foo": "DOID:0001816",
            "Hemangiosarcoma foo": "DOID:0001816",
            "Hemangiosarcoma Foo": "DOID:0001816",
            "HEMANGIOSARCOMA FOO": "DOID:0001816",
            "pterygium": "DOID:0002116",
            "PTERYGIUM": "DOID:0002116",
            "crohns disease": "DOID:0002116",
            "Crohns Disease": "DOID:0002116",
            "CROHNS DISEASE": "DOID:0002116",
            "Crohns disease": "DOID:0002116",

        }
        self.assertCountEqual(target.disease_dictionary, expected_dict)

        test_sentence = "Recent study showed that Hemangiosarcoma Foo and Crohn's disease both are really bad stuff"
        actual_found = target.find(test_sentence)
        expected_found = [Entity("Hemangiosarcoma Foo", "DOID0001816", DISEASE_TAG),
                          Entity("Crohns disease", "DOID0002116", DISEASE_TAG)]

        self.assertCountEqual(actual_found.entities, expected_found)


if __name__ == '__main__':
    unittest.main()
