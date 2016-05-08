import os
from itertools import product

import pandas as pd
from nltk import sent_tokenize

from ohmygut.core.catalog.catalog import EntityCollection


def get_sentences(text):
    return sent_tokenize(text)


# todo: rewrite for any entities number (not only bacteria, nutrients, diseases)
def remove_entity_overlapping_old(sentence, bacteria, nutrients, diseases, food, stanford_tokenizer):
    # add all_catalog here
    # search for all bacterias
    tokens = stanford_tokenizer.tokenize(sentence)
    tokens_lists = {}
    tokens_lists['bacteria'] = [bacterium_name.split(' ') for bacterium_name, ncbi_id in bacteria]
    tokens_lists['nutrients'] = [nutrient_name.split(' ') for nutrient_name, idname in nutrients]
    tokens_lists['diseases'] = [disease_name.split(' ') for disease_name, doid_id in diseases]
    tokens_lists['food'] = [food_name.split(' ') for food_name, food_group in food]

    entities = ['bacteria', 'nutrients', 'diseases', 'food']

    tokens_coordinates = {entity: [] for entity in entities}

    for entity in entities:
        for tokens_list in tokens_lists[entity]:
            for i in range(len(tokens) - len(tokens_list) + 1):
                if tokens[i:i + len(tokens_list)] == tokens_list:
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
                elif intersection == set_1 and intersection == set_2 and entity_1 != entity_2:
                    tokens_coordinates[entity_2].remove(entity_2_coordinates)

    bacteria_new = [' '.join(tokens[i:j]) for i, j in tokens_coordinates['bacteria']]
    nutrients_new = [' '.join(tokens[i:j]) for i, j in tokens_coordinates['nutrients']]
    diseases_new = [' '.join(tokens[i:j]) for i, j in tokens_coordinates['diseases']]
    food_new = [' '.join(tokens[i:j]) for i, j in tokens_coordinates['food']]

    bacteria_new = [(name, dict(bacteria)[name]) for name in bacteria_new]
    nutrients_new = [(name, dict(nutrients)[name]) for name in nutrients_new]
    diseases_new = [(name, dict(diseases)[name]) for name in diseases_new]
    food_new = [(name, dict(food)[name]) for name in food_new]

    return bacteria_new, nutrients_new, diseases_new, food_new


def remove_entity_overlapping(entity_collections, tokens_words):
    """

    :param tokens_words:
    :param entity_collections: format - [ EntityCollection, EntityCollection, ... ]
    :return: sorted by tag [ EntityCollection, EntityCollection, ... ]
    """

    # tokenizing names
    tokenized_entities_names = []
    for collection in entity_collections:
        tokenized_names = []
        for entity in collection.entities:
            tokenized_names.append((entity, entity.name.split(' ')))
        tokenized_entities_names.append(tokenized_names)

    # each list contains one type of entities, so we do [0]
    entities_tags = [collection.tag for collection in entity_collections]

    entities_coordinates = {entity_tag: [] for entity_tag in entities_tags}
    coordinates_tmp = []
    for tokenized_names in tokenized_entities_names:
        for entity_and_words in tokenized_names:
            entity = entity_and_words[0]
            entity_words = entity_and_words[1]
            words_number = len(entity_words)
            # now sliding window of length `words_number` over tokens
            for i in range(len(tokens_words) - words_number + 1):
                begin = i
                end = i + words_number
                sentence_words = tokens_words[begin:end]
                if entity_words == sentence_words:
                    coordinates = (begin, end)
                    if coordinates not in coordinates_tmp:
                        coordinates_tmp.append(coordinates)
                        entities_coordinates[entity.tag].append([entity, coordinates])
                        break

    entities_coordinates_to_keep = {entity_tag: [] for entity_tag in entities_tags}

    # now remove overlapping in each entity
    for entity_tag, entities_coordinates in entities_coordinates.items():
        # comparing each entity to each entity
        for i in range(len(entities_coordinates)):
            if len(entities_coordinates) == 1:  # only one entity for tag
                entities_coordinates_to_keep[entity_tag].append(entities_coordinates[0])
                continue
            for j in range(i + 1, len(entities_coordinates)):
                entity_1_coordinates = entities_coordinates[i]
                entity_2_coordinates = entities_coordinates[j]
                entity_1_begin = entity_1_coordinates[1][0]  # [1] contains coords; [0] contains begin
                entity_2_begin = entity_2_coordinates[1][0]
                if entity_1_begin == entity_2_begin:
                    # overlapping! keep which longer
                    entity_1_end = entity_1_coordinates[1][1]  # [1][1] contains end
                    entity_2_end = entity_2_coordinates[1][1]
                    if entity_1_end > entity_2_end:
                        keep = entity_1_coordinates
                    else:
                        keep = entity_2_coordinates
                    if keep not in entities_coordinates_to_keep[entity_tag]:
                        entities_coordinates_to_keep[entity_tag].append(keep)
                    break
                else:
                    # no overlapping; keep both
                    if entity_1_coordinates not in entities_coordinates_to_keep[entity_tag]:
                        entities_coordinates_to_keep[entity_tag].append(entity_1_coordinates)
                    if entity_2_coordinates not in entities_coordinates_to_keep[entity_tag]:
                        entities_coordinates_to_keep[entity_tag].append(entity_2_coordinates)

    # now looking for overlapping between entities
    for entity_1_tag, entity_2_tag in product(entities_tags, entities_tags):
        for entity_1_coordinates in entities_coordinates_to_keep[entity_1_tag]:
            for entity_2_coordinates in entities_coordinates_to_keep[entity_2_tag]:
                coordinates_1 = entity_1_coordinates[1]
                coordinates_2 = entity_2_coordinates[1]
                set_1 = set(range(*coordinates_1))
                set_2 = set(range(*coordinates_2))
                intersection = set_1 & set_2
                if intersection == set_1 and intersection != set_2:
                    entities_coordinates_to_keep[entity_1_tag].remove(entity_1_coordinates)
                elif intersection == set_2 and intersection != set_1:
                    entities_coordinates_to_keep[entity_2_tag].remove(entity_2_coordinates)
                elif intersection == set_1 and intersection == set_2 and entity_1_tag != entity_2_tag:
                    entities_coordinates_to_keep[entity_2_tag].remove(entity_2_coordinates)

    # now initializing new EntityCollections
    entities_collections_by_tag = {entity_tag: EntityCollection([], entity_tag) for entity_tag in entities_tags}
    for entity_tag, entities_coordinates in entities_coordinates_to_keep.items():
        for entity_and_coordinates in entities_coordinates:
            entities_collections_by_tag[entity_tag].entities.append(entity_and_coordinates[0])

    entities_to_keep = list(entities_collections_by_tag.values())
    # sort by tag
    entities_to_keep.sort(key=lambda x: x.tag)

    return entities_to_keep


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


def check_if_more_than_one_list_not_empty(elements):
    return sum(map(bool, elements)) > 1


def memory_usage_psutil():
    # return the memory usage in MB
    import psutil
    process = psutil.Process(os.getpid())
    mem = process.memory_info()[0] / float(2 ** 20)
    return mem
