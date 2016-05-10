import os
import unittest

import pandas as pd
import pickle

from ohmygut.core.sentence import Sentence
from ohmygut.core.write.csv_writer import CsvWriter, CSV_SEPARATOR, INCLUDE_HEADER
from ohmygut.core.write.pkl_writer import PklWriter


class TestCase(unittest.TestCase):
    def test_csv_write(self):
        test_path = os.path.join('result', "test.csv")
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
        if INCLUDE_HEADER:
            header = 0
        else:
            header = None

        df1 = pd.read_csv(test_path, sep=CSV_SEPARATOR, header=header)
        self.assertTrue(df1.shape[0] == 1)

        target.write(test_sentence2)
        df2 = pd.read_csv(test_path, sep=CSV_SEPARATOR, header=header)
        self.assertTrue(df2.shape[0] == 2)

    def test_pkl_write(self):
        output_dir = "result/"

        target = PklWriter(output_dir)
        test_sentence1 = Sentence("a text", "article", "journal",
                                  "bacteria", "nutrient", "disease", "food",
                                  "parser_output", "shortest_paths")
        res_path = os.path.join(output_dir, "journal_article_1.pkl")
        if os.path.exists(res_path):
            os.remove(res_path)
        target.write(test_sentence1)
        with open(res_path, 'rb') as f:
            actual = pickle.load(f)
        self.assertTrue(actual, test_sentence1)


if __name__ == '__main__':
    unittest.main()
