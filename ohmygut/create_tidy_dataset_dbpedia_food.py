import os

import inflect as inflect
import pandas as pd

if __name__ == '__main__':
    food_data = pd.read_csv(os.path.join('..', 'data', 'food', 'food_dbpedia_raw.csv'), sep="\t")
    food_data_sub = food_data['name'].drop_duplicates()
    food_words = list(food_data_sub)
    food_words = [word.lower() for word in food_words]

    # pluralize
    inflect_engine = inflect.engine()
    food_words = food_words + [inflect_engine.plural(word) for word in food_words]

    # capitalize
    food_words_capitalized = [word.capitalize() for word in food_words]
    food_words = food_words + food_words_capitalized

    food_data_words = pd.DataFrame({'name': food_words})
    food_data_words.to_csv(os.path.join('..', 'data', 'food', 'food_dbpedia_tidy.csv'), index=False, header=False)

