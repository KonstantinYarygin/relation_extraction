import unittest

from ohmygut.core.tools import get_sentences


class TestCase(unittest.TestCase):
    def test_get_sentences(self):
        test_text = "First sentence. Second sentence. Sentence with 2.0 number. Sentence with H. pylori. Good bye."
        expected = ["First sentence.", "Second sentence.", "Sentence with 2.0 number.", "Sentence with H. pylori.",
                    "Good bye."]
        actual = get_sentences(test_text)
        self.assertListEqual(expected, actual)

    def test_get_sentences_tyakht(self):
        test_text = "Was (Tyakht et al. 2008) shown that xxx. Sentence two."
        expected = ["Was (Tyakht et al. 2008) shown that xxx.", "Sentence two."]
        actual = get_sentences(test_text)
        self.assertListEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
