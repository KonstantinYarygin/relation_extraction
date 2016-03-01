import os
import sys

from nltk.parse.stanford import StanfordDependencyParser
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import StanfordTokenizer

from ohmygut.core.analyzer import SentenceAnalyzer
from ohmygut.core.article.file_article_data_source import FileArticleDataSource
from ohmygut.core.catalog.diseases_catalog import DiseasesCatalog
from ohmygut.core.catalog.gut_bacteria_catalog import GutBacteriaCatalog
from ohmygut.core.catalog.nutrients_catalog import NutrientsCatalogNikogosov
from ohmygut.core.main import main
from ohmygut.core.sentence_processing import SentenceParser

script_dir = os.path.dirname(os.path.realpath(__file__))

lancaster_stemmer = LancasterStemmer()
stanford_tokenizer = StanfordTokenizer(path_to_jar=os.path.join(script_dir,
                                                                '../data/stanford_parser_dependencies/stanford-parser.jar'))
sentence_analyzer = SentenceAnalyzer(stemmer=lancaster_stemmer, tokenizer=stanford_tokenizer)

stanford_dependency_parser = StanfordDependencyParser(
    path_to_jar=os.path.join(script_dir, '../data/stanford_parser_dependencies/stanford-parser.jar'),
    path_to_models_jar=os.path.join(script_dir, '../data/stanford_parser_dependencies/stanford-parser-3.5.2-models.jar'),
    model_path=os.path.join(script_dir, '../data/stanford_parser_dependencies/englishPCFG.ser.gz'),
)
sentence_parser = SentenceParser(stanford_dependency_parser)

bacteria_catalog = GutBacteriaCatalog(os.path.join('../data/bacteria/gut_catalog.csv'))
bacteria_catalog.initialize(verbose=True)

nutrients_catalog = NutrientsCatalogNikogosov(
    path=os.path.join(script_dir, '../data/nutrients/nikogosov_nutrients_normalized.tsv'))
nutrients_catalog.initialize(verbose=True)

diseases_catalog = DiseasesCatalog(doid_path=os.path.join(script_dir, '../data/diseases/doid.obo'))
diseases_catalog.initialize(verbose=True)

article_data_source = FileArticleDataSource(articles_folder=os.path.join(script_dir, '../data/articles/'))

main(article_data_source, bacteria_catalog, nutrients_catalog, diseases_catalog, sentence_parser, sentence_analyzer)
