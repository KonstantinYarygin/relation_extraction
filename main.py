# -*- coding: utf-8 -*-

from nltk.parse.stanford import StanfordDependencyParser


from article_data_loader import get_articles_nxmls, get_article_text
from nutrients_catalog import NutrientsCatalog
from bacteria_catalog import BacteriaCatalog
from sentence import Sentence
from sentence_processing import SentenceParser

# bacteria_catalog = BacteriaCatalog(verbose=True)
# nutrients_catalog = NutrientsCatalog(verbose=True)
stanford_dependency_parser = StanfordDependencyParser(
    path_to_jar='./stanford_parser/stanford-parser.jar',
    path_to_models_jar='./stanford_parser/stanford-parser-3.5.2-models.jar',
    model_path='./stanford_parser/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'
    )
sentence_parser = SentenceParser(stanford_dependency_parser)


def main(articles_directory):
    nxml_list = get_articles_nxmls(articles_directory)
    sentences = (Sentence(sentence) for nxml in nxml_list for sentence in get_article_text(nxml))
    results = []
    for sentence in sentences:
        print(sentence.text)
        # bacteria = bacteria_catalog.find(sentence.text)
        # nutrients = nutrients_catalog.find(sentence.text)
        # if not (bacteria and nutrients):
        #     continue
        # sentence_parser_output = sentence_parser.parse_sentence(sentence)


main('../article_data/texts/')