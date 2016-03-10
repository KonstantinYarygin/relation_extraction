# -*- coding: utf-8 -*-

import datetime
import pandas as pd
from ohmygut.core.sentence import Sentence
from ohmygut.core.tools import get_sentences, remove_entity_overlapping


def sentences_to_data_frame(sentences):
    data_list = map(lambda x: [x.text,
                               x.article_title,
                               x.journal,
                               str(x.bacteria),
                               str(x.nutrients),
                               str(x.diseases),
                               str(x.parse_result)
                               ], sentences)
    data = pd.DataFrame(list(data_list),
                        columns=['text', 'article_title', 'journal',
                                 'bacteria', 'nutrients', 'diseases', 'parse_result'])
    return data


def main(article_data_source, bacteria_catalog, nutrients_catalog, diseases_catalog, sentence_parser,
         sentence_analyzer):
    articles = article_data_source.get_articles()
    sentences_titles_journals_tuple = ((sentence, article.title, article.journal) for article in articles
                                       for sentence in get_sentences(article.text))
    sentences = []
    n = 0

    for sentence_text, article_title, article_journal in sentences_titles_journals_tuple:
        bacteria = bacteria_catalog.find(sentence_text)
        nutrients = nutrients_catalog.find(sentence_text)
        diseases = diseases_catalog.find(sentence_text)
        diseases = []

        if sum(map(bool, [bacteria, nutrients, diseases])) < 2:
            continue

        bacteria, nutrients, diseases = remove_entity_overlapping(sentence_text, bacteria, nutrients, diseases,
                                                                  sentence_analyzer.get_tokenizer())

        if sum(map(bool, [bacteria, nutrients, diseases])) < 2:
            continue

        print(sentence_text)
        print(bacteria)
        print(nutrients)
        print()
        n +=1
        parser_output = sentence_parser.parse_sentence(sentence_text)
        if not parser_output:
            continue

        sentence = Sentence(text=sentence_text,
                            article_title=article_title,
                            bacteria=bacteria,
                            nutrients=nutrients,
                            diseases=diseases,
                            parse_result=parser_output)
        print(sentence)
        n += 1
        print("sentence № %i" % n)
        sentences.append(sentence)
        print('=' * 80)

    data = sentences_to_data_frame(sentences)
    data.to_csv('sentences%s.csv' % (datetime.datetime.now().strftime("%H_%M_%S-%d_%m_%y")))
