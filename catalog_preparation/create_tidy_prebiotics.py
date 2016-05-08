import os

import inflect
import pandas as pd

prebiotics_list_path = os.path.join('..', 'data', 'prebiotic', 'prebiotics.txt')
output_csv_path = os.path.join('..', 'data', 'prebiotic', 'prebiotics_tidy.csv')

if __name__ == '__main__':
    prebiotics_final = []

    prebiotics = pd.read_table(prebiotics_list_path, header=None, names=["name"])
    prebiotics_list = list(prebiotics['name'].drop_duplicates())

    # as is
    prebiotics_final = prebiotics_final + prebiotics_list

    # pluralize
    inflect_engine = inflect.engine()
    prebiotic_plural = [inflect_engine.plural(prebiotic) for prebiotic in prebiotics_final]
    prebiotics_final = prebiotics_final + prebiotic_plural

    # lower
    prebiotic_lower = [prebiotic.lower() for prebiotic in prebiotics_final]
    prebiotics_final = prebiotics_final + prebiotic_lower

    # capitalize
    prebiotic_capitalized = [prebiotic.capitalize() for prebiotic in prebiotics_final]
    prebiotics_final = prebiotics_final + prebiotic_capitalized

    # upper
    prebiotic_upper = [prebiotic.upper() for prebiotic in prebiotics_final]
    prebiotics_final = prebiotics_final + prebiotic_upper

    prebiotics_df = pd.DataFrame({"name": prebiotics_final})
    prebiotics_df = prebiotics_df['name'].drop_duplicates()
    prebiotics_df.to_csv(output_csv_path, index=False, header=False)
