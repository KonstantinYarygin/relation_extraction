import os

project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

data_dir = os.path.join(project_dir, "data")

food_file_path = os.path.join(data_dir, "food", "food_catalog.csv")
dbpedia_food_file_path = os.path.join(data_dir, "food", "food_dbpedia_tidy.csv")

stanford_jar_path = os.path.join(data_dir, "stanford_parser", "stanford-parser.jar")
stanford_models_jar_path = os.path.join(data_dir, "stanford_parser", "stanford-parser-3.5.2-models.jar")
stanford_lex_parser_path = os.path.join(data_dir, "stanford_parser", "englishPCFG.ser.gz")

gut_catalog_file_path = os.path.join(data_dir, "bacteria", "gut_bact_catalog.csv")
all_catalog_file_path = os.path.join(data_dir, "bacteria", "all_bact_catalog.csv")

prebiotics_file_path = os.path.join(data_dir, "prebiotic", "prebiotics_tidy.csv")

nutrients_file_path = os.path.join(data_dir, "nutrients", "nutrients_catalog.csv")

diseases_csv_path = os.path.join(data_dir, "diseases", "diseases_catalog.csv")

nxml_articles_dir = os.path.join(data_dir, "article_data", "texts")
abstracts_dir = os.path.join(data_dir, "article_data", "abstracts", "gut_microbiota.medline.txt")
libgen_texts_dir = os.path.join(data_dir, "article_data", "libgen")

verb_ontollogy_path = os.path.join(data_dir, 'verb_ontology.json')

gut_bact_list_path = os.path.join(data_dir, "bacteria", "bact_names_pull_new_base.csv")  # '../data/bacteria/HITdb_taxonomy_qiime.txt'
names_path = os.path.join("data", "bacteria", "taxdump", "names.dmp")
nodes_path = os.path.join("data", "bacteria", "taxdump", "nodes.dmp")
