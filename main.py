import os

from article_data_loader import get_articles_nxmls, get_article_text
from sentence import Sentence
from bacteria_catalog import BacteriaCatalog
from nutrients_catalog import NutrientsCatalog
# from sentence_processing import SentenceGraphCreator

bacteria_catalog = BacteriaCatalog(verbose=True)
nutrients_catalog = NutrientsCatalog(verbose=True)


def main(articles_directory):
    nxml_list = get_articles_nxmls(articles_directory)
    sentences = (Sentence(sentence) for nxml in nxml_list for sentence in get_article_text(nxml))
    results = []
    for sentence in sentences:
        bacteria = bacteria_catalog.find(sentence.text)
        nutrients = nutrients_catalog.find(sentence.text)
        if bacteria and nutrients:
            print(sentence)
            print(bacteria)
            print(nutrients)
            print()



main('../article_data/texts/')