import pandas as pd

from catalog_preparation.catalog_creation_helper import remove_literally, all_cases_of_cases

nutrient_file_path = '../data/nutrients/nikogosov_nutrients_normalized.tsv'
output_csv_path = '../data/nutrients/nutrients_catalog.csv'

if __name__ == '__main__':
    nutrient_data = pd.read_table(nutrient_file_path, sep='\t', header=1, names=['idname', 'name'])
    nutrient_data_long = pd.DataFrame(columns=['name'])
    for idname, name in nutrient_data.values:
        nutrient_data_i = pd.DataFrame({'name': name.split(';')})
        nutrient_data_i['idname'] = idname
        nutrient_data_long = pd.concat([nutrient_data_long, nutrient_data_i])
    nutrient_data = remove_literally(nutrient_data_long, ['Agar-agar', 'Agar', 'Protein', 'Polypeptide', 'Lead'])
    nutrient_data_cases = all_cases_of_cases(nutrient_data, do_lower=False, do_upper=False)
    nutrient_data = pd.merge(nutrient_data, nutrient_data_cases, on=list(nutrient_data), how='outer')
    nutrient_data = nutrient_data.drop_duplicates()
    nutrient_data.to_csv(output_csv_path, index=False, sep='\t')