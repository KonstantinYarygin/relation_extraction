import os
import unittest

from ohmygut.core.sentence import Sentence
from ohmygut.core.tools import get_sentences, remove_entity_overlapping, delete_forbidden_characters, serialize_result

script_dir = os.path.dirname(os.path.realpath(__file__))

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

    def test_delete_forbidden_characters(self):
        string = "Abbb ###\\ sss22_% 4 asd."
        expected = "Abbb__sss22__4_asd."
        actual = delete_forbidden_characters(string)

        self.assertEqual(expected, actual)

    def test_serialize_result(self):
        sentence = Sentence("text of the sentence", "Article Title456789012\\", None, None, None, None, "Science-Nature")
        expected_file_name = os.path.join(script_dir, "ScienceNature_Article_Title4567890_2.pkl")
        try:
            os.remove(expected_file_name)
        except:
            pass

        serialize_result(sentence, script_dir, 2)
        if_exists = os.path.exists(expected_file_name)
        self.assertEqual(if_exists, True)


if __name__ == '__main__':
    unittest.main()
