import os

from nltk.parse.stanford import StanfordDependencyParser
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import StanfordTokenizer

from ohmygut.core.article.file_article_data_source import NxmlFreeArticleDataSource
from ohmygut.core.article.libgen_txt_article_data_source import LibgenTxtArticleDataSource
from ohmygut.core.article.medline_abstracts_article_data_source import MedlineAbstractsArticleDataSource
from ohmygut.core.catalog.diseases_catalog import DiseasesCatalog
from ohmygut.core.catalog.gut_bacteria_catalog import GutBacteriaCatalog
from ohmygut.core.catalog.nutrients_catalog import NutrientsCatalogNikogosov
from ohmygut.core.catalog.usda_food_catalog import UsdaFoodCatalog
from ohmygut.core.main import main
from ohmygut.core.pattern_finder import PatternFinder
from ohmygut.core.sentence_processing import SentenceParser
from ohmygut.core.write.csv_writer import CsvWriter, get_csv_path
from ohmygut.core.write.log_writer import LogWriter
from ohmygut.core.write.pkl_writer import PklWriter, get_output_dir_path
from ohmygut.paths import stanford_jar_path, stanford_models_jar_path, stanford_lex_parser_path, food_file_path, \
    gut_catalog_file_path, nutrients_file_path, nxml_articles_dir, abstracts_dir, libgen_texts_dir, \
    verb_ontollogy_path, diseases_csv_path

script_dir = os.path.dirname(os.path.realpath(__file__))

stanford_tokenizer = StanfordTokenizer(
    path_to_jar=stanford_jar_path
)

stanford_dependency_parser = StanfordDependencyParser(
    path_to_jar=stanford_jar_path,
    path_to_models_jar=stanford_models_jar_path,
    model_path=stanford_lex_parser_path,
)

sentence_parser = SentenceParser(stanford_dependency_parser, stanford_tokenizer)

food_catalog = UsdaFoodCatalog(food_file_path)
food_catalog.initialize()

bacteria_catalog = GutBacteriaCatalog(gut_catalog_file_path)
bacteria_catalog.initialize()

nutrients_catalog = NutrientsCatalogNikogosov(path=nutrients_file_path)
nutrients_catalog.initialize()

diseases_catalog = DiseasesCatalog(diseases_csv_path=diseases_csv_path)
diseases_catalog.initialize()

nxml_article_data_source = NxmlFreeArticleDataSource(articles_folder=nxml_articles_dir)
medline_article_data_source = MedlineAbstractsArticleDataSource(medline_file=abstracts_dir)
libgen_article_data_source = LibgenTxtArticleDataSource(libgen_folder=libgen_texts_dir)

with open(verb_ontollogy_path) as f:
    verb_ontology = eval(''.join(f.readlines()))

lancaster_stemmer = LancasterStemmer()
pattern_finder = PatternFinder(verb_ontology, lancaster_stemmer)

article_data_sources = [nxml_article_data_source, libgen_article_data_source, medline_article_data_source]

output_dir = get_output_dir_path()
csv_path = get_csv_path()
csv_writer = CsvWriter(csv_path)
pkl_writer = PklWriter(output_dir)
log_writer = LogWriter()

main(article_data_sources,
     bacteria_catalog, nutrients_catalog, diseases_catalog, food_catalog,
     sentence_parser, stanford_tokenizer, pattern_finder, writers=[csv_writer, log_writer],
     do_parse=False, do_analyze=False)
