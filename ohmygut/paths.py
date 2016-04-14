import os

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

data_dir = os.path.join(project_dir, "data")

food_file_path = os.path.join(data_dir, "food", "food.tsv")

stanford_jar_path = os.path.join(data_dir, "stanford_parser", "stanford-parser.jar")
stanford_models_jar_path = os.path.join(data_dir, "stanford_parser", "stanford-parser-3.5.2-models.jar")

stanford_lex_parser_path = os.path.join(data_dir, "stanford_parser", "englishPCFG.ser.gz")

gut_catalog_file_path = os.path.join(data_dir, "bacteria", "gut_catalog.csv")

nutrients_file_path = os.path.join(data_dir, "nutrients", "nikogosov_nutrients_normalized.tsv")

diseases_csv_path = os.path.join(data_dir, "diseases", "diseases.csv")

nxml_articles_dir = os.path.join(data_dir, "article_data", "texts")
abstracts_dir = os.path.join(data_dir, "article_data", "abstracts", "gut_microbiota.medline.txt")
libgen_texts_dir = os.path.join(data_dir, "article_data", "libgen")

verb_ontollogy_path = os.path.join(data_dir, 'verb_ontology.json')
