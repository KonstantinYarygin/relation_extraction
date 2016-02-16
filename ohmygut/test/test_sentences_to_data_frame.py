import unittest

from ohmygut.core.main import sentences_to_data_frame
from ohmygut.core.sentence import Sentence


class TestCase(unittest.TestCase):
    def test_sentences_to_data_frame(self):
        sentences = [
            Sentence('sentence text', 'title1', ['bac1', 'bac2'], ['nut1'], [], 'parse result'),
            Sentence('sentence text text', 'title2', ['bac1', 'bac2'], ['nut1'], [], 'parse result'),
            Sentence('sentence text 3', 'title3', ['bac1', 'bac2', 'bac3'], ['nut1', 'nut2'], [], 'parse result')
                     ]

        actual = sentences_to_data_frame(sentences)
        print(actual)


if __name__ == '__main__':
    unittest.main()
