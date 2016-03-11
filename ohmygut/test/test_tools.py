import unittest

from ohmygut.core.tools import get_sentences, remove_entity_overlapping


class TestCase(unittest.TestCase):
    def test_get_sentences(self):
        test_text = "First sentence. Second sentence. Sentence with 2.0 number. Sentence with H. pylori. Good bye."
        expected = ["First sentence.", "Second sentence.", "Sentence with 2.0 number.", "Sentence with H. pylori.",
                    "Good bye."]
        actual = get_sentences(test_text)
        self.assertListEqual(expected, actual)

    def test_remove_entity_overlapping(self):
        sentence = 'M. tuberculosis is the cause of tuberculosis and chronic obstructive syndrome, also M. tuberculosis is a propionic acid producer.'
        bacteria = [('M. tuberculosis', '111'), ('M. tuberculosis', '111')]
        nutrients = [('propionic', '123')]
        diseases = [('tuberculosis', 'a'), ('tuberculosis', 'a'), ('tuberculosis', 'a'),
                    ('chronic obstructive syndrome', 'a1'), ('obstructive syndrome', 'b1')]

        class MockTokenizer():
            def tokenize(self):
                tokens = ['M.', 'tuberculosis', 'is', 'the', 'cause', 'of', 'tuberculosis', 'and', 'chronic',
                          'obstructive',
                          'syndrome', ',', 'also', 'M.', 'tuberculosis', 'is', 'a', 'propionic', 'acid', 'producer',
                          '.']
                return tokens

        bacteria_new, nutrients_new, diseases_new = remove_entity_overlapping(sentence, bacteria, nutrients, diseases,
                                                                              stanford_tokenizer=MockTokenizer)

        bacteria_expected = [('M. tuberculosis', '111'), ('M. tuberculosis', '111')]
        nutrients_expected = [('propionic', '123')]
        diseases_expected = [('tuberculosis', 'a'), ('chronic obstructive syndrome', 'a1')]

        self.assertListEqual(bacteria_expected, bacteria_new)
        self.assertListEqual(nutrients_expected, nutrients_new)
        self.assertListEqual(diseases_expected, diseases_new)


if __name__ == '__main__':
    unittest.main()
