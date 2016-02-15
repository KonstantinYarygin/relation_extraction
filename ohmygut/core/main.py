# -*- coding: utf-8 -*-

from ohmygut.core.sentence import Sentence
from ohmygut.core.tools import get_sentences


def main(article_data_source, bacteria_catalog, nutrients_catalog, diseases_catalog, sentence_parser):
    articles = article_data_source.get_articles()
    sentences_titles_tuple = ((sentence, article.title) for article in articles \
                              for sentence in get_sentences(article.text))
    results = []
    for sentence_text, article_title in sentences_titles_tuple:
        bacteria = bacteria_catalog.find(sentence_text)
        nutrients = nutrients_catalog.find(sentence_text)
        diseases = diseases_catalog.find(sentence_text)
        if sum(map(bool, [bacteria, nutrients, diseases])) < 2:
            continue
        parser_output = sentence_parser.parse_sentence(sentence_text)
        sentence = Sentence(text=sentence_text,
                            article_title=article_title,
                            bacteria=bacteria,
                            nutrients=nutrients,
                            diseases=diseases,
                            parse_result=parser_output)
        print(sentence)
        print()
        # analyser_output = analyser.analyse(sentence)
