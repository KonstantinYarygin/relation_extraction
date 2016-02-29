from nltk.tokenize import StanfordTokenizer
from nltk import sent_tokenize
from itertools import product
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
stanford_tokenizer = StanfordTokenizer(path_to_jar=os.path.join(script_dir, '../../stanford_parser/stanford-parser.jar'))


def get_sentences(text):
    # todo: use stanford tokenizer
    return sent_tokenize(text)

# todo: test me
def remove_entity_overlapping(sentence, bacteria, nutrients, diseases):
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
                if sentence_tokens[i:i+len(tokens_list)] == tokens_list:
                    if (i, i+len(tokens_list)) not in tokens_coordinates[entity]:
                        tokens_coordinates[entity].append((i, i+len(tokens_list)))
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
    
    return(bacteria_new, nutrients_new, diseases_new)


# sentence = 'M. tuberculosis is the cause of tuberculosis and chronic obstructive syndrome, also M. tuberculosis is a propionic acid producer.'
# bacteria = [('M. tuberculosis', '111'), ('M. tuberculosis', '111')]
# nutrients = ['propionic']
# diseases = [('tuberculosis', 'a'), ('tuberculosis', 'a'), ('tuberculosis', 'a'), ('chronic obstructive syndrome', 'a1'), ('obstructive syndrome', 'b1')]

# print(sentence)

# print(bacteria)
# print(nutrients)
# print(diseases)

# bacteria_new, nutrients_new, diseases_new = remove_entity_overlapping(sentence, bacteria, nutrients, diseases)
# print()

# print(bacteria_new)
# print(nutrients_new)
# print(diseases_new)
