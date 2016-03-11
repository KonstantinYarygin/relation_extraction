import logging
import logging.config
import os

import yaml

path_to_constants = os.path.dirname(os.path.abspath(__file__))
log_config_name = 'log_conf.yaml'
base_logger_name = 'brightbox_logger'


def setup_logging(
        default_path=os.path.join(path_to_constants, log_config_name),
        default_level=logging.INFO,
        env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            string = f.read()
            config = yaml.load(string)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

setup_logging()
logger = logging.getLogger(base_logger_name)
pattern_logger = logging.getLogger("pattern_logger")
large_pattern_logger = logging.getLogger("large_pattern_logger")
google_search_nutrient_logger = logging.getLogger("google_search_nutrient_logger")

CLASS_EXCLUSIONS = ['type material', 'genbank acronym', 'acronym']
RANK_EXCLUSIONS = ['superkingdom', 'kingdom']

FIELD_NAME = 'name'
FIELD_CLASS = 'class'
FIELD_ID = 'id'
FIELD_RANK = 'rank'
FIELD_PARENT_ID = 'parent_id'


NCBI_COLS_NAMES = [FIELD_ID, FIELD_NAME, FIELD_CLASS]
NCBI_COLS_NODES = [FIELD_ID, FIELD_PARENT_ID, FIELD_RANK]

NCBI_NUM_NAMES = [0, 2, 6]
NCBI_NUM_NODES = [0, 2, 4]

CHUNK_SIZE = 10000

plural_dict = {'a': 'ae', 'us': 'i', 'er': 'i', 'um': 'a',
               'on': 'a', 'is': 'es', 'al': 'alia',
               'ar': 'aria', 'e': 'ia', 'u': 'ua',
               'as': ['ades', 'ads', 'ad']}

TRIM_LETTERS_NUMBER = 20