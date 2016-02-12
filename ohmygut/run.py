import os

from nltk.parse.stanford import StanfordDependencyParser

from ohmygut.core.article.file_article_data_source import FileArticleDataSource
from ohmygut.core.catalog.bacteria_catalog import BacteriaCatalog
from ohmygut.core.catalog.nutrients_catalog import NutrientsCatalog
from ohmygut.core.main import main
from ohmygut.core.sentence_processing import SentenceParser

script_dir = os.path.dirname(os.path.realpath(__file__))
bacteria_catalog = BacteriaCatalog(nodes_path=os.path.join(script_dir, '../data/bacteria/taxdump/nodes.dmp'),
                                   names_path=os.path.join(script_dir, '../data/bacteria/taxdump/names.dmp'),
                                   verbose=True)
nutrients_catalog = NutrientsCatalog(path=os.path.join(script_dir, '../data/nutrients/natalia_nitrients.txt'),
                                     verbose=True)

stanford_dependency_parser = StanfordDependencyParser(
    path_to_jar='./stanford_parser/stanford-parser.jar',
    path_to_models_jar='./stanford_parser/stanford-parser-3.5.2-models.jar',
    model_path='./stanford_parser/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'
    )
sentence_parser = SentenceParser(stanford_dependency_parser)
article_data_source = FileArticleDataSource('../article_data/texts/')

main(article_data_source, bacteria_catalog, nutrients_catalog, sentence_parser)