# -*- coding: utf-8 -*-

from ohmygut.core.sentence import Sentence


# Здесь лучше сначала просто создать список предложений, а уже в цикле создавать объект нашего класса
def main(articles_directory, bacteria_catalog, nutrients_catalog, sentence_parser):
    articles_nxml_list = get_articles_nxmls(articles_directory)
    article_texts = map(get_article_text, articles_nxml_list)
    raw_sentences = []
    results = []
    for raw_sentence in raw_sentences:
        sentence = Sentence(raw_sentence)
        sentence.bacteria = bacteria_catalog.find(sentence.text)
        sentence.nutrients = nutrients_catalog.find(sentence.text)
        if not (sentence.bacteria and sentence.nutrients):
            continue
        sentence.parser_output = sentence_parser.parse_sentence(sentence.text)
        # analyser_output = analyser.analyse(sentence)

