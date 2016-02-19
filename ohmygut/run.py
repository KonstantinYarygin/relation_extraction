import sys
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(script_dir, '..'))

from nltk.parse.stanford import StanfordDependencyParser
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import StanfordTokenizer

from ohmygut.core.article.file_article_data_source import FileArticleDataSource
from ohmygut.core.catalog.bacteria_catalog import BacteriaCatalog
from ohmygut.core.catalog.nutrients_catalog import NutrientsCatalog
from ohmygut.core.catalog.diseases_catalog import DiseasesCatalog
from ohmygut.core.sentence_processing import SentenceParser
from ohmygut.core.analyzer import SentenceAnalyzer
from ohmygut.core.main import main

lancaster_stemmer = LancasterStemmer()
stanford_tokenizer = StanfordTokenizer(path_to_jar=os.path.join(script_dir, '../stanford_parser/stanford-parser.jar')) 
sentence_analyzer = SentenceAnalyzer(stemmer=lancaster_stemmer, tokenizer=stanford_tokenizer)

stanford_dependency_parser = StanfordDependencyParser(
    path_to_jar=os.path.join(script_dir, '../stanford_parser/stanford-parser.jar'),
    path_to_models_jar=os.path.join(script_dir, '../stanford_parser/stanford-parser-3.5.2-models.jar'),
    model_path=os.path.join(script_dir, '../stanford_parser/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'),
    )
sentence_parser = SentenceParser(stanford_dependency_parser)

bacteria_catalog = BacteriaCatalog(nodes_path=os.path.join(script_dir, '../data/bacteria/taxdump/nodes.dmp'),
                                   names_path=os.path.join(script_dir, '../data/bacteria/taxdump/names.dmp'),
                                   tokenizer=stanford_tokenizer)
bacteria_catalog.initialize(verbose=True)

nutrients_catalog = NutrientsCatalog(path=os.path.join(script_dir, '../data/nutrients/natalia_nitrients.txt'),
									 tokenizer=stanford_tokenizer)
nutrients_catalog.initialize(verbose=True)

diseases_catalog = DiseasesCatalog(doid_path=os.path.join(script_dir, '../data/diseases/doid.obo'),
								   tokenizer=stanford_tokenizer)
diseases_catalog.initialize(verbose=True)


article_data_source = FileArticleDataSource(articles_folder = os.path.join(script_dir, '../../article_data/texts/'))

main(article_data_source, bacteria_catalog, nutrients_catalog, diseases_catalog, sentence_parser, sentence_analyzer)