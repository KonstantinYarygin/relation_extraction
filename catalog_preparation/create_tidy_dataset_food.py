import pandas as pd

from catalog_preparation.catalog_creation_helper import remove_literally, all_cases_of_cases

food_file_path = '../data/food/food.tsv'
output_csv_path = '../data/food/food_catalog.csv'

if __name__ == '__main__':
    food_data = pd.read_table(food_file_path, sep=';', encoding='cp1252', header=1, names=['group', 'name'])
    food_data = remove_literally(food_data, ['pie'])
    food_data_cases = all_cases_of_cases(food_data)
    food_data = pd.merge(food_data, food_data_cases, on=list(food_data), how='outer')
    food_data = food_data.drop_duplicates()
    food_data.to_csv(output_csv_path, index=False)