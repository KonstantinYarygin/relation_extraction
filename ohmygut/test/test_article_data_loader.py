import unittest

from ohmygut.core.article_data_loader import get_article_text, get_sentences


class TestCase(unittest.TestCase):
    def test_get_article_text(self):
        text_xml = "<!DOCTYPE article>" \
                   "<article> " \
                   "<front>blabla</front>" \
                   "<body>" \
                   "<p>text!</p>" \
                   "not interesting text" \
                   "<p>text<strong> again</strong>!</p>" \
                   "</body>" \
                   "</article>"
        expected = "text! text again! "
        actual = get_article_text(text_xml)
        self.assertEqual(expected, actual)

    def test_get_sentences(self):
        test_text = "First sentence. Second sentence. Sentence with 2.0 number. Sentence with H. pylori. Good bye."
        expected = ["First sentence.", "Second sentence.", "Sentence with 2.0 number.", "Sentence with H. pylori.",
                    "Good bye."]
        actual = get_sentences(test_text)
        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
