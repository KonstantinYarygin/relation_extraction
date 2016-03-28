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

CHUNK_SIZE = 10000

plural_dict = {'a': 'ae', 'us': 'i', 'er': 'ers', 'um': 'a',
               'on': 'a', 'is': 'es', 'al': 'alia',
               'ar': 'aria', 'e': 'ia', 'u': 'ua',
               'as': 'ads', 'o': 'os'}

TRIM_LETTERS_NUMBER = 20
RESULT_DIR_NAME = "result"
if not os.path.exists(RESULT_DIR_NAME):
        os.mkdir(RESULT_DIR_NAME)

SENTENCE_LENGTH_THRESHOLD = 400
