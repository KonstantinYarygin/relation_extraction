import os

script_dir = os.path.dirname(os.path.realpath(__file__))

data_dir = os.path.join(script_dir, "..", "data")

food_file_path = os.path.join(data_dir, "food", "food.tsv")

stanford_jar_path = os.path.join(data_dir, "stanford_parser", "stanford-parser.jar")
stanford_models_jar_path = os.path.join(data_dir, "stanford_parser", "stanford-parser-3.5.2-models.jar")

stanford_lex_parser_path = os.path.join(data_dir, "stanford_parser",
                                        "edu", "stanford", "nlp", "models", "lexparser", "englishPCFG.ser.gz")

gut_catalog_file_path = os.path.join(data_dir, "bacteria", "gut_catalog.csv")

nutrients_file_path = os.path.join(data_dir, "nutrients", "nikogosov_nutrients_normalized.tsv")

diseases_doid_path = os.path.join(data_dir, "diseases", "doid.obo")

nxml_articles_dir = os.path.join(data_dir, "article_data", "texts")
abstracts_dir = os.path.join(data_dir, "article_data", "abstracts", "gut_microbiota.medline.txt")
libgen_texts_dir = os.path.join(data_dir, "article_data", "libgen")

verb_ontollogy_path = os.path.join(data_dir, 'verb_ontology.json')
