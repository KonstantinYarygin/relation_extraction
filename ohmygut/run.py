from nltk.parse.stanford import StanfordDependencyParser

from ohmygut.core.article.file_article_data_source import FileArticleDataSource
from ohmygut.core.bacteria_catalog import BacteriaCatalog
from ohmygut.core.main import main
from ohmygut.core.nutrients_catalog import NutrientsCatalog
from ohmygut.core.sentence_processing import SentenceParser

bacteria_catalog = BacteriaCatalog(verbose=True)
nutrients_catalog = NutrientsCatalog(verbose=True)
stanford_dependency_parser = StanfordDependencyParser(
    path_to_jar='./stanford_parser/stanford-parser.jar',
    path_to_models_jar='./stanford_parser/stanford-parser-3.5.2-models.jar',
    model_path='./stanford_parser/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'
    )
sentence_parser = SentenceParser(stanford_dependency_parser)
article_data_source = FileArticleDataSource('../article_data/texts/')

main(article_data_source, bacteria_catalog, nutrients_catalog, sentence_parser)