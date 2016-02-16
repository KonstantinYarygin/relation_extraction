# -*- coding: utf-8 -*-
import pandas as pd

from ohmygut.core.sentence import Sentence
from ohmygut.core.tools import get_sentences


def sentences_to_data_frame(sentences):
    data_list = map(lambda x: [x.text,
                               x.article_title,
                               str(x.bacteria),
                               str(x.nutrients),
                               str(x.diseases),
                               str(x.parse_result)], sentences)
    data = pd.DataFrame(list(data_list),
                        columns=['text', 'article_title', 'bacteria', 'nutrients', 'diseases', 'parse_result'])
    return data


def main(article_data_source, bacteria_catalog, nutrients_catalog, diseases_catalog, sentence_parser):
    articles = article_data_source.get_articles()
    sentences_titles_tuple = ((sentence, article.title) for article in articles \
                              for sentence in get_sentences(article.text))
    sentences = []
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
        sentences.append(sentence)
        print(sentence)
        print()

    data = sentences_to_data_frame(sentences)
    data.to_csv('sentences.csv')
