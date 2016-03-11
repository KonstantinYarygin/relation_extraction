import os
import pickle
import re
from itertools import product

import pandas as pd
from nltk import sent_tokenize

from ohmygut.core.constants import TRIM_LETTERS_NUMBER


def get_sentences(text):
    return sent_tokenize(text)


def remove_entity_overlapping(sentence, bacteria, nutrients, diseases, stanford_tokenizer):
    sentence_tokens = stanford_tokenizer.tokenize(sentence)
    tokens_lists = {}
    tokens_lists['bacteria'] = [bacterium_name.split(' ') for bacterium_name, ncbi_id in bacteria]
    tokens_lists['nutrients'] = [nutrient_name.split(' ') for nutrient_name, idname in nutrients]
    tokens_lists['diseases'] = [disease_name.split(' ') for disease_name, doid_id in diseases]

    entities = ['bacteria', 'nutrients', 'diseases']

    tokens_coordinates = {entity: [] for entity in entities}

    for entity in entities:
        for tokens_list in tokens_lists[entity]:
            for i in range(len(sentence_tokens) - len(tokens_list) + 1):
                if sentence_tokens[i:i + len(tokens_list)] == tokens_list:
                    if (i, i + len(tokens_list)) not in tokens_coordinates[entity]:
                        tokens_coordinates[entity].append((i, i + len(tokens_list)))
                        break

    for entity_1, entity_2 in product(entities, entities):
        for entity_1_coordinates in tokens_coordinates[entity_1]:
            for entity_2_coordinates in tokens_coordinates[entity_2]:
                set_1 = set(range(*entity_1_coordinates))
                set_2 = set(range(*entity_2_coordinates))
                intersection = set_1 & set_2
                if intersection == set_1 and intersection != set_2:
                    tokens_coordinates[entity_1].remove(entity_1_coordinates)
                elif intersection == set_2 and intersection != set_1:
                    tokens_coordinates[entity_2].remove(entity_2_coordinates)

    bacteria_new = [' '.join(sentence_tokens[i:j]) for i, j in tokens_coordinates['bacteria']]
    nutrients_new = [' '.join(sentence_tokens[i:j]) for i, j in tokens_coordinates['nutrients']]
    diseases_new = [' '.join(sentence_tokens[i:j]) for i, j in tokens_coordinates['diseases']]

    bacteria_new = [(name, dict(bacteria)[name]) for name in bacteria_new]
    nutrients_new = [(name, dict(nutrients)[name]) for name in nutrients_new]
    diseases_new = [(name, dict(diseases)[name]) for name in diseases_new]

    return (bacteria_new, nutrients_new, diseases_new)


def untokenize(tokens):
    result = ' '.join(tokens)
    result = result.replace(' , ', ', ').replace(' .', '.').replace(' !', '!')
    result = result.replace(' ?', '?').replace(' : ', ': ').replace(' \'', '\'')
    result = result.replace('( ', '(').replace(' )', ')')
    return result


def sentences_to_data_frame(sentences):
    data_list = map(lambda x: [x.text,
                               x.article_title,
                               x.journal,
                               str(x.bacteria),
                               str(x.nutrients),
                               str(x.diseases),
                               ], sentences)
    data = pd.DataFrame(list(data_list),
                        columns=['text', 'article_title', 'journal',
                                 'bacteria', 'nutrients', 'diseases'])
    return data


def serialize_result(sentence, save_path, sentence_number):
    filename = '%s_%s_%i.pkl' % (sentence.journal[0:TRIM_LETTERS_NUMBER], sentence.article_title[0:TRIM_LETTERS_NUMBER], sentence_number)
    filename = delete_forbidden_characters(filename)
    filename = os.path.join(save_path, filename)
    with open(filename, 'wb') as f:
        pickle.dump(sentence, f)


def delete_forbidden_characters(string):
    return_string = string.replace(' ', '_')
    return_string = re.sub('[^\w_\d\.]', '', return_string)
    return return_string
