import os
import unittest

from ohmygut.core.article.article import Article
from ohmygut.core.article.file_article_data_source import get_article_text, FileArticleDataSource

script_dir = os.path.dirname(os.path.realpath(__file__))


class TestCase(unittest.TestCase):
    def test_get_articles(self):
        test_articles_directory = os.path.join(script_dir, 'resource/test_articles')
        target = FileArticleDataSource(test_articles_directory)

        expected = [Article("A title", "text! text again!")]
        actual = target.get_articles()

        for expected_article, actual_article in zip(expected, actual):
            self.assertEqual(expected_article, actual_article)

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
        expected = "text! text again!"
        actual = get_article_text(text_xml)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
