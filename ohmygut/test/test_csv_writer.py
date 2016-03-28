import os
import unittest

import pandas as pd

from ohmygut.core.sentence import Sentence
from ohmygut.core.write.csv_writer import CsvWriter, CSV_SEPARATOR, DO_INCLUDE_HEADER


class TestCase(unittest.TestCase):
    def test_write(self):
        test_path = "test.csv"
        if os.path.exists(test_path):
            os.remove(test_path)
        target = CsvWriter(test_path)
        test_sentence1 = Sentence("a text", "article", "journal",
                                  "bacteria", "nutrient", "disease", "food",
                                  "parser_output", "shortest_paths")
        test_sentence2 = Sentence("a text #2", "article", "journal",
                                  "bacteria #2", "nutrient #2", "disease #2", "food #2",
                                  "parser_output", "shortest_paths")
        target.write(test_sentence1)
        if DO_INCLUDE_HEADER:
            header = 0
        else:
            header = None

        df1 = pd.read_csv(test_path, sep=CSV_SEPARATOR, header=header)
        self.assertTrue(df1.shape[0] == 1)

        target.write(test_sentence2)
        df2 = pd.read_csv(test_path, sep=CSV_SEPARATOR, header=header)
        self.assertTrue(df2.shape[0] == 2)


if __name__ == '__main__':
    unittest.main()
