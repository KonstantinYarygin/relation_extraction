import unittest
from unittest.mock import MagicMock, patch

from ohmygut.core import constants
from ohmygut.core.article.article import Article
from ohmygut.core.article.article_data_source import ArticleDataSource
from ohmygut.core.catalog.catalog import Catalog
from ohmygut.core.constants import SENTENCE_LENGTH_THRESHOLD
from ohmygut.core.main import main, find_sentence
from ohmygut.core.sentence_processing import StanfordSentenceParser


class MockCatalog(Catalog):
    def __init__(self, prefix=""):
        super().__init__()
        self.prefix = prefix

    def initialize(self):
        pass

    def find(self, sentence_text):
        return [('bacteria%s' % self.prefix, 'code%s' % self.prefix)]


class MockDataSource(ArticleDataSource):
    def get_articles(self):
        articles = [Article("title", "text", "journal"), Article("title", "text", "journal"),
                    Article("title", "text", "journal")]
        for article in articles:
            yield article


class TestCase(unittest.TestCase):
    @patch("ohmygut.core.main.remove_entity_overlapping", return_value=([("bac1", "cod1")], [("bac2", "cod2")], []))
    @patch("ohmygut.core.main.analyze_sentence", return_value=["yeah"])
    def test_main(self, mock_remove_entity_overlapping, mock_analyze_sentence):
        article_data_sources = [MockDataSource(), MockDataSource()]
        bacteria_catalog = MockCatalog("a")
        nutrients_catalog = MockCatalog("b")
        diseases_catalog = MockCatalog("c")
        food_catalog = MockCatalog("d")
        sentence_parser = StanfordSentenceParser(stanford_dependency_parser=None, stanford_tokenizer=False)
        sentence_parser.parse_sentence = MagicMock()
        sentence_parser.parse_sentence.return_value = ["yeah"]
        constants.logger.info("asdasd")
        main(article_data_sources, bacteria_catalog, nutrients_catalog, diseases_catalog, food_catalog, sentence_parser,
             tokenizer=None, pattern_finder=None, writers=[])

    def test_find_sentence_very_long(self):
        sentence_text = "a very long" * SENTENCE_LENGTH_THRESHOLD * 2
        expected = None
        actual = find_sentence(sentence_text, article_title='', article_journal='',
                               bacteria_catalog=None, nutrients_catalog=None, diseases_catalog=None, food_catalog=None,
                               tokenizer=None, sentence_parser=None, pattern_finder=None)

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
