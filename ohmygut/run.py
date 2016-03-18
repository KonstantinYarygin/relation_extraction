import os

from nltk.parse.stanford import StanfordDependencyParser
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import StanfordTokenizer

from ohmygut.core.article.article import Article
from ohmygut.core.article.article_data_source import ArticleDataSource
from ohmygut.core.article.file_article_data_source import NxmlFreeArticleDataSource
from ohmygut.core.article.medline_abstracts_article_data_source import MedlineAbstractsArticleDataSource
from ohmygut.core.article.libgen_txt_article_data_source import LibgenTxtArticleDataSource
from ohmygut.core.catalog.catalog import Catalog
from ohmygut.core.catalog.diseases_catalog import DiseasesCatalog
from ohmygut.core.catalog.gut_bacteria_catalog import GutBacteriaCatalog
from ohmygut.core.catalog.nutrients_catalog import NutrientsCatalogNikogosov
from ohmygut.core.catalog.usda_food_catalog import UsdaFoodCatalog
from ohmygut.core.main import main
from ohmygut.core.pattern_finder import PatternFinder
from ohmygut.core.sentence_processing import SentenceParser

script_dir = os.path.dirname(os.path.realpath(__file__))

stanford_dependency_parser = StanfordDependencyParser(
    path_to_jar=os.path.join(script_dir, '../data/stanford_parser_dependencies/stanford-parser.jar'),
    path_to_models_jar=os.path.join(script_dir, '../data/stanford_parser_dependencies/stanford-parser-3.5.2-models.jar'),
    model_path=os.path.join(script_dir, '../data/stanford_parser_dependencies/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'),
)
sentence_parser = SentenceParser(stanford_dependency_parser)

food_catalog = UsdaFoodCatalog(os.path.join(script_dir, '../data/food/food.tsv'))
food_catalog.initialize()

bacteria_catalog = GutBacteriaCatalog(os.path.join(script_dir, '../data/bacteria/gut_catalog.csv'))
bacteria_catalog.initialize()

nutrients_catalog = NutrientsCatalogNikogosov(
    path=os.path.join(script_dir, '../data/nutrients/nikogosov_nutrients_normalized.tsv'))
nutrients_catalog.initialize()

diseases_catalog = DiseasesCatalog(doid_path=os.path.join(script_dir, '../data/diseases/doid.obo'))
diseases_catalog.initialize()

nxml_article_data_source = NxmlFreeArticleDataSource(articles_folder=os.path.join(script_dir, '../data/article 1/'))
medline_article_data_source = MedlineAbstractsArticleDataSource(medline_file=os.path.join(script_dir, '../../article_data/abstracts/gut_microbiota.medline.txt'))
libgen_article_data_source = LibgenTxtArticleDataSource(libgen_folder=os.path.join(script_dir, '../../article_data/libgen/'))

with open(os.path.join(script_dir, '../data/verb_ontology.json')) as f:
    verb_ontology = eval(''.join(f.readlines()))

lancaster_stemmer = LancasterStemmer()
stanford_tokenizer = StanfordTokenizer(path_to_jar=os.path.join(script_dir,
                                                                '../data/stanford_parser_dependencies/stanford-parser.jar'))
pattern_finder = PatternFinder(verb_ontology, lancaster_stemmer)


class MockCatalog(Catalog):
    def initialize(self):
        pass

    def find(self, sentence_text):
        return [('bacteria', 'code')]


class MockDataSource(ArticleDataSource):
    def get_articles(self):
        articles = [Article("title", "text", "journal"), Article("title", "text", "journal"), Article("title", "text", "journal")]
        for article in articles:
            yield article


mock_catalog = MockCatalog()

article_data_sources = [MockDataSource(), MockDataSource()]
main(article_data_sources,
     mock_catalog, mock_catalog, mock_catalog,
     sentence_parser, stanford_tokenizer, pattern_finder)
