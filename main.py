# -*- coding: utf-8 -*-

from nltk.parse.stanford import StanfordDependencyParser

from article_data_loader import get_articles_nxmls, get_article_text
from sentence_processing import SentenceParser
from nutrients_catalog import NutrientsCatalog
from bacteria_catalog import BacteriaCatalog
from sentence import Sentence

bacteria_catalog = BacteriaCatalog(verbose=True)
nutrients_catalog = NutrientsCatalog(verbose=True)
stanford_dependency_parser = StanfordDependencyParser(
    path_to_jar='./stanford_parser/stanford-parser.jar',
    path_to_models_jar='./stanford_parser/stanford-parser-3.5.2-models.jar',
    model_path='./stanford_parser/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz'
    )
sentence_parser = SentenceParser(stanford_dependency_parser)


# Здесь лучше сначала просто создать список предложений, а уже в цикле создавать объект нашего класса
def main(articles_directory):
    nxml_list = get_articles_nxmls(articles_directory)
    raw_sentences = (sentence for nxml in nxml_list for sentence in get_article_text(nxml))
    results = []
    for raw_sentence in raw_sentences:
        sentence = Sentence(raw_sentence)
        sentence.bacteria = bacteria_catalog.find(sentence.text)
        sentence.nutrients = nutrients_catalog.find(sentence.text)
        if not (sentence.bacteria and sentence.nutrients):
            continue
        sentence.parser_output = sentence_parser.parse_sentence(sentence.text)
        # analyser_output = analyser.analyse(sentence)

main('../article_data/texts/')