import os
import unittest

from ohmygut.core.catalog.usda_food_catalog import UsdaFoodCatalog

script_dir = os.path.dirname(os.path.realpath(__file__))


class TestCase(unittest.TestCase):
    test_data_file_name = "test_food_data.tsv"

    def test_initialize(self):
        target = UsdaFoodCatalog(os.path.join(script_dir, self.test_data_file_name))
        target.initialize()

    def test_search(self):
        target = UsdaFoodCatalog(os.path.join(script_dir, self.test_data_file_name))
        target.initialize()

        actual1 = target.find("Whipped cream substitute is very tasty")
        expected1 = ["Whipped cream substitute"]

        self.assertCountEqual(actual1, expected1)

        actual2 = target.find("It's appear to be that eggs with whipped cream substitute are very tasty")
        expected2 = ["whipped cream substitute", "eggs"]

        self.assertCountEqual(actual2, expected2)


if __name__ == '__main__':
    unittest.main()
