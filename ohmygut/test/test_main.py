import unittest
from unittest.mock import MagicMock, patch

from ohmygut.core.article.article import Article
from ohmygut.core.article.article_data_source import ArticleDataSource
from ohmygut.core.catalog.catalog import Catalog
from ohmygut.core.main import main
from ohmygut.core.sentence_processing import SentenceParser


class MockCatalog(Catalog):
    def __init__(self, prefix=""):
        super().__init__()
        self.prefix = prefix

    def initialize(self):
        pass

    def find(self, sentence_text):
        return [('bacteria%s' % self.prefix , 'code%s' % self.prefix)]


class MockDataSource(ArticleDataSource):
    def get_articles(self):
        articles = [Article("title", "text", "journal"), Article("title", "text", "journal"),
                    Article("title", "text", "journal")]
        for article in articles:
            yield article


class TestCase(unittest.TestCase):
    @patch("ohmygut.core.main.remove_entity_overlapping", return_value=([("bac1","cod1")], [("bac2","cod2")], []) )
    @patch("ohmygut.core.main.analyze_sentence", return_value=["yeah"])
    @patch("ohmygut.core.main.log_paths")
    def test_main(self, mock_remove_entity_overlapping, mock_analyze_sentence, mock_log_paths):
        article_data_sources = [MockDataSource(), MockDataSource()]
        bacteria_catalog = MockCatalog("a")
        nutrients_catalog = MockCatalog("b")
        diseases_catalog = MockCatalog("c")
        sentence_parser = SentenceParser(stanford_dependency_parser=None)
        sentence_parser.parse_sentence = MagicMock()
        sentence_parser.parse_sentence.return_value = ["yeah"]
        main(article_data_sources, bacteria_catalog, nutrients_catalog, diseases_catalog, sentence_parser,
             tokenizer=None, pattern_finder=None)

        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
