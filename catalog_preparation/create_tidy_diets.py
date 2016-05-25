import os

import inflect
import pandas as pd

diets_list_path = os.path.join('..', 'data', 'diet', 'diets_raw.txt')
output_csv_path = os.path.join('..', 'data', 'diet', 'diets_tidy.csv')

if __name__ == '__main__':
    diets_final = []

    diets = pd.read_table(diets_list_path, header=None, names=["name"])
    diets_list = list(diets['name'].drop_duplicates())

    # as is
    diets_final = diets_final + diets_list

    # pluralize
    inflect_engine = inflect.engine()
    diet_plural = [inflect_engine.plural(diet) for diet in diets_final]
    diets_final = diets_final + diet_plural

    # lower
    diet_lower = [diet.lower() for diet in diets_final]
    diets_final = diets_final + diet_lower

    # capitalize
    diet_capitalized = [diet.capitalize() for diet in diets_final]
    diets_final = diets_final + diet_capitalized

    # title
    diet_titled = [diet.title() for diet in diets_final]
    diets_final = diets_final + diet_titled

    # upper
    diet_upper = [diet.upper() for diet in diets_final]
    diets_final = diets_final + diet_upper

    diets_df = pd.DataFrame({"name": diets_final})
    diets_df = diets_df['name'].drop_duplicates()
    diets_df.to_csv(output_csv_path, index=False, header=False)
